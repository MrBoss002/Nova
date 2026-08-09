<div align="center">

  <h1>🤖 Nova - Multi-Group Telegram AI Bot</h1>
  <p>An intelligent Python Telegram bot built with aiogram 3, Google Gemini AI, and MongoDB. Supports natural DM conversations, group mentions, automatic channel post commentary, and interactive mini-games.</p>

### 🚀 One-Click Deploy

  <p>
    <a href="https://app.koyeb.com/deploy?type=git&repository=github.com/MrBoss002/Nova&branch=main">
      <img src="https://img.shields.io/badge/Deploy%20to-Koyeb-121019?style=for-the-badge&logo=koyeb&logoColor=white" alt="Deploy to Koyeb" height="32">
    </a>
    <a href="https://render.com/deploy?repo=https://github.com/MrBoss002/Nova">
      <img src="https://img.shields.io/badge/Deploy%20to-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white" alt="Deploy to Render" height="32">
    </a>
    <a href="https://heroku.com/deploy?template=https://github.com/MrBoss002/Nova">
      <img src="https://img.shields.io/badge/Deploy%20to-Heroku-430090?style=for-the-badge&logo=heroku&logoColor=white" alt="Deploy to Heroku" height="32">
    </a>
  </p>

  <p>
    <a href="https://github.com/MrBoss002/Nova/stargazers"><img src="https://img.shields.io/github/stars/MrBoss002/Nova?style=for-the-badge&color=0088CC" alt="Stars"/></a>
    <a href="https://github.com/MrBoss002/Nova/network/members"><img src="https://img.shields.io/github/forks/MrBoss002/Nova?style=for-the-badge&color=0088CC" alt="Forks"/></a>
    <a href="https://github.com/MrBoss002/Nova/issues"><img src="https://img.shields.io/github/issues/MrBoss002/Nova?style=for-the-badge&color=0088CC" alt="Issues"/></a>
  </p>

</div>

---

## ✨ Features

- 📰 **Channel Auto-Reply:** Detects automatic forwards from linked Telegram channels and posts a relevant AI response.
- 🎮 **Mini-Games & Polls:** Play Trivia and Word Scramble via `/game` or create interactive group polls with `/poll`.
- 💬 **Private DMs & Group Smart Replies:** Responds to all DM messages and activates in groups via mentions or direct replies.
- 🧠 **MongoDB Context Memory:** Remembers recent chat history per group/user for continuous conversations.
- 📢 **Admin Broadcast:** Reply-to broadcast system for broadcasting text and rich media to users.

---

## 🛠️ Tech Stack & Dependencies

- **Language:** Python 3.10+
- **Framework:** `aiogram 3`
- **Database:** MongoDB Atlas (`motor`)
- **AI Engine:** `google-generativeai`

---

## ⚙️ Environment Variables

Create a `.env` file in the root directory:

```env
BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN
MONGO_URI=YOUR_MONGODB_URI
GEMINI_API_KEY=YOUR_FREE_GEMINI_API_KEY
ADMIN_ID=YOUR_TELEGRAM_USER_ID
```

---

## 🚀 Getting Started Locally

### 1. Clone the Repository
```
git clone [https://github.com/MrBoss002/Nova.git](https://github.com/MrBoss002/Nova.git)
cd Nova
```
### 2. Install Dependencies
```
pip install -r requirements.txt
```
### 3. Run the Bot
```
python bot.py
```

---

## 🎮 Bot Commands

| Command | Permission | Description |
| :--- | :---: | :--- |
| ` /start ` | 🌐 **Public** | Starts the bot and displays the main welcome menu. |
| ` /game ` | 🌐 **Public** | Opens the interactive mini-game menu (Trivia & Scramble). |
| ` /poll ` | 🌐 **Public** | Generates an interactive opinion poll in the chat. |
| ` /clear ` | 🌐 **Public** | Clears Nova's conversation context memory for the chat. |
| ` /stats ` | 👑 **Admin Only** | Displays total registered bot user count. |
| ` /broadcast ` | 👑 **Admin Only** | Reply to any message/media to broadcast it to all bot users. |

---

<div align="center">

  <h2>📬 Developer Space</h2>

  <p>Need help, want to report a bug, or connect with the developer?</p>

  <p>
    <a href="https://t.me/MrBoss002">
      <img src="https://img.shields.io/badge/💬%20Help%20%26%20Feedback-Contact%20Admin-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Help and Feedback"/>
    </a>
    <a href="https://sites.google.com/view/zerotwo-onlinestore">
      <img src="https://img.shields.io/badge/🛍️%20ZeroTwo%20Store-Catalog-107C41?style=for-the-badge&logo=google-chrome&logoColor=white" alt="ZeroTwo Store"/>
    </a>
  </p>

  <br/>

  <p>Developed with ❤️ by <b>Muhammad Riswan C</b> (<a href="https://github.com/MrBoss002">@MrBoss002</a>)</p>

</div>
