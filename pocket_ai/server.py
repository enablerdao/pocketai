"""
Web server for ポケットAI (Pocket AI)
"""

import os
import json
from typing import Dict, Any, List, Optional

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from .agent.agent import PocketAI
from .config import get_config
from .utils.logger import get_logger

logger = get_logger(__name__)

# Create Flask app
app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)  # Enable CORS for all routes

# Create ポケットAI instance
pocket_ai = None

@app.route("/")
def index():
    """Render the index page"""
    return render_template("index.html")

@app.route("/api/run", methods=["POST"])
def run_agent():
    """Run the agent with a task"""
    global pocket_ai
    
    # Get request data
    data = request.json
    task = data.get("task", "")
    context = data.get("context", {})
    api_key = data.get("api_key", "")
    
    # Validate input
    if not task:
        return jsonify({"error": "No task provided"}), 400
    
    # Initialize ポケットAI if needed
    if pocket_ai is None or api_key:
        pocket_ai = PocketAI(api_key=api_key)
    
    try:
        # Run the agent
        result = pocket_ai.run(task, initial_context=context)
        
        return jsonify({
            "success": True,
            "result": result
        })
    except Exception as e:
        logger.error(f"Error running agent: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route("/api/execute_code", methods=["POST"])
def execute_code():
    """Execute code"""
    global pocket_ai
    
    # Get request data
    data = request.json
    code = data.get("code", "")
    language = data.get("language", "python")
    
    # Validate input
    if not code:
        return jsonify({"error": "No code provided"}), 400
    
    # Initialize ポケットAI if needed
    if pocket_ai is None:
        pocket_ai = PocketAI()
    
    try:
        # Execute code
        result = pocket_ai.programming_tools.execute_code(code, language)
        
        return jsonify({
            "success": True,
            "result": result
        })
    except Exception as e:
        logger.error(f"Error executing code: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

def create_app():
    """Create and configure the Flask app"""
    return app

def run_server():
    """Run the server"""
    host = get_config("server.host")
    port = get_config("server.port")
    
    logger.info(f"Starting ポケットAI server on {host}:{port}")
    app.run(host=host, port=port, debug=True)

if __name__ == "__main__":
    run_server()