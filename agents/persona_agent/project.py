import os
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module=r"milvus_lite")
from datetime import datetime
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_tools_agent
from pymilvus import MilvusClient
from langchain_core.tools import Tool, StructuredTool
import requests

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
EMBEDDING_DIM = 1536
METRIC_TYPE = "COSINE"

# Load .env
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Initialize Milvus
client_milvus = MilvusClient(uri="agent-conversations.db")

def init_milvus():
    """Initialize Milvus collection for conversation storage."""
    collection_name = "persona_conversations"
    
    # Create collection if it doesn't exist
    if not client_milvus.has_collection(collection_name):
        client_milvus.create_collection(
            collection_name=collection_name,
            dimension=EMBEDDING_DIM,
            metric_type=METRIC_TYPE,
            auto_id=True,
            enable_dynamic_field=True,
        )
        if DEBUG:
            print(f"Created collection: {collection_name}")
        # Create default index for vector field
        try:
            client_milvus.create_index(
                collection_name=collection_name,
                index_name="idx_vector",
                field_name="vector",
                index_params={"index_type": "AUTOINDEX", "metric_type": METRIC_TYPE}
            )
            if DEBUG:
                print("Created vector index: idx_vector")
        except Exception as e:
            if DEBUG:
                print(f"⚠️  Skipped index creation: {e}")
    # Ensure collection is loaded for search
    try:
        client_milvus.load_collection(collection_name)
    except Exception:
        pass
    
    return collection_name

# Initialize collection
collection_name = init_milvus()

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.8, api_key=openai_api_key)

# Tool: DuckDuckGo search (if available)
SEARCH_AVAILABLE = True
try:
    import time
    from duckduckgo_search import DDGS

    def web_search_safe(query: str) -> str:
        """DuckDuckGo web search with retries; returns concise bullet list."""
        query = (query or "").strip()
        if not query:
            return "(no query)"
        last_err = None
        for attempt in range(3):
            try:
                with DDGS() as ddgs:
                    results = list(ddgs.text(query, max_results=5))
                if not results:
                    return "(no results)"
                lines = []
                for r in results:
                    title = r.get("title") or r.get("body") or "result"
                    href = r.get("href") or r.get("link") or ""
                    lines.append(f"- {title} {(' - ' + href) if href else ''}")
                return "\n".join(lines)
            except Exception as e:
                last_err = e
                time.sleep(2 ** attempt)
        return f"(search unavailable: {last_err})"

    search_tool = StructuredTool.from_function(
        func=web_search_safe,
        name="web_search",
        description="Search the web and return up to 5 concise results",
    )
except Exception as e:
    SEARCH_AVAILABLE = False
    search_tool = None
    if DEBUG:
        print(f"⚠️  Could not initialize search tool: {e}")

# Weather tool (StructuredTool)
WEATHER_AVAILABLE = True
try:
    import requests

    def get_weather(city: str) -> str:
        """Get 3-day weather forecast for a city using Open-Meteo geocoding + forecast APIs."""
        if not city:
            return "Please provide a city name. Example: /weather Austin, TX"

        # 1) Geocode the city to latitude/longitude
        try:
            geo_resp = requests.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": city, "count": 1, "language": "en", "format": "json"},
                timeout=10,
            )
            geo_resp.raise_for_status()
            geo = geo_resp.json()
            results = geo.get("results") or []
            if not results:
                return f"Could not find coordinates for '{city}'. Try a more specific name."
            top = results[0]
            lat = float(top.get("latitude"))
            lon = float(top.get("longitude"))
            city_name = top.get("name") or city
            admin = top.get("admin1") or ""
            country = top.get("country") or ""
        except Exception as e:
            return f"Geocoding failed for '{city}': {e}"

        # 2) Fetch forecast (Fahrenheit units, auto-timezone)
        try:
            fc_resp = requests.get(
                "https://api.open-meteo.com/v1/forecast",
                params={
                    "latitude": lat,
                    "longitude": lon,
                    "daily": "temperature_2m_max,temperature_2m_min",
                    "timezone": "auto",
                    "temperature_unit": "fahrenheit",
                },
                timeout=10,
            )
            fc_resp.raise_for_status()
            data = fc_resp.json()
            temps = data.get("daily", {})
            times = temps.get("time", [])
            tmin = temps.get("temperature_2m_min", [])
            tmax = temps.get("temperature_2m_max", [])
            days = list(zip(times, tmin, tmax))[:3]
            if not days:
                return f"No forecast available for {city_name}."
            forecast = "\n".join([f"{d}: {low}°F - {high}°F" for d, low, high in days])
            loc = f"{city_name}{(', ' + admin) if admin else ''}{(', ' + country) if country else ''}"
            return f"3-day forecast for {loc} ({lat:.2f},{lon:.2f}):\n{forecast}"
        except Exception as e:
            return f"Weather lookup failed for '{city}': {e}"

    weather_tool = StructuredTool.from_function(
        func=get_weather,
        name="get_weather",
        description="Get a 3-day weather forecast for a given city name",
    )
