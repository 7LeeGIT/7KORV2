# 🤖 7KOR Discord Bot

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org)
[![Discord.py](https://img.shields.io/badge/Discord.py-2.0+-blue.svg)](https://discordpy.readthedocs.io/en/stable/)
[![Status](https://img.shields.io/badge/Status-Active-success.svg)](https://github.com/7LeeGIT)
[![Discord Server](https://img.shields.io/badge/Discord-Join%20Server-7289DA?logo=discord&logoColor=white)](https://discord.gg/PQaReaqK8Q)

## ✨ Features

### 🔗 Social Media Link Enhancement

- Automatically converts social media links to better embedding alternatives:
  - Twitter/X.com links → vxtwitter.com
  - Instagram links → ddinstagram.com
  - TikTok links → tnktok.com
- Messages with social media links are automatically replaced with properly embedded versions

### 📊 System Monitoring

- Real-time system status monitoring with auto-updating dashboard
- Displays various metrics including:
  - System uptime
  - Bot uptime
  - Discord API latency
  - CPU usage
  - RAM usage
  - Operating system information
- Status updates every 45 minutes
- Control panel with restart functionality for authorized users

## 🚀 Setup

### 📋 Prerequisites

- Python 3.8 or higher
- Discord.py library
- Required Python packages (install via pip):
  ```bash
  pip install discord.py python-dotenv psutil
  ```

### ⚙️ Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/7LeeGIT/7KORV2.git
   cd 7KORV2
   ```

2. Create a `.env` file based on the provided `.env.example`:

   ```
   DISCORD_BOT_TOKEN=your_bot_token_here
   LOGS_CHANNEL_ID=your_logs_channel_id
   GUILD_ID=your_guild_id
   AUTHORIZED_KOR=your_kor_user_id
   AUTHORIZED_LEE=your_lee_user_id
   ```

3. Fill in the environment variables:
   - `DISCORD_BOT_TOKEN`: Your Discord bot token from the Discord Developer Portal
   - `LOGS_CHANNEL_ID`: The channel ID where status updates will be posted
   - `GUILD_ID`: Your Discord server ID
   - `AUTHORIZED_KOR`/`AUTHORIZED_LEE`: User IDs for administrators who can use the control panel

### 🔄 Running the Bot

```bash
python main.py
```

## 📁 Project Structure

- `main.py`: Main bot initialization and event handling
- `embed.py`: Social media link conversion functionality
- `logs.py`: System monitoring and status dashboard
- `.env.example`: Template for environment variables
- `.gitignore`: Git ignore rules for the project

## 🛡️ Security

- Control panel access is restricted to authorized users
- Environment variables are used for sensitive information
- Token and sensitive IDs are not tracked in git

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 💬 Support

Discord : 7Lee
