from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, Bot
from telegram.ext import Application, CallbackQueryHandler , ContextTypes
# from telegram.ext import Application, CommandHandler, ContextTypes
import asyncio
from dotenv import load_dotenv
import os

# 代币创建事件和dexscreener api之间存在延迟, 需要在tg的每个msg上做个button, 事后可以一键点击查询dexscreener api中的相关信息
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
  pass

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

asyncio.run(send_msg(f'''
代币创建信息\n
Pair: <a href="{base_url}+{address}">{address}</a>\n#Address'''))