except Exception as e:
    WEATHER_AVAILABLE = False
    weather_tool = None
    if DEBUG:
        print(f"⚠️  Could not initialize weather tool: {e}")


# Persona system prompt
def persona_prompt(persona_name: str) -> str:
    """Return a short system instruction for the given persona."""
    persona_styles = {
        "pirate": "Talk like a pirate: rough, adventurous, and full of 'Arrr!'",
        "clown": "Speak playfully and make silly jokes like a circus clown.",
        "surfer": "Sound chill and use surfer slang.",
        "frenchman": "Be sophisticated and slightly dramatic with a French accent.",
        "jimmy": "Be relaxed and beachy, like Jimmy Buffett.",
        "neutral": "Be helpful and conversational."
    }
    return persona_styles.get(persona_name.lower(), "Be yourself.")


class PersonaAgent:
    """Agent with persona and conversation storage."""
    
    def __init__(self, milvus_client, collection_name, session_id=None):
        self.milvus = milvus_client
        self.collection_name = collection_name
        self.session_id = session_id or datetime.now().strftime("%Y%m%d_%H%M%S")
        self.persona = "neutral"
        self.llm = llm
        self.search_tool = search_tool

        # Session-scoped chat histories
        self._history_by_session = {}

        # Build tools-enabled agent prompt (must include agent_scratchpad)
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "{system_prompt}"),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ])

        # Assemble active tools
        active_tools = [t for t in [search_tool, weather_tool] if t is not None]

        # Create an OpenAI tools agent (required per setup)
        agent_graph = create_openai_tools_agent(self.llm, active_tools, self.prompt)
        self.agent = AgentExecutor(
            agent=agent_graph,
            tools=active_tools,
            verbose=DEBUG,
            handle_parsing_errors=True,
        )

        # Wrap executor with session-scoped message history
        def _get_session_history(session_id: str):
            return self._history_by_session.setdefault(session_id, ChatMessageHistory())

        self.agent_with_history = RunnableWithMessageHistory(
            self.agent,
            get_session_history=_get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )
        
        # Load existing conversation and persona
        self.load_conversation()
    
    def save_message(self, role, content, persona=None):
        """Save a message to Milvus."""
        # Compute embedding vector for semantic search
        try:
            vector = embeddings.embed_query(content)
        except Exception:
            vector = [0.0] * EMBEDDING_DIM

        data = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "role": role,
            "content": content,
            "persona": persona or self.persona,
            "vector": vector
        }
        
        try:
            self.milvus.insert(
                collection_name=self.collection_name,
                data=[data]
            )
            if DEBUG:
                print(f"💾 Saved {role} message with persona '{persona or self.persona}'")
        except Exception as e:
            if DEBUG:
                print(f"⚠️  Error saving message: {e}")
    
    def save_persona(self, persona):
        """Save persona change to Milvus."""
        # Also embed persona change note so it can be surfaced in search
        note = f"Persona changed to: {persona}"
        try:
            vector = embeddings.embed_query(note)
        except Exception:
            vector = [0.0] * EMBEDDING_DIM

        data = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "role": "system",
            "content": note,
            "persona": persona,
            "vector": vector
        }
        
        try:
            self.milvus.insert(
                collection_name=self.collection_name,
                data=[data]
            )
            if DEBUG:
                print(f"💾 Saved persona change: {persona}")
        except Exception as e:
            if DEBUG:
                print(f"⚠️  Error saving persona: {e}")
    
    def load_conversation(self):
        """Load conversation history and persona from Milvus."""
        try:
            # Query for messages in this session
            results = self.milvus.query(
                collection_name=self.collection_name,
                filter=f'session_id == "{self.session_id}"',
                output_fields=["timestamp", "role", "content", "persona"]
            )
            
            # Sort by timestamp
            results.sort(key=lambda x: x.get("timestamp", ""))
            
            message_count = 0
            history = self.get_session_history()
            for msg in results:
                role = msg["role"]
                content = msg["content"]
                persona = msg.get("persona", "neutral")
                
                # Update persona if this is a system message about persona change
                if role == "system" and "Persona changed to:" in content:
                    self.persona = persona
                    if DEBUG:
                        print(f"📝 Restored persona: {persona}")
                
                # Add user/assistant messages to history
                elif role == "user":
                    history.add_user_message(content)
                    message_count += 1
                elif role == "assistant":
                    history.add_ai_message(content)
                    message_count += 1
            
            if message_count > 0:
                print(f"✓ Loaded {message_count} messages from session (persona: {self.persona})\n")
            
        except Exception as e:
            if DEBUG:
                print(f"⚠️  Error loading conversation: {e}")
    
    def set_persona(self, persona):
        """Change the persona and save to Milvus."""
        self.persona = persona
        self.save_persona(persona)
    
    def chat(self, user_input):
        """Process user input with current persona and return response."""
        try:
            # Save user message
            self.save_message("user", user_input)
            
            # Invoke tools-enabled agent with session-scoped history
            result = self.agent_with_history.invoke(
                {"input": user_input, "system_prompt": persona_prompt(self.persona)},
                config={"configurable": {"session_id": self.session_id}},
            )
            # AgentExecutor returns dict with "output"
            if isinstance(result, dict) and "output" in result:
                response_text = result["output"]
            else:
                response_text = getattr(result, "content", str(result))
            
            # Save assistant response
            self.save_message("assistant", response_text)
            
            return response_text
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            print(f"\n⚠️  {error_msg}\n")
            if DEBUG:
                import traceback
                traceback.print_exc()
            return None
    
    def clear_conversation(self):
        """Start a new conversation session."""
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.persona = "neutral"
        # New session uses a fresh history; keep old session history in memory
        print(f"✓ Started new session: {self.session_id}\n")

    def semantic_search(self, query: str, top_k: int = 5, current_session_only: bool = True):
        """Search stored messages semantically using Milvus."""
        try:
            query_vec = embeddings.embed_query(query)
        except Exception as e:
            print(f"⚠️  Failed to embed query: {e}")
            return []

        milvus_filter = None
        if current_session_only:
            milvus_filter = f'session_id == "{self.session_id}"'

        try:
            results = client_milvus.search(
                collection_name=self.collection_name,
                data=[query_vec],
                limit=top_k,
                filter=milvus_filter,
                output_fields=["timestamp", "role", "content", "persona", "session_id"],
                search_params={"metric_type": METRIC_TYPE}
            )
            # MilvusClient returns a list of hits per query
            hits = results[0] if results else []
            return [
                {
                    "score": hit.get("distance") or hit.get("score"),
                    "timestamp": hit.get("entity", {}).get("timestamp"),
                    "role": hit.get("entity", {}).get("role"),
                    "content": hit.get("entity", {}).get("content"),
                    "persona": hit.get("entity", {}).get("persona"),
                    "session_id": hit.get("entity", {}).get("session_id"),
                }
                for hit in hits
            ]
        except Exception as e:
            if DEBUG:
                print(f"⚠️  Search error: {e}")
            return []


