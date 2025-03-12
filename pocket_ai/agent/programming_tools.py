"""
Programming Tools - Tools for programming tasks
"""

import os
import subprocess
from typing import Dict, Any, List, Optional, Union

from ..utils.logger import get_logger

logger = get_logger(__name__)

class ProgrammingTools:
    """
    Tools for programming tasks
    """
    
    @staticmethod
    def execute_code(code: str, language: str = "python") -> Dict[str, Any]:
        """
        Execute code in the specified language
        
        Args:
            code: The code to execute
            language: The programming language
            
        Returns:
            Dictionary with execution results
        """
        result = {
            "success": False,
            "output": "",
            "error": ""
        }
        
        try:
            if language.lower() == "python":
                # Create a temporary file
                temp_file = "/tmp/pocket_ai_temp.py"
                with open(temp_file, "w") as f:
                    f.write(code)
                
                # Execute the code
                process = subprocess.Popen(
                    ["python", temp_file],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                stdout, stderr = process.communicate()
                
                # Check if execution was successful
                if process.returncode == 0:
                    result["success"] = True
                    result["output"] = stdout
                else:
                    result["error"] = stderr
                
                # Clean up
                os.remove(temp_file)
                
            elif language.lower() == "javascript":
                # Create a temporary file
                temp_file = "/tmp/pocket_ai_temp.js"
                with open(temp_file, "w") as f:
                    f.write(code)
                
                # Execute the code
                process = subprocess.Popen(
                    ["node", temp_file],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                stdout, stderr = process.communicate()
                
                # Check if execution was successful
                if process.returncode == 0:
                    result["success"] = True
                    result["output"] = stdout
                else:
                    result["error"] = stderr
                
                # Clean up
                os.remove(temp_file)
                
            else:
                result["error"] = f"Unsupported language: {language}"
                
        except Exception as e:
            result["error"] = str(e)
            
        return result
    
    @staticmethod
    def search_code(query: str, language: Optional[str] = None) -> Dict[str, Any]:
        """
        Search for code examples (simulated)
        
        Args:
            query: The search query
            language: Optional language filter
            
        Returns:
            Dictionary with search results
        """
        # In a real implementation, this would search GitHub or other code repositories
        # For now, we'll return simulated results
        
        results = []
        
        if language:
            logger.info(f"Searching for {query} in {language}")
            
            # Simulated results
            if language.lower() == "python":
                results = [
                    {
                        "title": "Example Python function",
                        "code": "def example_function(param1, param2):\n    \"\"\"Example function\"\"\"\n    return param1 + param2",
                        "source": "simulated"
                    },
                    {
                        "title": "Python class example",
                        "code": "class ExampleClass:\n    def __init__(self, name):\n        self.name = name\n    \n    def greet(self):\n        return f\"Hello, {self.name}!\"",
                        "source": "simulated"
                    }
                ]
            elif language.lower() == "javascript":
                results = [
                    {
                        "title": "Example JavaScript function",
                        "code": "function exampleFunction(param1, param2) {\n    // Example function\n    return param1 + param2;\n}",
                        "source": "simulated"
                    },
                    {
                        "title": "JavaScript class example",
                        "code": "class ExampleClass {\n    constructor(name) {\n        this.name = name;\n    }\n    \n    greet() {\n        return `Hello, ${this.name}!`;\n    }\n}",
                        "source": "simulated"
                    }
                ]
        else:
            logger.info(f"Searching for {query} in all languages")
            
            # Simulated results for any language
            results = [
                {
                    "title": "Example Python function",
                    "code": "def example_function(param1, param2):\n    \"\"\"Example function\"\"\"\n    return param1 + param2",
                    "language": "python",
                    "source": "simulated"
                },
                {
                    "title": "Example JavaScript function",
                    "code": "function exampleFunction(param1, param2) {\n    // Example function\n    return param1 + param2;\n}",
                    "language": "javascript",
                    "source": "simulated"
                }
            ]
            
        return {
            "query": query,
            "language": language,
            "results": results
        }
    
    @staticmethod
    def analyze_code(code: str, language: str = "python") -> Dict[str, Any]:
        """
        Analyze code for potential issues
        
        Args:
            code: The code to analyze
            language: The programming language
            
        Returns:
            Dictionary with analysis results
        """
        result = {
            "issues": [],
            "suggestions": [],
            "complexity": "low"
        }
        
        try:
            if language.lower() == "python":
                # Create a temporary file
                temp_file = "/tmp/pocket_ai_temp.py"
                with open(temp_file, "w") as f:
                    f.write(code)
                
                # Run pylint for static analysis
                process = subprocess.Popen(
                    ["pylint", "--disable=all", "--enable=E,F", temp_file],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                
                stdout, stderr = process.communicate()
                
                # Parse pylint output
                if stdout:
                    for line in stdout.split("\n"):
                        if line.strip():
                            result["issues"].append(line.strip())
                
                # Clean up
                os.remove(temp_file)
                
                # Add some simulated suggestions
                result["suggestions"] = [
                    "Consider adding docstrings to functions",
                    "Use type hints for better code readability",
                    "Follow PEP 8 style guidelines"
                ]
                
            elif language.lower() == "javascript":
                # Create a temporary file
                temp_file = "/tmp/pocket_ai_temp.js"
                with open(temp_file, "w") as f:
                    f.write(code)
                
                # In a real implementation, you would use ESLint or similar
                # For now, we'll return simulated results
                
                # Clean up
                os.remove(temp_file)
                
                # Add some simulated issues and suggestions
                result["issues"] = [
                    "Missing semicolons",
                    "Unused variables"
                ]
                
                result["suggestions"] = [
                    "Use const/let instead of var",
                    "Add JSDoc comments for functions",
                    "Follow a consistent code style"
                ]
                
            else:
                result["issues"] = [f"Unsupported language: {language}"]
                
        except Exception as e:
            result["issues"].append(str(e))
            
        return result