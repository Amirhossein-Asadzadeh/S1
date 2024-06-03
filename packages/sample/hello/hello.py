import logging
import os
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = "7149467380:AAG7_UN-t0xLYztX4J1EwsAP1DS8eOqacxA"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm your IP-finding bot! I'll scan group messages for IP addresses.")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Just add me to your group, and I'll automatically find and report IP addresses in messages."
    )

# Message handler (modified for groups)
async def find_ip_in_groups(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type in ["group", "supergroup"]:  # Check if it's a group message
        text = update.message.text
        ip_pattern = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"  # IP address pattern
        ip_addresses = re.findall(ip_pattern, text)

        for ip in ip_addresses:
            response = f"`{ip}`"
            await context.bot.send_message(chat_id=update.effective_chat.id, text=response, parse_mode="MarkdownV2", reply_to_message_id=update.message.message_id)  # Reply to the original message

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error("Update %s caused error %s", update, context.error)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    # Add command handlers (no changes here)
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help))

    # Add the modified message handler for groups
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), find_ip_in_groups))

    # Error handler (no changes here)
    application.add_handler(MessageHandler(filters.ALL, error))

    application.run_polling()
