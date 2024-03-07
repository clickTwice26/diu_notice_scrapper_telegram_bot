import asyncio
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from junky import *

TOKEN: Final = open("/home/giyan/Desktop/noticebot_token", "r").read().strip()
BOT_USERNAME = "@diu_notice_bot"

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hi! I am a bot to get diu notices')

# Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()
    if 'hello' in processed:
        return "Hello World!"
    if "notice" in processed:
        return notice_scrapper()
        # return "notice fetched successfully"
    else:
        return "Unknown command given"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    print(f"User: {update.message.chat.id}| Message: {text} | type: {message_type}")

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    else:
        response: str = handle_response(text)
    print("Bot", response)
    # await context.bot.send_message(response=response, chat_id=update.message.chat.id)
    await update.message.reply_text(response, parse_mode='html')

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update: {update} caused error {context.error}")

async def send_certain_response(chat_id: int, bot):
    while True:
        response = handle_response("notice")
        await asyncio.sleep(3)  # 1800 seconds = 30 minutes
        await bot.send_message(chat_id=chat_id, text=response, parse_mode='html')

if __name__ == "__main__":
    print("Program is starting")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    ## errors
    app.add_error_handler(error)


    loop = asyncio.get_event_loop()
    loop.create_task(send_certain_response(-4195586623, app.bot))

    print("Program is polling...")
    app.run_polling(poll_interval=1)