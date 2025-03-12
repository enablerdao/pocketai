"""
LLM Module - Handles interactions with Claude 3.7
"""

import os
from typing import Dict, Any, List, Optional

import anthropic
from ..config import get_config, update_config
from ..utils.logger import get_logger

logger = get_logger(__name__)

class LLMManager:
    """
    Manages interactions with the LLM (Claude 3.7)
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the LLM manager
        
        Args:
            api_key: Optional API key (will use config or environment variable if not provided)
        """
        # Use provided API key, or get from config, or get from environment
        self.api_key = api_key or get_config("llm.api_key") or os.environ.get("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            logger.warning("No API key provided for Claude. LLM functionality will be limited.")
            self.client = None
        else:
            # Update config with the API key
            update_config("llm.api_key", self.api_key)
            self.client = anthropic.Anthropic(api_key=self.api_key)
            
        # Get model configuration
        self.model = "claude-3-sonnet-20240229"  # Use Claude 3 Sonnet as a fallback
        self.temperature = get_config("llm.temperature")
        self.max_tokens = get_config("llm.max_tokens")
        
    def generate(self, 
                 messages: List[Dict[str, str]], 
                 system_prompt: Optional[str] = None,
                 temperature: Optional[float] = None,
                 max_tokens: Optional[int] = None) -> str:
        """
        Generate a response from the LLM
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            system_prompt: Optional system prompt
            temperature: Optional temperature override
            max_tokens: Optional max tokens override
            
        Returns:
            Generated text response
        """
        if not self.client:
            logger.error("Cannot generate response: No Claude API client available")
            return "Error: Claude API client not available. Please provide a valid API key."
        
        try:
            # Generate response with system parameter for Claude 3.7
            response = self.client.messages.create(
                model=self.model,
                system=system_prompt if system_prompt else "",
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens
            )
            
            return response.content[0].text
            
        except Exception as e:
            logger.error(f"Error generating response from Claude: {e}")
            return f"Error generating response: {str(e)}"
    
    def generate_with_context(self, 
                             prompt: str, 
                             context: Dict[str, Any],
                             system_prompt: Optional[str] = None) -> str:
        """
        Generate a response with the current context
        
        Args:
            prompt: The prompt to send to the LLM
            context: The current context dictionary
            system_prompt: Optional system prompt
            
        Returns:
            Generated text response
        """
        # Create a message with the prompt and relevant context
        messages = [
            {
                "role": "user",
                "content": f"{prompt}\n\nContext: {str(context)}"
            }
        ]
        
        return self.generate(messages, system_prompt=system_prompt)
    
    def get_next_action(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determine the next action based on the current context
        
        Args:
            context: The current context
            
        Returns:
            Updated context with next action
        """
        task = context.get("task", "")
        observations = context.get("observations", {})
        
        system_prompt = f"""
        You are {get_config('agent.name')}, {get_config('agent.description')}.
        Your task is to determine the next action to take based on the current context.
        You should return a JSON object with the following structure:
        {{
            "action": "action_name",
            "parameters": {{
                "param1": "value1",
                "param2": "value2"
            }},
            "reasoning": "Your reasoning for choosing this action"
        }}
        """
        
        user_message = f"""
        Current task: {task}
        
        Observations:
        {observations}
        
        Based on the current context, what is the next action I should take?
        """
        
        # Create a message with the prompt
        messages = [
            {
                "role": "user",
                "content": user_message
            }
        ]
        
        response = self.generate(messages, system_prompt=system_prompt)
        
        # Extract the action from the response
        # In a real implementation, you would parse the JSON response
        # For simplicity, we'll just add the raw response to the context
        context["next_action"] = response
        
        return context