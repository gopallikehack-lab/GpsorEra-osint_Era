#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
🔥 ELECTRON OSINT BOT — PREMIUM NUMBER INFO
👑 Owner: @GpsirEra
📢 Channel: https://t.me/+0w8ATlAukVA1MWU1
⚡ Vercel Serverless | FIXED WEBHOOK
"""

import os
import json
import requests
from datetime import datetime
from fastapi import FastAPI, Request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)
from telegram.constants import ParseMode

# ============ CONFIG ============
TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
API_URL = os.environ.get("API_URL", "https://electron-cursed.vercel.app/lookup")
API_KEY = os.environ.get("API_KEY", "@GpsirEra")
OWNER_ID = int(os.environ.get("OWNER_ID", "123456789"))
CHANNEL_LINK = os.environ.get("CHANNEL_LINK", "https://t.me/+0w8ATlAukVA1MWU1")
OWNER_USERNAME = "@GpsirEra"
BOT_NAME = "Electron OSINT Bot"

# ============ PREMIUM EMOJI IDs ============
EMOJIS = {
    "computer": "5260382369688333746",
    "thinking": "5843618080713874142",
    "skull": "5422636707893762950",
    "laptop": "5350478083340122287",
    "woman_tech": "5301083932211550593",
    "cloud": "5339052439540606093",
    "ninja": "6292081815389735688",
    "warning": "5199950783969255534",
    "cool": "5249380218254151868",
    "crossed_swords": "5276294450425902729",
    "ninja2": "5240415835528383591",
    "eyes": "6140757035081271294"
}

def premium_emoji(key):
    eid = EMOJIS.get(key, "")
    if eid:
        return f'<tg-emoji emoji-id="{eid}">✨</tg-emoji>'
    return "✨"

# ============ FASTAPI APP ============
app = FastAPI()
bot_app = None

# ============ API FUNCTION ============
def lookup_number(phone: str) -> dict:
    url = f"{API_URL}?mobile={phone}&key={API_KEY}"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            return response.json()
        return {"status": "error", "message": f"API Error: {response.status_code}"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# ============ FORMAT RESULT ============
def format_result(data: dict) -> str:
    if data.get("status") != "success":
        return f"""
{premium_emoji('warning')} *ERROR*

❌ {data.get('message', 'Unknown error')}

Please check the number and try again.
        """
    
    target = data.get("target", "Unknown")
    info = data.get("data", [])
    
    if not info:
        return f"""
{premium_emoji('thinking')} *NO DATA FOUND*

📱 Number: `{target}`

No information found for this number.
        """
    
    result = info[0]
    
    lines = []
    lines.append(f"{premium_emoji('eyes')} *🔍 OSINT RESULT* {premium_emoji('crossed_swords')}")
    lines.append("")
    lines.append(f"📱 *Number:* `{result.get('phoneNumber', 'N/A')}`")
    lines.append("")
    lines.append(f"👤 *Name:* `{result.get('name', 'N/A')}`")
    lines.append(f"👨 *Father's Name:* `{result.get('fathersName', 'N/A')}`")
    lines.append("")
    lines.append(f"🆔 *Aadhar Number:* `{result.get('aadharNumber', 'N/A')}`")
    lines.append(f"📞 *Other Number:* `{result.get('otherNumber', 'N/A')}`")
    lines.append("")
    lines.append(f"📍 *Address:*")
    address = result.get('address', 'N/A')
    for line in address.split('!'):
        if line.strip():
            lines.append(f"   • {line.strip()}")
    lines.append("")
    lines.append(f"🏙️ *District:* `{result.get('district', 'N/A')}`")
    lines.append(f"📍 *State:* `{result.get('state', 'N/A')}`")
    lines.append(f"📮 *Pincode:* `{result.get('pincode', 'N/A')}`")
    lines.append(f"🏘️ *Town:* `{result.get('town', 'N/A')}`")
    lines.append("")
    lines.append(f"🔗 *Source:* @GpsirEra")
    lines.append(f"📢 *Channel:* {CHANNEL_LINK}")
    lines.append("")
    lines.append(f"{premium_emoji('warning')} *Disclaimer:* Data may not be 100% accurate. Use responsibly.")
    
    return "\n".join(lines)

# ============ TELEGRAM HANDLERS ============
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    welcome = f"""
{premium_emoji('ninja')} *WELCOME TO {BOT_NAME}* {premium_emoji('cool')}

Hi {user.first_name}! {premium_emoji('computer')}

I'm a premium OSINT bot that fetches detailed information from any Indian phone number.

{premium_emoji('cloud')} *What I can find:*
• Full Name
• Father's Name
• Aadhar Number
• Address (Complete)
• District, State, Pincode
• Other Phone Numbers

{premium_emoji('crossed_swords')} *Commands:*
/lookup `<number>` — Lookup any number
/example — See a demo result
/help — Help & commands
/about — About this bot
/premium — Premium info

