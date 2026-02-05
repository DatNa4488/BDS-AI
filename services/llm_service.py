"""
Simple LLM Service Wrapper

Provides a simple interface to call LLM (Gemini) for chat and analysis.
"""

import os
import logging
from typing import List, Dict, Optional
import google.generativeai as genai

logger = logging.getLogger(__name__)


class LLMService:
    """Simple LLM service using Gemini."""
    
    def __init__(self):
        """Initialize LLM service."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.warning("GEMINI_API_KEY not found, LLM features may not work")
        else:
            genai.configure(api_key=api_key)
        
        self.model = genai.GenerativeModel('gemini-pro')
    
    async def chat(self, messages: List[Dict]) -> str:
        """
        Send chat messages to LLM.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
                     or LangChain message objects
            
        Returns:
            LLM response text
        """
        try:
            # Convert LangChain messages to simple format
            formatted_messages = []
            for msg in messages:
                if hasattr(msg, 'content'):
                    # LangChain message object
                    role = msg.__class__.__name__.replace('Message', '').lower()
                    if role == 'system':
                        # Gemini doesn't have system role, prepend to first user message
                        formatted_messages.insert(0, {'role': 'system', 'content': msg.content})
                    else:
                        formatted_messages.append({'role': role, 'content': msg.content})
                else:
                    # Already dict format
                    formatted_messages.append(msg)
            
            # Build prompt (combine system + user messages)
            prompt_parts = []
            for msg in formatted_messages:
                role = msg.get('role', 'user')
                content = msg.get('content', '')
                
                if role == 'system':
                    prompt_parts.append(f"System Instructions:\n{content}\n")
                elif role == 'human' or role == 'user':
                    prompt_parts.append(f"User: {content}")
                elif role == 'ai' or role == 'assistant':
                    prompt_parts.append(f"Assistant: {content}")
            
            full_prompt = "\n\n".join(prompt_parts)
            
            # Generate response
            response = self.model.generate_content(full_prompt)
            return response.text
            
        except Exception as e:
            logger.error(f"LLM chat error: {e}")
            return f"Xin lỗi, tôi gặp sự cố khi xử lý yêu cầu: {str(e)}"
