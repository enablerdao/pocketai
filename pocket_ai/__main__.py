"""
Main entry point for ポケットAI (Pocket AI)
"""

import os
import sys
import argparse

from .server import run_server
from .agent.agent import PocketAI
from .config import update_config
from .utils.logger import get_logger

logger = get_logger(__name__)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="ポケットAI (Pocket AI) - A Doraemon-inspired AI assistant")
    
    # Add arguments
    parser.add_argument("--api-key", help="API key for Claude")
    parser.add_argument("--port", type=int, help="Port for the web server")
    parser.add_argument("--host", help="Host for the web server")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    parser.add_argument("--task", help="Run a single task and exit")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Update configuration
    if args.api_key:
        update_config("llm.api_key", args.api_key)
        os.environ["ANTHROPIC_API_KEY"] = args.api_key
    
    if args.port:
        update_config("server.port", args.port)
    
    if args.host:
        update_config("server.host", args.host)
    
    if args.headless is not None:
        update_config("browser.headless", args.headless)
    
    # Run a single task if specified
    if args.task:
        logger.info(f"Running task: {args.task}")
        
        agent = PocketAI()
        result = agent.run(args.task)
        
        print("\nTask result:")
        print(f"Task: {args.task}")
        print(f"Completed: {result.get('complete', False)}")
        print(f"Iterations: {result.get('iterations', 0)}")
        
        if result.get('action_results'):
            print("\nAction results:")
            for key, value in result['action_results'].items():
                print(f"{key}: {value}")
        
        if result.get('evaluation'):
            print("\nEvaluation:")
            for key, value in result['evaluation'].items():
                print(f"{key}: {value}")
        
        sys.exit(0)
    
    # Run the web server
    run_server()

if __name__ == "__main__":
    main()