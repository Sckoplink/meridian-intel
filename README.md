# 🤖 Meridian Intelligence

**Meridian** — 24/7 autonomous intelligence layer for AI Sckop Technologies.

## What It Does

- 🌅 **Morning Brief** (9 AM daily): Market scan, grant deadlines, investor news
- 💰 **Grant Monitor**: Tracks Innovate UK, Scottish EDGE, EIC Accelerator
- 🎯 **Investor Tracker**: Monitors VC firm activity, new funds, portfolio changes
- 📊 **Weekly Report** (Sundays): Full intelligence summary

## Triggers

- **Schedule**: Daily at 9 AM UTC via GitHub Actions
- **Telegram**: Message "daily report" to @aisckop_agent_bot
- **Manual**: GitHub Actions "Run workflow" button

## Cost

£0 — GitHub Actions free tier: 2,000 minutes/month

## Setup

1. Create GitHub repo (public)
2. Push this code
3. Set secrets in Settings → Secrets → Actions:
   - `TELEGRAM_BOT_TOKEN`: Your bot token
   - `TELEGRAM_CHAT_ID`: Your chat ID
4. Done! Meridian wakes up daily automatically.

---
*Powered by AI Sckop Technologies*