{premium_emoji('warning')} *⚠️ Important:*
Join our channel before using!
{CHANNEL_LINK}

👑 *Owner:* {OWNER_USERNAME}
    """
    
    keyboard = [
        [InlineKeyboardButton(f"{premium_emoji('computer')} Lookup Number", callback_data="lookup")],
        [InlineKeyboardButton(f"{premium_emoji('eyes')} View Example", callback_data="example")],
        [InlineKeyboardButton(f"{premium_emoji('warning')} Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton(f"{premium_emoji('skull')} About", callback_data="about")]
    ]
    
    await update.message.reply_text(
        welcome,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def lookup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text(
            f"{premium_emoji('warning')} *Usage:* `/lookup <phone_number>`\n\n"
            f"Example: `/lookup 9035622887`",
            parse_mode=ParseMode.HTML
        )
        return
    
    phone = args[0].strip()
    if not phone.isdigit() or len(phone) < 10:
        await update.message.reply_text(
            f"{premium_emoji('warning')} *Invalid Number!*\n\n"
            f"Please enter a valid 10-digit phone number.",
            parse_mode=ParseMode.HTML
        )
        return
    
    msg = await update.message.reply_text(
        f"{premium_emoji('thinking')} *Fetching data for:* `{phone}`\n"
        f"Please wait... {premium_emoji('cloud')}",
        parse_mode=ParseMode.HTML
    )
    
    result = lookup_number(phone)
    formatted = format_result(result)
    
    await msg.edit_text(formatted, parse_mode=ParseMode.HTML)

async def example_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    example_data = {
        "status": "success",
        "target": "9035622887",
        "data": [{
            "name": "Mohammed Sameer",
            "fathersName": "Mohammed Zameer",
            "phoneNumber": "9035622887",
            "aadharNumber": "809507473757",
            "otherNumber": "9632788131",
            "address": "!7-920/3A!Mijgori Road!Naya Mohalla Gulbarga Gulbarga!Siddiqui Masjid!Kalaburagi!KALABURAGI!Karnataka!585104",
            "district": "Kalaburagi",
            "state": "Karnataka",
            "pincode": "585104",
            "town": "Kalaburagi"
        }]
    }
    
    formatted = format_result(example_data)
    
    note = f"""
{premium_emoji('eyes')} *📌 EXAMPLE RESULT*

{formatted}

---
📱 *Try it yourself:* `/lookup 9035622887`
    """
    
    await update.message.reply_text(note, parse_mode=ParseMode.HTML)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = f"""
{premium_emoji('ninja2')} *HELP & COMMANDS* {premium_emoji('crossed_swords')}

📌 *Commands:*

/lookup `<number>` — Get info about a phone number
/example — See a demo result
/help — Show this help
/about — About the bot
/premium — Premium features
/start — Welcome menu

📌 *How to use:*

1️⃣ Join our channel first:
{CHANNEL_LINK}

2️⃣ Use the /lookup command:
`/lookup 9035622887`

3️⃣ Get detailed information:
• Name & Father's Name
• Aadhar Number
• Full Address
• District, State, Pincode
• Other Phone Numbers

{premium_emoji('warning')} *Disclaimer:*
This bot uses public data sources. Use responsibly.

👑 *Owner:* {OWNER_USERNAME}
📢 *Channel:* {CHANNEL_LINK}
    """
    
    keyboard = [
        [InlineKeyboardButton(f"{premium_emoji('computer')} Try Now", callback_data="lookup")],
        [InlineKeyboardButton(f"{premium_emoji('warning')} Join Channel", url=CHANNEL_LINK)]
    ]
    
    await update.message.reply_text(
        help_text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    about = f"""
{premium_emoji('ninja')} *ABOUT {BOT_NAME}* {premium_emoji('cool')}

{premium_emoji('cloud')} *Version:* 2.0 Premium
{premium_emoji('computer')} *Platform:* Telegram Bot
{premium_emoji('crossed_swords')} *Type:* OSINT Number Lookup

{premium_emoji('eyes')} *Features:*
• Unlimited free searches
• Detailed personal info
• Aadhar number lookup
• Full address with location
• District, State, Pincode
• Other associated numbers

{premium_emoji('warning')} *Data Source:* Public databases
{premium_emoji('skull')} *Usage:* Personal & educational only

👑 *Owner:* {OWNER_USERNAME}
📢 *Channel:* {CHANNEL_LINK}
🔗 *API:* @ElectronCursed → @GpsirEra
    """
    
    await update.message.reply_text(about, parse_mode=ParseMode.HTML)

async def premium_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    premium = f"""
{premium_emoji('skull')} *🔥 PREMIUM FEATURES* {premium_emoji('ninja')}

