from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, constants
from telegram.ext import Application, CallbackQueryHandler , ContextTypes, CommandHandler
# from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio
from dotenv import load_dotenv
import os

# wiki
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/InlineKeyboard-Example
# https://docs.python-telegram-bot.org/en/latest/examples.inlinekeyboard.html

load_dotenv()
token = os.getenv('token')
chat_id = os.getenv('chat_id')


async def go(update: Update, context: ContextTypes.DEFAULT_TYPE):
  
# 先创建 Button 对象，再创建 Markup 对象
  keyboard = [
    [InlineKeyboardButton(text = '测试按钮', callback_data="this is callback_data")]
    ]
  markup = InlineKeyboardMarkup(keyboard)
  
  await update.message.reply_text('reply_message', reply_markup = markup)

# async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#   print('this is callback')
  
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"Selected option: {query.data} + 1")

base_url = 'https://etherscan.io/address/'
address = '0xdb767e9626a543BB9b61964421BFA4512185469b'

# asyncio.run(send_msg(f'''
# 代币创建信息\n
# Pair: <a href="{base_url}+{address}">{address}</a>\n#Address'''))
application = Application.builder().token(token).build()
application.add_handler(CommandHandler("go", go))
application.add_handler(CallbackQueryHandler(button))
application.run_polling(allowed_updates=Update.ALL_TYPES)