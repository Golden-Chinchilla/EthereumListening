from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from telegram.ext import Application, CallbackQueryHandler , ContextTypes
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

# 先创建 Button 对象，再创建 Markup 对象
async def callback():
  print('callback msg')

keyboard = [
  [InlineKeyboardButton(text = '测试按钮', callback_data = callback)]
  ]

markup = InlineKeyboardMarkup(keyboard)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  print('this is callback')

async def send_msg(msg: str):
  bot = Bot(token=token)
  async with bot:
    await bot.send_message(chat_id = chat_id, text = msg, reply_markup = markup)

# async def send_msg(msg: str):
#   bot = telegram.Bot(token=token)
#   async with bot:
#     await bot.send_message(chat_id = chat_id, text = msg, parse_mode=telegram.constants.ParseMode.HTML)


base_url = 'https://etherscan.io/address/'
address = '0xdb767e9626a543BB9b61964421BFA4512185469b'

# asyncio.run(send_msg(f'''
# 代币创建信息\n
# Pair: <a href="{base_url}+{address}">{address}</a>\n#Address'''))
application = Application.builder().token("TOKEN").build()

# application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(button))

# Run the bot until the user presses Ctrl-C
application.run_polling(allowed_updates=Update.ALL_TYPES)
