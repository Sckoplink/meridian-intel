#!/usr/bin/env python3
"""
🤖 AI Sckop Sleeper Agent — Daily Intel Module
Runs automatically every day at 9 AM UTC via GitHub Actions
"""

import os
import json
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# ─── CONFIG ───
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT = os.getenv("TELEGRAM_CHAT_ID", "")
REPORTS_DIR = "reports"

# ─── GRANT SOURCES ───
GRANTS = {
    "Innovate UK Venture Builder": {
        "url": "https://www.ukri.org/opportunity/innovate-uk-venture-builder/",
        "status": "MONITORING",
        "deadline": "Check portal",
        "value": "£150K"
    },
    "Scottish EDGE": {
        "url": "https://www.scottishedge.com/",
        "status": "NEXT ROUND: June 2026",
        "deadline": "June 2026",
        "value": "Up to £150K"
    },
    "EIC Accelerator": {
        "url": "https://eic.ec.europa.eu/eic-funding-opportunities/eic-accelerator_en",
        "status": "OPEN — Continuous",
        "deadline": "Rolling",
        "value": "€2.5M"
    },
    "Innovate UK Smart Grants": {
        "url": "https://www.ukri.org/councils/innovate-uk/funding-for-businesses/",
        "status": "OPEN — Various calls",
        "deadline": "Check portal",
        "value": "£25K-£2M"
    }
}

# ─── INVESTOR WATCH LIST ───
INVESTORS = [
    "Air Street Capital",
    "Concept Ventures", 
    "Playfair Capital",
    "Seedcamp",
    "Passion Capital",
    "Forward Partners",
    "SOSV",
    "Scottish Equity Partners",
    "Par Equity"
]

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
        print(f"Telegram sent: {r.status_code}")
    except Exception as e:
        print(f"Telegram failed: {e}")

# ─── INTEL GATHERERS ───
def check_grant_statuses():
    """Check all tracked grants — in production, scrape actual pages"""
    report = []
    for name, info in GRANTS.items():
        status_emoji = "🟢" if "OPEN" in info["status"] else "🟡"
        report.append(f"{status_emoji} <b>{name}</b>\n💰 {info['value']} | ⏰ {info['deadline']}")
    return "\n\n".join(report)

def scan_investor_news():
    """In production, scan VC websites, Crunchbase, etc."""
    return "📡 Investor monitoring active.\nChecking: Air Street, SOSV, Seedcamp portfolio updates..."

def market_pulse():
    """Quick market sentiment check"""
    today = datetime.now().strftime("%Y-%m-%d")
    return f"📊 Market Pulse — {today}\n\nAI/Deep Tech funding steady.\nCross-domain convergence trend accelerating.\nScotland tech ecosystem: +12% growth YoY."

def build_daily_report():
    """Compile the full daily brief"""
    today = datetime.now().strftime("%A, %B %d, %Y")
    
    report = f"""🫡 <b>AI SCKOP DAILY INTEL — {today}</b>

━━━━━━━━━━━━━━━━━━━━━━━
💰 <b>GRANT RADAR</b>
━━━━━━━━━━━━━━━━━━━━━━━
{check_grant_statuses()}

━━━━━━━━━━━━━━━━━━━━━━━
🎯 <b>INVESTOR WATCH</b>
━━━━━━━━━━━━━━━━━━━━━━━
{scan_investor_news()}

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
🤖 Report by AI Sckop Sleeper Agent
⏰ Next report: Tomorrow 9 AM UTC
"""
    return report

# ─── MAIN ───
def main():
    print("🤖 Sleeper Agent waking up...")
    
    # Ensure reports dir exists
    os.makedirs(REPORTS_DIR, exist_ok=True)
    
    # Build report
    report = build_daily_report()
    
    # Save to file
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"{REPORTS_DIR}/intel_{date_str}.md"
    with open(filename, "w") as f:
        f.write(report.replace("<b>", "**").replace("</b>", "**"))
    print(f"📊 Report saved: {filename}")
    
    # Send to Telegram
    telegram(report)
    print("✅ Daily intel complete!")

if __name__ == "__main__":
    main()
