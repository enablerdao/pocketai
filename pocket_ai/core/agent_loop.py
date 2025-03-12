"""
Agent Loop - The core of ポケットAI (Pocket AI)
Implements the Observe-Judge-Act-Evaluate loop
"""

import time
from typing import Dict, Any, List, Optional, Callable

from ..config import get_config
from ..utils.logger import get_logger

logger = get_logger(__name__)

class AgentLoop:
    """
    The core agent loop that implements the Observe-Judge-Act-Evaluate cycle
    """
    
    def __init__(self):
        """Initialize the agent loop"""
        self.name = get_config("agent.name")
        self.description = get_config("agent.description")
        self.max_iterations = get_config("agent.max_iterations")
        self.memory = []
        self.memory_size = get_config("agent.memory_size")
        self.current_task = None
        self.observers = []
        self.judges = []
        self.actors = []
        self.evaluators = []
        
    def register_observer(self, observer: Callable) -> None:
        """Register an observer function"""
        self.observers.append(observer)
        
    def register_judge(self, judge: Callable) -> None:
        """Register a judge function"""
        self.judges.append(judge)
        
    def register_actor(self, actor: Callable) -> None:
        """Register an actor function"""
        self.actors.append(actor)
        
    def register_evaluator(self, evaluator: Callable) -> None:
        """Register an evaluator function"""
        self.evaluators.append(evaluator)
    
    def observe(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Observe the environment and gather information
        
        Args:
            context: The current context
            
        Returns:
            Updated context with observations
        """
        logger.info("🔍 Observing environment...")
        
        for observer in self.observers:
            try:
                context = observer(context)
            except Exception as e:
                logger.error(f"Observer error: {e}")
                
        return context
    
    def judge(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Judge what action to take based on observations
        
        Args:
            context: The current context with observations
            
        Returns:
            Updated context with judgment
        """
        logger.info("🤔 Making judgment...")
        
        for judge in self.judges:
            try:
                context = judge(context)
            except Exception as e:
                logger.error(f"Judge error: {e}")
                
        return context
    
    def act(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Take action based on judgment
        
        Args:
            context: The current context with judgment
            
        Returns:
            Updated context with action results
        """
        logger.info("🚀 Taking action...")
        
        for actor in self.actors:
            try:
                context = actor(context)
            except Exception as e:
                logger.error(f"Actor error: {e}")
                
        return context
    
    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate the results of the action
        
        Args:
            context: The current context with action results
            
        Returns:
            Updated context with evaluation
        """
        logger.info("📊 Evaluating results...")
        
        for evaluator in self.evaluators:
            try:
                context = evaluator(context)
            except Exception as e:
                logger.error(f"Evaluator error: {e}")
                
        return context
    
    def add_to_memory(self, entry: Dict[str, Any]) -> None:
        """
        Add an entry to the agent's memory
        
        Args:
            entry: The memory entry to add
        """
        self.memory.append(entry)
        
        # Trim memory if it exceeds the maximum size
        if len(self.memory) > self.memory_size:
            self.memory = self.memory[-self.memory_size:]
    
    def run_once(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run one iteration of the agent loop
        
        Args:
            context: The initial context
            
        Returns:
            Updated context after one iteration
        """
        # Add timestamp to context
        context["timestamp"] = time.time()
        
        # Run the observe-judge-act-evaluate loop
        context = self.observe(context)
        context = self.judge(context)
        context = self.act(context)
        context = self.evaluate(context)
        
        # Add to memory
        self.add_to_memory({
            "timestamp": context["timestamp"],
            "task": self.current_task,
            "context": context
        })
        
        return context
    
    def run(self, task: str, initial_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run the agent loop for a given task
        
        Args:
            task: The task to perform
            initial_context: Optional initial context
            
        Returns:
            Final context after completing the task
        """
        self.current_task = task
        
        # Initialize context
        context = initial_context or {}
        context["task"] = task
        context["iterations"] = 0
        context["complete"] = False
        
        logger.info(f"🤖 Starting task: {task}")
        
        # Run the loop until the task is complete or max iterations is reached
        while not context.get("complete", False) and context["iterations"] < self.max_iterations:
            context["iterations"] += 1
            logger.info(f"Iteration {context['iterations']}/{self.max_iterations}")
            
            context = self.run_once(context)
            
            # Check if the task is complete
            if context.get("complete", False):
                logger.info(f"✅ Task completed in {context['iterations']} iterations")
                break
                
        if not context.get("complete", False):
            logger.warning(f"⚠️ Task not completed after {self.max_iterations} iterations")
            
        return context