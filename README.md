# 🌀 ATOMIC

**Advanced Telegram Group/Channel Reporting Tool**

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Telethon-Latest-blue.svg" alt="Telethon">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
</p>

---

## ⚠️ WARNING

```
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║   ⚠️ THIS TOOL IS FOR EDUCATIONAL PURPOSES ONLY              ║
║                                                                ║
║   • Use at your own risk                                      ║
║   • Not responsible for any account bans                      ║
║   • Telegram's TOS may be violated                            ║
║   • This is a SIDE PROJECT - not actively maintained           ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

## 📋 FEATURES

- 🔥 **Multi-Account Reporting** - Use multiple Telegram accounts simultaneously
- ⚡ **Fast Reporting** - Automated reports with configurable intervals
- 🛡️ **Proxy Support** - Add proxies to avoid rate limits
- 📊 **Statistics** - Track total reports sent
- 👥 **Multi-User Support** - Handle multiple users at once
- 🎯 **Real Telegram API** - Uses official Telethon library
- 🔄 **Rate Limit Handling** - Auto-wait and retry on blocks
- 📢 **Broadcast Messages** - Admin can broadcast to all users

---

## 🚀 QUICK SETUP

```bash
# 1. Clone the repository
git clone https://github.com/clayhackergroup/atomic.git
cd atomic

# 2. Run setup script
chmod +x setup.sh
./setup.sh

# 3. Configure credentials
# Edit accounts.json with your API credentials

# 4. Run the bot
python userbot.py
```

---

## 📝 CONFIGURATION

### Step 1: Get Telegram API Credentials

1. Go to [my.telegram.org](https://my.telegram.org)
2. Login with your phone number
3. Click "API Development"
4. Create a new application
5. Copy `api_id` and `api_hash`

### Step 2: Edit accounts.json

```json
[
  {
    "api_id": 12345678,
    "api_hash": "your_api_hash_here",
    "session": "account1"
  },
  {
    "api_id": 87654321,
    "api_hash": "your_api_hash_2",
    "session": "account2"
  }
]
```

### Step 3: (Optional) Add Proxies

Edit `proxies.json`:

```json
[
  {
    "host": "proxy_ip",
    "port": 8080,
    "user": "proxy_user",
    "pass": "proxy_pass"
  }
]
```

### Step 4: Configure config.json

```json
{
  "admin_id": 8754040441,
  "max_reports": 100,
  "interval": 3,
  "image_path": "/path/to/image.jpg",
  "rate_limit_wait": 60
}
```

---

## 💻 COMMANDS

| Command | Description |
|---------|-------------|
| `/start` | Start the bot |
| `/help` | Show help menu |
| `/report <target> <reason> [count]` | Report with single account |
| `/multi <target> <reason> [count]` | Report with multiple accounts |
| `/accounts` | List configured accounts |
| `/proxies` | List configured proxies |
| `/status` | Check bot status |
| `/stats` | View report statistics |
| `/cancel` | Cancel current operation |
| `/broadcast <message>` | Broadcast message (admin only) |

### Report Reasons

```
spam, violence, illegal, fake, adult, abuse, scam, drugs, pedo, copyright
```

---

## 📌 USAGE EXAMPLES

### Single Account Report
```
/report @groupname spam
```

### Single Account with Custom Count
```
/report @groupname spam 200
```

### Multi-Account Report (Uses ALL accounts)
```
/multi @groupname violence 500
```

---

## 🛠️ ERROR SOLUTIONS

### Error: "Cannot import name 'ReportSpamRequest'"

**Solution:** 
```bash
pip install --upgrade telethon
```

### Error: "Chat not found"

**Solution:** 
- Make sure the group username is correct
- Bot must be able to access the group
- Try using group ID instead of username

### Error: "Rate limited"

**Solution:** 
- Wait for the specified time (default 60s)
- Add more accounts in `accounts.json`
- Use proxies from `proxies.json`
- Increase `rate_limit_wait` in config.json

### Error: "api_id/api_hash is invalid"

**Solution:**
- Get fresh credentials from [my.telegram.org](https://my.telegram.org)
- Make sure there are no spaces or quotes in the values

### Error: "No accounts available"

**Solution:**
- Add at least one account in `accounts.json`
- Make sure api_id is a number (not string)

### Error: "Phone number required"

**Solution:**
- Userbot requires phone authentication
- Run `python userbot.py` and enter your phone when prompted
- Use bot token if you only want bot commands (limited features)

---

## 🏗️ HOW IT WORKS

```
┌─────────────────────────────────────────────────────────────┐
│                      ATOMIC WORKFLOW                        │
└─────────────────────────────────────────────────────────────┘

1. User sends /report or /multi command
       │
       ▼
2. Bot validates target and reason
       │
       ▼
3. Fetches entity using Telegram API
       │
       ▼
4. Sends reports via ReportSpamRequest()
   ┌────────────────────────────────────────────┐
   │  • Uses your Telegram account               │
   │  • Submits to Telegram's review system      │
   │  • Each report = 1 API call                │
   └────────────────────────────────────────────┘
       │
       ▼
5. Handles rate limits automatically
       │
       ▼
6. Sends progress updates to user
       │
       ▼
7. Completion notification
```

**Note:** Reports are submitted to Telegram's system for review. Effectiveness depends on:
- Number of unique reporters
- Severity of violation
- Previous complaints on the target

---

## 🧑‍💻 DEVELOPERS

<p align="center">

**Spidey**  |  **Mr Dark Horizon**  |  **Nalli Dev Ganag**

**Sweta**  |  **Nishat**  |  **DevX Tiwari**

</p>

---

## 📞 SUPPORT

<p align="center">
  <a href="https://t.me/mrdarkhorizon">
    <img src="https://img.shields.io/badge/Telegram-MrDarkHorizon-blue?style=flat&logo=telegram">
  </a>
  <a href="https://t.me/spideyze">
    <img src="https://img.shields.io/badge/Telegram-Spidey-blue?style=flat&logo=telegram">
  </a>
  <a href="https://t.me/h4ckerin">
    <img src="https://img.shields.io/badge/Telegram-H4cker.in-blue?style=flat&logo=telegram">
  </a>
</p>

<p align="center">
  <a href="https://instagram.com/exp1oit">
    <img src="https://img.shields.io/badge/Instagram-@exp1oit-pink?style=flat&logo=instagram">
  </a>
</p>

---

## ⚡️ DISCLAIMER

```
This tool is a SIDE PROJECT and is NOT actively maintained.

By using this tool you agree to:
• Take full responsibility for your actions
• Not hold developers liable for any consequences
• Use only for educational purposes
• Understand Telegram's TOS may be violated
```

---

## 📄 LICENSE

MIT License - See LICENSE file for details

---

<p align="center">
  <strong>⭐ Star us on GitHub if you find this useful!</strong>
</p>

<p align="center">
  Made with ❤️ by <a href="https://github.com/clayhackergroup">ClayHackerGroup</a>
</p>