{premium_emoji('computer')} *What you get:*
• Unlimited number lookups
• Full personal details
• Aadhar verification
• Address with location
• Associated numbers
• Fast API response

{premium_emoji('crossed_swords')} *Status:* FREE for all members!

{premium_emoji('warning')} *To Use:*
1️⃣ Join our channel
2️⃣ Use /lookup command
3️⃣ Get instant results

{premium_emoji('eyes')} *Example:*
`/lookup 9035622887`

👑 *Owner:* {OWNER_USERNAME}
📢 *Channel:* {CHANNEL_LINK}
    """
    
    keyboard = [
        [InlineKeyboardButton(f"{premium_emoji('warning')} Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton(f"{premium_emoji('computer')} Try Lookup", callback_data="lookup")]
    ]
    
    await update.message.reply_text(
        premium,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    if text.isdigit() and len(text) >= 10:
        msg = await update.message.reply_text(
            f"{premium_emoji('thinking')} *Fetching data for:* `{text}`\n"
            f"Please wait... {premium_emoji('cloud')}",
            parse_mode=ParseMode.HTML
        )
        
        result = lookup_number(text)
        formatted = format_result(result)
        await msg.edit_text(formatted, parse_mode=ParseMode.HTML)
    else:
        await update.message.reply_text(
            f"{premium_emoji('warning')} *Invalid input*\n\n"
            f"Send a 10-digit phone number, or use:\n"
            f"`/lookup <number>`\n\n"
            f"Example: `/lookup 9035622887`",
            parse_mode=ParseMode.HTML
        )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "lookup":
        await query.message.reply_text(
            f"{premium_emoji('computer')} *Enter phone number:*\n\n"
            f"Send a 10-digit number like: `9035622887`\n"
            f"Or use: `/lookup 9035622887`",
            parse_mode=ParseMode.HTML
        )
    
    elif data == "example":
        example_data = {
            "status": "success",
            "target": "9035622887",
            "data": [{
                "name": "Mohammed Sameer",
                "fathersName": "Mohammed Zameer",
                "phoneNumber": "9035622887",
                "aadharNumber": "809507473757",
                "otherNumber": "9632788131",
                "address": "!7-920/3A!Mijgori Road!Naya Mohalla Gulbarga Gulbarga!Siddiqui Masjid!Kalaburagi!KALABURAGI!Karnataka!585104",
                "district": "Kalaburagi",
                "state": "Karnataka",
                "pincode": "585104",
                "town": "Kalaburagi"
            }]
        }
        formatted = format_result(example_data)
        await query.message.reply_text(
            f"{premium_emoji('eyes')} *📌 EXAMPLE RESULT*\n\n{formatted}",
            parse_mode=ParseMode.HTML
        )
    
    elif data == "about":
        about = f"""
{premium_emoji('ninja')} *ABOUT {BOT_NAME}* {premium_emoji('cool')}

Version: 2.0 Premium
Type: OSINT Number Lookup
Data: Public databases

👑 Owner: @GpsirEra
📢 Channel: {CHANNEL_LINK}
        """
        await query.message.reply_text(about, parse_mode=ParseMode.HTML)

# ============ VERCEL WEBHOOK ============
@app.on_event("startup")
async def startup():
    global bot_app
    
    # Initialize bot application
    bot_app = Application.builder().token(TOKEN).build()
    
    # Add handlers
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CommandHandler("lookup", lookup_command))
    bot_app.add_handler(CommandHandler("example", example_command))
    bot_app.add_handler(CommandHandler("help", help_command))
    bot_app.add_handler(CommandHandler("about", about_command))
    bot_app.add_handler(CommandHandler("premium", premium_command))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    bot_app.add_handler(CallbackQueryHandler(button_callback))
    
    # Set webhook
    webhook_url = os.environ.get("WEBHOOK_URL", "https://gpsor-era-osint-era-snowy.vercel.app/webhook")
    await bot_app.bot.set_webhook(webhook_url)
    print(f"✅ Bot initialized. Webhook: {webhook_url}")

@app.post("/webhook")
async def webhook(request: Request):
    global bot_app
    
    if bot_app is None:
        return {"status": "error", "message": "Bot not initialized"}
    
    try:
        data = await request.json()
        update = Update.de_json(data, bot_app.bot)
        await bot_app.process_update(update)
        return {"status": "ok"}
    except Exception as e:
        print(f"Webhook error: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/webhook")
async def webhook_get():
    return {
        "status": "ok",
        "message": "Webhook endpoint is active. Use POST for Telegram updates.",
        "docs": "https://core.telegram.org/bots/api#setwebhook"
    }

@app.get("/")
async def root():
    return {
        "name": "Electron OSINT Bot",
        "version": "2.0",
        "owner": "@GpsirEra",
        "channel": "https://t.me/+0w8ATlAukVA1MWU1",
        "status": "✅ Running"
    }

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "bot": "Electron OSINT Bot"
    }
