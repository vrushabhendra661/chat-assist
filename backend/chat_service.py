"""
Chat service for managing conversations and generating AI responses
"""
import os
import logging
from typing import Dict, List
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class ChatService:
    """Service for handling chat conversations with OpenAI GPT"""
    
    def __init__(self):
        """Initialize chat service with OpenAI client"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.warning("OPENAI_API_KEY not found in environment variables")
        
        self.client = openai.OpenAI(api_key=self.api_key)
        self.max_context_messages = int(os.getenv("MAX_CONTEXT_MESSAGES", "10"))
        
        # In-memory context storage (session_id -> list of messages)
        self.contexts: Dict[str, List[Dict[str, str]]] = {}
        
        # System prompt for the assistant
        self.system_prompt = {
            "role": "system",
            "content": (
                "You are a helpful, friendly, and knowledgeable AI assistant. "
                "You provide clear, accurate, and concise responses. "
                "You maintain context throughout the conversation and can reference "
                "previous messages. Be conversational and engaging while staying "
                "professional and helpful."
            )
        }
    
    async def generate_response(self, message: str, session_id: str = "default") -> str:
        """
        Generate AI response based on user message and conversation context
        
        Args:
            message: User's input message
            session_id: Session identifier for context management
            
        Returns:
            AI-generated response
        """
        try:
            # Initialize context for new sessions
            if session_id not in self.contexts:
                self.contexts[session_id] = []
            
            # Add user message to context
            self.contexts[session_id].append({
                "role": "user",
                "content": message
            })
            
            # Limit context size to prevent token overflow
            if len(self.contexts[session_id]) > self.max_context_messages:
                self.contexts[session_id] = self.contexts[session_id][-self.max_context_messages:]
            
            # Build message history with system prompt
            messages = [self.system_prompt] + self.contexts[session_id]
            
            # Call OpenAI API
            logger.info(f"Calling OpenAI API for session {session_id}")
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            # Extract response
            assistant_message = response.choices[0].message.content
            
            # Add assistant response to context
            self.contexts[session_id].append({
                "role": "assistant",
                "content": assistant_message
            })
            
            logger.info(f"Response generated successfully for session {session_id}")
            return assistant_message
            
        except openai.APIError as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise Exception(f"OpenAI API error: {str(e)}")
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise Exception(f"Failed to generate response: {str(e)}")
    
    def clear_context(self, session_id: str):
        """
        Clear conversation context for a specific session
        
        Args:
            session_id: Session identifier to clear
        """
        if session_id in self.contexts:
            self.contexts[session_id] = []
            logger.info(f"Context cleared for session {session_id}")
        else:
            logger.warning(f"No context found for session {session_id}")
    
    def get_context(self, session_id: str) -> List[Dict[str, str]]:
        """
        Get conversation context for a specific session
        
        Args:
            session_id: Session identifier
            
        Returns:
            List of message dictionaries
        """
        return self.contexts.get(session_id, [])

