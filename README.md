# 🍥 Kakashi Sensei Bot

<div align="center">
  <h3>🎌 Your Ultimate Anime Notification Companion</h3>
  <p><em>Stay updated with the latest anime episodes automatically delivered to your Discord server!</em></p>
</div>

---

## 📖 About

**Kakashi Sensei Bot** is a sophisticated Discord bot that keeps your server updated with the latest anime releases from MyAnimeList. Named after the legendary Copy Ninja himself, this bot efficiently tracks currently airing anime and delivers beautiful notifications directly to your Discord channels.

### ✨ Key Features

- 🔄 **Automatic Updates**: Hourly checks for new anime episodes
- 📺 **Real-time Notifications**: Beautiful embed messages with anime details
- 🎯 **Smart Filtering**: Only notifies about genuinely new content
- 🌐 **Reliable Data Source**: Powered by Jikan API (MyAnimeList)
- ⚡ **Fast & Efficient**: Optimized for minimal resource usage
- 🛡️ **Professional Web Interface**: Complete with Terms of Service and Privacy Policy

## 🚀 Quick Start

### Add to Your Server
[![Invite Bot](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS4QwbkUJoui5W95abZaxCiJlyvErxYZLVSiA&usqp=CAU)](https://discord.com/oauth2/authorize?client_id=1386331041782042735&permissions=0&integration_type=0&scope=bot)

**Click on the Logo. **
### Basic Commands
```
%start          - Begin anime monitoring
%stop           - Stop anime monitoring
%status         - Check bot status
%setchanel     - Set notification channel
%test           - Test API connection
%clear          - Clear anime cache
%delete [number] - Delete bot messages
%hello          - Simple greeting
%help           - To review commands 
```

## 📋 Prerequisites

- Python 3.8 or higher
- Discord Bot Token
- Basic understanding of Discord bot hosting

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Salehin-07/Kakashi-Sensei-Bot.git
cd Kakashi-Sensei-Bot
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the root directory:
```env
DISCORD_TOKEN=your_discord_bot_token_here
```

### 4. Discord Bot Setup
1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Navigate to the "Bot" section
4. Copy the bot token and add it to your `.env` file
5. Enable necessary intents (Message Content Intent)

### 5. Run the Bot
```bash
python main.py
```

## 🌐 Web Interface

The bot includes a professional Flask web interface accessible at:
- **Homepage**: Information about the bot and features
- **Invite Page**: Direct bot invitation link
- **Terms of Service**: Legal compliance
- **Privacy Policy**: Data handling transparency

## 📁 Project Structure

```
Kakashi-Sensei-Bot/
├── main.py              # Main bot script
├── requirements.txt     # Python dependencies
├── .env                # Environment variables (create this)
├── README.md           # Project documentation
└── .gitignore          # Git ignore file
```

## 🔧 Configuration

### Bot Permissions Required
- Send Messages
- Embed Links
- Read Message History
- Use Slash Commands (optional)

### API Rate Limits
The bot respects Jikan API rate limits:
- 1 request per second
- 60 requests per minute
- Built-in retry mechanisms

## 📊 Usage Examples

### Starting Anime Monitoring
```
%start
```
Bot will begin monitoring and send notifications to the current channel.

### Setting Custom Channel
```
%setchannel
```
Use this command in the channel where you want notifications.

### Checking Status
```
%status
```
View current bot status, tracked anime count, and settings.

## 🚀 Deployment

### Render Deployment
1. Fork this repository
2. Connect your GitHub account to [Render](https://render.com)
3. Create a new Web Service
4. Set environment variables in Render dashboard
5. Deploy automatically from GitHub

### Environment Variables for Production
```env
DISCORD_TOKEN=your_production_bot_token
PYTHON_VERSION=3.9.0
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Bug Reports & Feature Requests

Please use the [GitHub Issues](https://github.com/Salehin-07/Kakashi-Sensei-Bot/issues) page to:
- Report bugs
- Request new features
- Ask questions
- Provide feedback

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/Salehin-07/Kakashi-Sensei-Bot/blob/main/LICENSE) file for details.

## 📞 Support

- **GitHub Issues**: [Report Issues](https://github.com/Salehin-07/Kakashi-Sensei-Bot/issues)
- **Discord**: Join our support server (coming soon)
- **Email**: Available through GitHub profile

## 🙏 Acknowledgments

- **Jikan API**: For providing reliable MyAnimeList data
- **Discord.py**: For the excellent Discord bot framework
- **MyAnimeList**: For comprehensive anime database
- **Render**: For reliable hosting platform

---

<div align="center">
  <p>Made with ❤️ by <a href="https://github.com/Salehin-07">Salehin-07</a></p>
  <p><em>"A true ninja never reveals all their techniques at once." - Kakashi Hatake</em></p>
</div>
