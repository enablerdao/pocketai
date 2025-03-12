#!/usr/bin/env python3
"""
Test script for ポケットAI (Pocket AI)
"""

import os
import sys
from pocket_ai.agent.agent import PocketAI

def main():
    """Main function"""
    # Set API key from environment variable
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        print("Warning: No ANTHROPIC_API_KEY environment variable found. Please set it before running this script.")
        print("Example: export ANTHROPIC_API_KEY='your-api-key'")
        return
    
    # Create agent
    agent = PocketAI(api_key=api_key)
    
    # Run a test task
    task = "Pythonでフィボナッチ数列を計算する関数を書いてください"
    print(f"Running task: {task}")
    
    result = agent.run(task)
    
    # Print results
    print("\nTask result:")
    print(f"Task: {task}")
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

if __name__ == "__main__":
    main()