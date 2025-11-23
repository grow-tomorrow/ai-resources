"""
Automated tests for the LangChain Persona Agent
"""

import os
import sys
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime

# Import the agent
from project import PersonaAgent, init_milvus, persona_prompt


class TestPersonaAgent:
    """Test suite for PersonaAgent class"""
    
    def test_persona_prompts(self):
        """Test that persona prompts are defined correctly"""
        print("Test 1: Persona Prompts...", end=" ")
        
        # Test known personas
        pirate = persona_prompt("pirate")
        assert "pirate" in pirate.lower()
        assert len(pirate) > 0
        
        clown = persona_prompt("clown")
        assert "clown" in clown.lower() or "joke" in clown.lower()
        
        # Test unknown persona (should have default)
        unknown = persona_prompt("unknown_persona_xyz")
        assert len(unknown) > 0
        
        print("✓ PASSED")
        return True
    
    def test_agent_initialization(self):
        """Test that agent initializes correctly"""
        print("Test 2: Agent Initialization...", end=" ")
        
        # Create mock Milvus client
        mock_milvus = Mock()
        mock_milvus.query.return_value = []
        
        # Initialize agent
        agent = PersonaAgent(mock_milvus, "test_collection", session_id="test_session")
        
        # Check initialization
        assert agent.milvus == mock_milvus
        assert agent.collection_name == "test_collection"
        assert agent.session_id == "test_session"
        assert agent.persona == "neutral"
        # Ensure LLM and session history are configured
        assert getattr(agent, "llm", None) is not None
        assert agent.get_session_history() is not None
        
        print("✓ PASSED")
        return True
    
    def test_persona_change(self):
        """Test that persona can be changed and saved"""
        print("Test 3: Persona Change...", end=" ")
        
        # Create mock Milvus client
        mock_milvus = Mock()
        mock_milvus.query.return_value = []
        mock_milvus.insert.return_value = None
        
        # Initialize agent
        agent = PersonaAgent(mock_milvus, "test_collection", session_id="test_session")
        
        # Change persona
        agent.set_persona("pirate")
        
        # Check that persona changed
        assert agent.persona == "pirate"
        
        # Check that save was called
        assert mock_milvus.insert.called
        
        print("✓ PASSED")
        return True
    
    def test_message_storage(self):
        """Test that messages are saved correctly"""
        print("Test 4: Message Storage...", end=" ")
        
        # Create mock Milvus client
        mock_milvus = Mock()
        mock_milvus.query.return_value = []
        mock_milvus.insert.return_value = None
        
        # Initialize agent
        agent = PersonaAgent(mock_milvus, "test_collection", session_id="test_session")
        
        # Save a message
        agent.save_message("user", "Hello!", persona="pirate")
        
        # Check that insert was called
        assert mock_milvus.insert.called
        call_args = mock_milvus.insert.call_args
        
        # Verify the data structure
        data = call_args[1]["data"][0]
        assert data["role"] == "user"
        assert data["content"] == "Hello!"
        assert data["persona"] == "pirate"
        assert data["session_id"] == "test_session"
        assert "timestamp" in data
        
        print("✓ PASSED")
        return True
    
    def test_conversation_loading(self):
        """Test that conversations can be loaded from storage"""
        print("Test 5: Conversation Loading...", end=" ")
        
        # Create mock Milvus client with existing conversation
        mock_milvus = Mock()
        mock_milvus.query.return_value = [
            {
                "timestamp": "2024-01-01T10:00:00",
                "role": "system",
                "content": "Persona changed to: pirate",
                "persona": "pirate"
            },
            {
                "timestamp": "2024-01-01T10:00:01",
                "role": "user",
                "content": "Hello!",
                "persona": "pirate"
            },
            {
                "timestamp": "2024-01-01T10:00:02",
                "role": "assistant",
                "content": "Arrr! Hello matey!",
                "persona": "pirate"
            }
        ]
        
        # Initialize agent (should load conversation)
        agent = PersonaAgent(mock_milvus, "test_collection", session_id="test_session")
        
        # Check that persona was restored
        assert agent.persona == "pirate"
        
        # Check that history has messages
        messages = agent.get_session_history().messages
        assert len(messages) >= 2  # At least user and assistant messages
        
        print("✓ PASSED")
        return True
    
    def test_clear_conversation(self):
        """Test that clearing conversation works"""
        print("Test 6: Clear Conversation...", end=" ")
        
        # Create mock Milvus client
        mock_milvus = Mock()
        mock_milvus.query.return_value = []
        
        # Initialize agent
        agent = PersonaAgent(mock_milvus, "test_collection", session_id="old_session")
        agent.set_persona("pirate")
        old_session_id = agent.session_id
        
        # Clear conversation
        agent.clear_conversation()
        
        # Check that session ID changed and persona reset
        assert agent.session_id != old_session_id
        assert agent.persona == "neutral"
        
        # Check that new session history is empty
        messages = agent.get_session_history().messages
        assert len(messages) == 0
        
        print("✓ PASSED")
        return True
    
    def test_milvus_initialization(self):
        """Test that Milvus collection can be initialized"""
        print("Test 7: Milvus Initialization...", end=" ")
        
        # This will test the init_milvus function exists and returns a name
        collection_name = init_milvus()
        assert collection_name is not None
        assert len(collection_name) > 0
        assert collection_name == "persona_conversations"
        
        print("✓ PASSED")
        return True


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("🧪 Running LangChain Persona Agent Tests")
    print("=" * 60)
    print()
    
    test_suite = TestPersonaAgent()
    tests = [
        test_suite.test_persona_prompts,
        test_suite.test_agent_initialization,
        test_suite.test_persona_change,
        test_suite.test_message_storage,
        test_suite.test_conversation_loading,
        test_suite.test_clear_conversation,
        test_suite.test_milvus_initialization,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ FAILED - {e}")
            if os.getenv("DEBUG", "false").lower() == "true":
                import traceback
                traceback.print_exc()
            failed += 1
    
    print()
    print("=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
