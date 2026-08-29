#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OSINT BOT — Number Info
Developer: @GpsirEra
"""

import os
import re
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ========== CONFIG ==========
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = "https://electron-cursed.vercel.app/lookup"
API_KEY = "@ElectronCursed"
CHANNEL_LINK = "https://t.me/+0w8ATlAukVA1MWU1"
OWNER_ID = 8932695749

# ========== PREMIUM EMOJI IDs (HTML) ==========
EMOJI = {
    "devil": "5422636707893762950",
    "computer": "5350478083340122287",
    "ninja": "6292081815389735688",
    "warning": "5199950783969255534",
    "cool": "5249380218254151868",
    "sword": "5276294450425902729",
    "eyes": "6140757035081271294",
    "cloud": "5339052439540606093",
    "woman_coder": "5301083932211550593",
}

def pe(key, fallback="•"):
    return f'<tg-emoji emoji-id="{EMOJI.get(key, "")}">{fallback}</tg-emoji>'

# ========== HELPERS ==========
def lookup_number(number):
    try:
        url = f"{API_URL}?mobile={number}&key={API_KEY}"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success" and data.get("data"):
                return data["data"][0]
        return None
    except:
        return None

def format_result(data):
    if not data:
        return None
    return f"""
{pe('devil')} *OSINT RESULT* {pe('devil')}

{pe('computer')} *Number:* `{data.get('phoneNumber', 'N/A')}`

{pe('ninja')} *Name:* `{data.get('name', 'N/A')}`
{pe('cloud')} *Father:* `{data.get('fathersName', 'N/A')}`
{pe('eyes')} *Aadhar:* `{data.get('aadharNumber', 'N/A')}`
{pe('woman_coder')} *Other:* `{data.get('otherNumber', 'N/A')}`

{pe('sword')} *Address:*
`{data.get('address', 'N/A')}`

{pe('cool')} *Source:* @GpsirEra
"""

# ========== BOT HANDLERS ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(f"{pe('computer')} Lookup", callback_data="lookup")],
        [InlineKeyboardButton(f"{pe('ninja')} Help", callback_data="help")],
        [InlineKeyboardButton(f"{pe('sword')} Join Channel", url=CHANNEL_LINK)],
        [InlineKeyboardButton(f"{pe('devil')} Owner", url="https://t.me/GpsirEra")],
    ]
    text = f"""
{pe('devil')} *OSINT BOT — NUMBER INFO* {pe('devil')}

{pe('computer')} *Unlimited Searches*
{pe('cloud')} *Free & Fast*
{pe('ninja')} *Aadhar + Address*

📌 *Send a 10-digit number:*
`9035622887`

⚠️ *Join channel to use bot!*
    """
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="HTML")

async def lookup_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Usage: `/lookup 9035622887`", parse_mode="Markdown")
        return
    await process_lookup(update, context.args[0].strip())

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if re.match(r'^[0-9]{10}$', text):
        await process_lookup(update, text)
    else:
        await update.message.reply_text("❌ Send a valid 10-digit number.")

async def process_lookup(update, number):
    msg = await update.message.reply_text(f"{pe('cloud')} *Searching for `{number}`...*", parse_mode="HTML")
    data = lookup_number(number)
    if data:
        await msg.edit_text(format_result(data), parse_mode="HTML")
    else:
        await msg.edit_text(f"{pe('warning')} *No data found for `{number}`*", parse_mode="HTML")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""
{pe('ninja')} *HELP* {pe('ninja')}

/lookup <number> — Search
/start — Menu
/help — This

📌 *Examples:*
`/lookup 9035622887`
`9035622887`

🔗 {CHANNEL_LINK}
👨‍💻 @GpsirEra
    """
    await update.message.reply_text(text, parse_mode="HTML")

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "lookup":
        await query.edit_message_text("📱 *Send a 10-digit number.*", parse_mode="Markdown")
    elif query.data == "help":
        await help_command(update, context)

# ========== MAIN (Polling) ==========
def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("lookup", lookup_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_callback))
    print("🔥 OSINT Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
