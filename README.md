# ポケットAI (Pocket AI)

ポケットAI (Pocket AI) is a Doraemon-inspired AGI-like agent system designed to help with programming tasks. It implements an agent loop (Observe-Judge-Act-Evaluate) to create a software-based autonomous agent that excels at programming.

![Pocket AI Logo](https://via.placeholder.com/150x150.png?text=PocketAI)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/enablerdao/pocketai)
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/enablerdao/pocketai)

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

## Cloud Deployment

### Deploy to Render

1. Click the "Deploy to Render" button above
2. Connect your GitHub account
3. Set the required environment variables:
   - `ANTHROPIC_API_KEY`: Your Claude API key

### Deploy to Heroku

1. Click the "Deploy to Heroku" button above
2. Create a new Heroku app
3. Set the required environment variables:
   - `ANTHROPIC_API_KEY`: Your Claude API key

### Deploy with Docker

```bash
# Build the Docker image
docker build -t pocketai .

# Run the container
docker run -p 54656:54656 -e ANTHROPIC_API_KEY=your-api-key pocketai
```

### Deploy with Docker Compose

```bash
# Set your API key in the environment
export ANTHROPIC_API_KEY=your-api-key

# Start the services
docker-compose up -d
```

## License

MIT

## Acknowledgements

- Inspired by Doraemon, the robot cat from the future with a magical pocket
- Built with Python, Flask, Playwright, and Claude 3