# Main conversation loop
def main():
    print("=" * 60)
    print("🤖 LangChain Persona Agent with Memory")
    print("=" * 60)
    print("Commands:")
    print("  /persona <name> - Change persona (pirate, clown, surfer, frenchman, jimmy)")
    print("  /clear          - Start a new conversation")
    print("  /search <query> - Semantic search in memory")
    print("  /exit           - Exit the program")
    print("=" * 60)
    print()
    
    # Initialize agent
    agent = PersonaAgent(client_milvus, collection_name)
    
    while True:
        try:
            user_input = input(f"You: ").strip()
            
            if not user_input:
                continue
            
            if user_input == "/exit":
                print("\n👋 Goodbye!")
                break
            
            if user_input.startswith("/persona"):
                parts = user_input.split(" ", 1)
                if len(parts) > 1:
                    persona = parts[1]
                    agent.set_persona(persona)
                    print(f"✓ Persona set to '{persona}'\n")
                else:
                    print("⚠️  Please specify a persona: /persona <name>\n")
                continue
            
            if user_input == "/clear":
                agent.clear_conversation()
                continue

            if user_input.startswith("/search "):
                query = user_input.split(" ", 1)[1].strip()
                results = agent.semantic_search(query)
                if not results:
                    print("\n(no results)\n")
                else:
                    print("\nTop matches:\n")
                    for i, r in enumerate(results, 1):
                        score = r.get("score")
                        print(f"{i}. [{r['role']}] ({r['persona']}) {r['timestamp']}  score={score}")
                        print(f"   {r['content'][:200]}\n")
                continue
            
            # Get response
            response = agent.chat(user_input)
            
            if response:
                print(f"\nAssistant ({agent.persona}): {response}\n")
        
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except EOFError:
            print("\n\n👋 Goodbye!")
            break

if __name__ == "__main__":
    main()
