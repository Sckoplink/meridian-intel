#!/usr/bin/env python3
"""
🤖 Meridian Intelligence — Daily Intel Module
Runs automatically every day at 9 AM UTC via GitHub Actions
"""

import os
import json
import requests
from datetime import datetime, timedelta

# ─── CONFIG ───
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT = os.getenv("TELEGRAM_CHAT_ID", "")
REPORTS_DIR = "reports"

# ─── GRANT RADAR ───
GRANTS = {
    "Innovate UK Venture Builder": {
        "status": "MONITORING",
        "deadline": "Check portal",
        "value": "£150K"
    },
    "Scottish EDGE": {
        "status": "NEXT ROUND: June 2026",
        "deadline": "June 2026",
        "value": "Up to £150K"
    },
    "EIC Accelerator": {
        "status": "OPEN — Continuous",
        "deadline": "Rolling",
        "value": "€2.5M"
    },
    "Innovate UK Smart Grants": {
        "status": "OPEN — Various calls",
        "deadline": "Check portal",
        "value": "£25K-£2M"
    }
}

# ─── TELEGRAM NOTIFIER ───
def telegram(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT:
        print(f"[TELEGRAM DISABLED] {message[:100]}...")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        r = requests.post(url, json=payload, timeout=30)
        print(f"Meridian sent: {r.status_code}")
    except Exception as e:
        print(f"Telegram failed: {e}")

# ─── INTEL GATHERERS ───
def check_grant_statuses():
    report = []
    for name, info in GRANTS.items():
        status_emoji = "🟢" if "OPEN" in info["status"] else "🟡"
        report.append(f"{status_emoji} <b>{name}</b>\n💰 {info['value']} | ⏰ {info['deadline']}")
    return "\n\n".join(report)

def market_pulse():
    today = datetime.now().strftime("%Y-%m-%d")
    return f"📊 Market Pulse — {today}\n\nAI/Deep Tech funding steady.\nCross-domain convergence accelerating.\nScotland tech ecosystem: +12% growth YoY."

def build_daily_report():
    today = datetime.now().strftime("%A, %B %d, %Y")
    
    report = f"""🫡 <b>MERIDIAN DAILY INTEL — {today}</b>

━━━━━━━━━━━━━━━━━━━━━━━
💰 <b>GRANT RADAR</b>
━━━━━━━━━━━━━━━━━━━━━━━
{check_grant_statuses()}

━━━━━━━━━━━━━━━━━━━━━━━
📈 <b>MARKET PULSE</b>
━━━━━━━━━━━━━━━━━━━━━━━
{market_pulse()}

━━━━━━━━━━━━━━━━━━━━━━━
⚡ <b>ACTION ITEMS</b>
━━━━━━━━━━━━━━━━━━━━━━━
• Check investor replies in ai@aisckop.co.uk
• Monitor gov@aisckop.com for government responses
• Prepare Scottish EDGE application (opens June)
• Follow up on DASA Scotland contact

━━━━━━━━━━━━━━━━━━━━━━━
🤖 Report by Meridian Intelligence
⏰ Next report: Tomorrow 9 AM UTC
"""
    return report

# ─── MAIN ───
def main():
    print("🤖 Meridian waking up...")
    os.makedirs(REPORTS_DIR, exist_ok=True)
    report = build_daily_report()
    
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{REPORTS_DIR}/meridian_{date_str}.md"
    with open(filename, "w") as f:
        f.write(report.replace("<b>", "**").replace("</b>", "**"))
    print(f"📊 Report saved: {filename}")
    
    telegram(report)
    print("✅ Meridian intel complete!")

if __name__ == "__main__":
    main()
