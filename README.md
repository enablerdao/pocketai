# ポケットAI (Pocket AI)

ポケットAI (Pocket AI) is a Doraemon-inspired AGI-like agent system designed to help with programming tasks. It implements an agent loop (Observe-Judge-Act-Evaluate) to create a software-based autonomous agent that excels at programming.

## Features

- 🤖 Agent loop architecture for autonomous operation
- 🌐 Browser automation for web interaction
- 💻 Code execution and analysis
- 🔍 Code search capabilities
- 🧠 Powered by Claude 3.7 for intelligent reasoning

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/pocket-ai.git
cd pocket-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Playwright browsers:
```bash
playwright install
```

## Usage

### Web Interface

Start the web server:

```bash
python -m pocket_ai
```

Then open your browser and navigate to `http://localhost:54656`.

### Command Line

Run a single task:

```bash
python -m pocket_ai --api-key YOUR_API_KEY --task "Write a Python function to calculate Fibonacci numbers"
```

### Configuration

You can configure ポケットAI using command-line arguments:

- `--api-key`: Claude API key
- `--port`: Web server port
- `--host`: Web server host
- `--headless`: Run browser in headless mode
- `--task`: Run a single task and exit

## Architecture

ポケットAI is built with the following components:

1. **Agent Loop**: The core of the system, implementing the Observe-Judge-Act-Evaluate cycle
2. **LLM Manager**: Handles interactions with Claude 3.7
3. **Browser Manager**: Manages browser automation using Playwright or Selenium
4. **Programming Tools**: Tools for executing, analyzing, and searching code
5. **Web Server**: Provides a user interface for interacting with the agent

## License

MIT

## Acknowledgements

- Inspired by Doraemon, the robot cat from the future with a magical pocket
- Built with Python, Flask, Playwright, and Claude 3.7