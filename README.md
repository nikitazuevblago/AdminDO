# AdminDO Bot

A Telegram bot for managing DigitalOcean droplets through a convenient chat interface.

## Features

- Execute console commands on your droplet directly from Telegram
- Interactive console mode with command history
- Secure authentication using environment variables
- Strict access control with Telegram user ID verification
- Docker support for easy deployment

## Setup

### Option 1: Local Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:
   - Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - Linux/MacOS:
     ```bash
     source .venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file with your configuration:
   ```env
   BOT_TOKEN=your_telegram_bot_token
   DO_TOKEN=your_digitalocean_api_token
   SSH_USER=root
   DROPLET_NAME=your_droplet_name
   ```

6. Update the `AUTHORIZED_ID` in `bot.py` with your Telegram user ID

7. Run the bot:
   ```bash
   python bot.py
   ```

### Option 2: Docker Setup

1. Build the Docker image:
   ```bash
   docker build -t admindo-bot .
   ```

2. Create a `.env` file as described above

3. Run the container:
   ```bash
   docker run --env-file .env admindo-bot
   ```

## Commands

- `/help` - Show available commands
- `/console` - Enter console mode to execute commands
- `/cancel` - Exit console mode

## Security

- The bot uses environment variables for sensitive data
- SSH password authentication for droplet access
- Command execution is limited to a single authorized Telegram user ID
- All other users receive "Access denied" message

## Files

- `bot.py` - Main bot implementation
- `droplet_manager.py` - DigitalOcean API and SSH functionality
- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker container configuration
- `.dockerignore` - Docker build exclusions 