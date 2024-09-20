from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, constants
from telegram.ext import Application, CallbackQueryHandler , ContextTypes, CommandHandler
# from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio
from dotenv import load_dotenv
import os
from dexscreener import Dex

# wiki
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/InlineKeyboard-Example
# https://docs.python-telegram-bot.org/en/latest/examples.inlinekeyboard.html

load_dotenv()
token = os.getenv('token')
chat_id = os.getenv('chat_id')

# maga pair addr: 0xE4b8583cCB95b25737C016ac88E539D0605949e8

async def go(update: Update, context: ContextTypes.DEFAULT_TYPE):
  
# 先创建 Button 对象，再创建 Markup 对象
  keyboard = [
    [InlineKeyboardButton(text = '测试按钮', callback_data="0xE4b8583cCB95b25737C016ac88E539D0605949e8")]
    ]
  markup = InlineKeyboardMarkup(keyboard)
  
  await update.message.reply_text('reply_message', reply_markup = markup)

# async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#   print('this is callback')

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #  CallbackQuery object represents an incoming callback query from a callback button in an inline keyboard.
    query = update.callback_query
    info = Dex.get_pair_info(query.data)
    # await query.edit_message_text(text=f"Selected option: {query.data} + 1")
    await query.get_bot().send_message(text = info, chat_id = chat_id)

base_url = 'https://etherscan.io/address/'
address = '0xdb767e9626a543BB9b61964421BFA4512185469b'

# asyncio.run(send_msg(f'''
# 代币创建信息\n
# Pair: <a href="{base_url}+{address}">{address}</a>\n#Address'''))
application = Application.builder().token(token).build()
application.add_handler(CommandHandler("go", go))
application.add_handler(CallbackQueryHandler(button))
application.run_polling(allowed_updates=Update.ALL_TYPES)