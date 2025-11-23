# Simple Chat Agent with LangChain & Personas

A conversational AI agent using LangChain with personality modes, web search capabilities, and persistent conversation storage using Milvus-lite.

## Features

- 🎭 **Multiple Personas**: Switch between pirate, clown, surfer, frenchman, and jimmy personalities
- 🔍 **Web Search**: DuckDuckGo search tool integration via LangChain
- 💬 **Conversation Memory**: LangChain memory maintains context across messages
- 💾 **Persistent Storage**: All conversations and persona changes saved to Milvus-lite
- 🔄 **Session Resume**: Automatically resumes your last conversation and persona
- 🎯 **Simple CLI**: Easy-to-use command-line interface

## Setup

### 1. Create Virtual Environment

```bash
python3 -m venv .pyenv
source .pyenv/bin/activate  # On Windows: .pyenv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file in the project directory:

```
OPENAI_API_KEY=your_api_key_here
DEBUG=false
```

Get your API key from: https://platform.openai.com/api-keys

## Usage

### Start the Agent

```bash
python3 project.py
```

### Commands

- `/persona <name>` - Change persona (pirate, clown, surfer, frenchman, jimmy, neutral)
- `/clear` - Start a new conversation (clears context and resets persona)
- `/exit` - Exit the program
- `Ctrl+C` - Exit the program

### Available Personas

- **pirate** - Talk like a pirate: rough, adventurous, and full of 'Arrr!'
- **clown** - Speak playfully and make silly jokes like a circus clown
- **surfer** - Sound chill and use surfer slang
- **frenchman** - Be sophisticated and slightly dramatic with a French accent
- **jimmy** - Be relaxed and beachy, like Jimmy Buffett
- **neutral** - Be helpful and conversational (default)

### Example Session

```bash
You: Hello!
Assistant (neutral): Hi! How can I help you today?

You: /persona pirate
✓ Persona set to 'pirate'

You: What's the weather like today?
Assistant (pirate): Arrr! I'll search the seven seas fer that information, matey!
[Agent searches the web for weather information]

You: /clear
✓ Started new session

You: /exit
👋 Goodbye!
```

## Configuration

### Debug Mode

Set `DEBUG=true` in your `.env` file to enable verbose output including:
- Agent reasoning steps
- Tool usage details
- Message save confirmations
- Conversation loading details
- Full error stack traces

### Storage

Conversations are stored in `agent-conversations.db` (Milvus-lite database). Each conversation session has:
- **Unique session ID**: Timestamp-based identifier
- **Persona tracking**: Records all persona changes
- **Full chat history**: User messages and assistant responses
- **Automatic resume**: Loads the most recent session on restart

The database stores:
- Timestamp for each message
- Session ID for grouping conversations
- Role (user/assistant/system)
- Message content
- Active persona at time of message

To start completely fresh:
1. Use the `/clear` command for a new session, or
2. Delete the `agent-conversations.db` file to erase all history

## Architecture

- **LangChain**: Agent framework with tool integration
- **ChatOpenAI**: GPT-4o-mini for conversation
- **DuckDuckGo Search**: Web search tool for up-to-date information
- **ConversationBufferMemory**: Maintains conversation context
- **Milvus-lite**: Local database for persistent storage
- **Session Management**: Each conversation session has a unique ID
- **Persona System**: Dynamic personality switching with storage

## Dependencies

- `openai` - OpenAI API client
- `python-dotenv` - Environment variable management
- `pymilvus[milvus_lite]` - Local vector database for conversation storage
- `langchain` - Agent framework
- `langchain-openai` - LangChain OpenAI integration
- `langchain-community` - Community tools (DuckDuckGo)
- `duckduckgo-search` - Web search functionality

## Testing

Run the automated tests:

```bash
python3 test_agent.py
```

## How It Works

1. **Initialization**: Agent loads the most recent conversation from Milvus
2. **Persona System**: Each message is prefixed with persona instructions
3. **Memory**: LangChain maintains conversation context automatically
4. **Tools**: Agent can search the web when needed
5. **Storage**: Every message and persona change is saved to Milvus
6. **Resume**: Restart the program to continue where you left off

## Troubleshooting

**"OPENAI_API_KEY not found"**
- Make sure you created a `.env` file
- Verify the API key is set correctly
- Check that the `.env` file is in the same directory as `project.py`

**"Error: Unable to get response from AI"**
- Check your internet connection
- Verify your OpenAI API key is valid
- Check if you have API credits available
- Enable DEBUG mode for more details

**Search tool not working**
- DuckDuckGo search requires internet connection
- Try disabling VPN if search fails
- Check firewall settings

**Database errors**
- Delete `agent-conversations.db` and restart
- Check file permissions in the project directory

**Agent not remembering context**
- Verify you're using the same session (don't use `/clear` unnecessarily)
- Check that Milvus is saving messages (enable DEBUG mode)
- Make sure the database file has write permissions
