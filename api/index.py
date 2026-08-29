import os
import json
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from bot import start, lookup_command, handle_message, help_command, button_callback

BOT_TOKEN = os.getenv("BOT_TOKEN")

def webhook(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            update = Update.de_json(data, None)
            
            app = Application.builder().token(BOT_TOKEN).build()
            app.add_handler(CommandHandler("start", start))
            app.add_handler(CommandHandler("lookup", lookup_command))
            app.add_handler(CommandHandler("help", help_command))
            app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
            app.add_handler(CallbackQueryHandler(button_callback))
            
            app.process_update(update)
            return {"status": "ok"}
        except Exception as e:
            return {"error": str(e)}, 500
    return {"message": "Webhook ready"}, 200

# Vercel entry point
handler = webhook    
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
