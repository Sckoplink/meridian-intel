#!/usr/bin/env python3
"""
📧 Meridian Inbox Monitor
Checks all AI Sckop email inboxes every hour via IMAP.
Sends Telegram alerts for new unread emails.
"""

import imaplib
import os
import requests
from datetime import datetime

# ─── CONFIG ───
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT = os.getenv("TELEGRAM_CHAT_ID", "")

EMAILS = {
    "ai": {
        "email": "ai@aisckop.co.uk",
        "pass": os.getenv("AI_EMAIL_PASS", ""),
        "server": "imap.hostinger.com",
        "port": 993
    },
    "hello": {
        "email": "hello@aisckop.co.uk",
        "pass": os.getenv("HELLO_EMAIL_PASS", ""),
        "server": "imap.hostinger.com",
        "port": 993
    },
    "gov": {
        "email": "gov@aisckop.com",
        "pass": os.getenv("GOV_EMAIL_PASS", ""),
        "server": "imap.hostinger.com",
        "port": 993
    },
    "investors": {
        "email": "investors@aisckop.co.uk",
        "pass": os.getenv("INVESTORS_EMAIL_PASS", ""),
        "server": "imap.hostinger.com",
        "port": 993
    },
    "grants": {
        "email": "grants@aisckop.co.uk",
        "pass": os.getenv("GRANTS_EMAIL_PASS", ""),
        "server": "imap.hostinger.com",
        "port": 993
    }
}

def telegram(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT:
        print(f"[SKIP] {message[:80]}...")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        r = requests.post(url, json=payload, timeout=30)
        print(f"Telegram: {r.status_code}")
    except Exception as e:
        print(f"Telegram error: {e}")

def check_inbox(alias, cfg):
    """Check a single inbox and return unread count + latest emails."""
    if not cfg["pass"]:
        return {"unread": 0, "error": "No password"}
    
    try:
        mail = imaplib.IMAP4_SSL(cfg["server"], cfg["port"])
        mail.login(cfg["email"], cfg["pass"])
        mail.select("inbox")
        
        _, search_data = mail.search(None, "UNSEEN")
        unread_ids = search_data[0].split()
        unread_count = len(unread_ids)
        
        latest = []
        for eid in unread_ids[:3]:  # Top 3
            _, data = mail.fetch(eid, "(RFC822)")
            raw = data[0][1]
            import email
            msg = email.message_from_bytes(raw)
            subject = msg.get("Subject", "No Subject")[:60]
            from_addr = msg.get("From", "Unknown")[:60]
            latest.append(f"• {from_addr}: {subject}")
        
        mail.close()
        mail.logout()
        
        return {
            "unread": unread_count,
            "latest": latest
        }
    except Exception as e:
        return {"unread": 0, "error": str(e)}

def main():
    print(f"📧 Meridian Inbox Check — {datetime.now().strftime('%H:%M UTC')}")
    
    results = []
    total_unread = 0
    
    for alias, cfg in EMAILS.items():
        result = check_inbox(alias, cfg)
        results.append({
            "alias": alias,
            "email": cfg["email"],
            **result
        })
        total_unread += result.get("unread", 0)
        print(f"  {cfg['email']}: {result.get('unread', 0)} unread")
    
    # Only send Telegram if there are new emails
    if total_unread > 0:
        lines = [f"📧 <b>MERIDIAN INBOX ALERT</b>\n<b>{total_unread} unread emails</b>\n"]
        for r in results:
            if r.get("unread", 0) > 0:
                lines.append(f"\n<b>{r['email']}</b>: {r['unread']} unread")
                for latest in r.get("latest", [])[:2]:
                    lines.append(latest)
        
        lines.append(f"\n🫡 Meridian Inbox Monitor\n{datetime.now().strftime('%H:%M UTC')}")
        telegram("\n".join(lines))
    else:
        print("  No unread emails — no Telegram alert sent")
    
    print("✅ Inbox check complete!")

if __name__ == "__main__":
    main()
