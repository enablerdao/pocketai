"""
Agent implementation for ポケットAI (Pocket AI)
"""

import os
import json
from typing import Dict, Any, List, Optional, Union, Callable

from ..core.agent_loop import AgentLoop
from ..core.llm import LLMManager
from ..browser.browser_manager import BrowserManager
from .programming_tools import ProgrammingTools
from ..utils.logger import get_logger

logger = get_logger(__name__)

class PocketAI:
    """
    ポケットAI (Pocket AI) - A Doraemon-inspired AI assistant
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the ポケットAI agent
        
        Args:
            api_key: Optional API key for the LLM
        """
        self.agent_loop = AgentLoop()
        self.llm = LLMManager(api_key=api_key)
        self.browser_manager = BrowserManager()
        self.programming_tools = ProgrammingTools()
        
        # Register components in the agent loop
        self._register_components()
        
    def _register_components(self) -> None:
        """Register components in the agent loop"""
        # Register observers
        self.agent_loop.register_observer(self._observe_environment)
        
        # Register judges
        self.agent_loop.register_judge(self._judge_next_action)
        
        # Register actors
        self.agent_loop.register_actor(self._execute_action)
        
        # Register evaluators
        self.agent_loop.register_evaluator(self._evaluate_results)
        
    def _observe_environment(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Observe the environment
        
        Args:
            context: The current context
            
        Returns:
            Updated context with observations
        """
        observations = {}
        
        # Get the current task
        task = context.get("task", "")
        
        # Check if we need to observe the browser
        if context.get("browser_url"):
            try:
                with self.browser_manager as browser:
                    browser.open(context["browser_url"])
                    observations["browser_content"] = browser.get_content()
                    
                    # Take a screenshot if needed
                    if context.get("take_screenshot", False):
                        screenshot_path = f"/tmp/pocket_ai_screenshot_{context['iterations']}.png"
                        browser.screenshot(screenshot_path)
                        observations["screenshot_path"] = screenshot_path
            except Exception as e:
                logger.error(f"Error observing browser: {e}")
                observations["browser_error"] = str(e)
        
        # Add observations to context
        context["observations"] = observations
        
        return context
    
    def _judge_next_action(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Judge what action to take next
        
        Args:
            context: The current context
            
        Returns:
            Updated context with judgment
        """
        # Use the LLM to determine the next action
        context = self.llm.get_next_action(context)
        
        # Parse the next action
        next_action = context.get("next_action", "")
        
        try:
            # Try to parse as JSON
            action_data = json.loads(next_action)
            context["parsed_action"] = action_data
        except:
            # If parsing fails, use the raw text
            context["parsed_action"] = {
                "action": "unknown",
                "parameters": {},
                "reasoning": next_action
            }
        
        return context
    
    def _execute_action(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the chosen action
        
        Args:
            context: The current context
            
        Returns:
            Updated context with action results
        """
        action_data = context.get("parsed_action", {})
        action = action_data.get("action", "unknown")
        parameters = action_data.get("parameters", {})
        
        results = {}
        
        try:
            if action == "browse":
                # Browse to a URL
                url = parameters.get("url", "")
                if url:
                    with self.browser_manager as browser:
                        browser.open(url)
                        results["browser_content"] = browser.get_content()
                        
                        # Set the URL for future observations
                        context["browser_url"] = url
                else:
                    results["error"] = "No URL provided for browse action"
            
            elif action == "click":
                # Click on an element
                selector = parameters.get("selector", "")
                if selector and context.get("browser_url"):
                    with self.browser_manager as browser:
                        browser.click(selector)
                        results["browser_content"] = browser.get_content()
                else:
                    results["error"] = "No selector or browser URL provided for click action"
            
            elif action == "type":
                # Type text into an element
                selector = parameters.get("selector", "")
                text = parameters.get("text", "")
                if selector and text and context.get("browser_url"):
                    with self.browser_manager as browser:
                        browser.type(selector, text)
                        results["browser_content"] = browser.get_content()
                else:
                    results["error"] = "No selector, text, or browser URL provided for type action"
            
            elif action == "execute_code":
                # Execute code
                code = parameters.get("code", "")
                language = parameters.get("language", "python")
                if code:
                    results = self.programming_tools.execute_code(code, language)
                else:
                    results["error"] = "No code provided for execute_code action"
            
            elif action == "search_code":
                # Search for code
                query = parameters.get("query", "")
                language = parameters.get("language")
                if query:
                    results = self.programming_tools.search_code(query, language)
                else:
                    results["error"] = "No query provided for search_code action"
            
            elif action == "analyze_code":
                # Analyze code
                code = parameters.get("code", "")
                language = parameters.get("language", "python")
                if code:
                    results = self.programming_tools.analyze_code(code, language)
                else:
                    results["error"] = "No code provided for analyze_code action"
            
            elif action == "complete":
                # Mark the task as complete
                context["complete"] = True
                results["message"] = "Task completed successfully"
            
            else:
                results["error"] = f"Unknown action: {action}"
        
        except Exception as e:
            logger.error(f"Error executing action {action}: {e}")
            results["error"] = str(e)
        
        # Add results to context
        context["action_results"] = results
        
        return context
    
    def _evaluate_results(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate the results of the action
        
        Args:
            context: The current context
            
        Returns:
            Updated context with evaluation
        """
        action_data = context.get("parsed_action", {})
        action = action_data.get("action", "unknown")
        results = context.get("action_results", {})
        
        evaluation = {
            "success": "error" not in results,
            "feedback": ""
        }
        
        if "error" in results:
            evaluation["feedback"] = f"Error: {results['error']}"
        else:
            evaluation["feedback"] = f"Action {action} executed successfully"
        
        # Add evaluation to context
        context["evaluation"] = evaluation
        
        return context
    
    def run(self, task: str, initial_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run the agent for a given task
        
        Args:
            task: The task to perform
            initial_context: Optional initial context
            
        Returns:
            Final context after completing the task
        """
        return self.agent_loop.run(task, initial_context)