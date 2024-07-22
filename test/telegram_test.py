import telegram
import asyncio
from dotenv import load_dotenv
import os

# 代币创建事件和dexscreener api之间存在延迟, 需要在tg的每个msg上做个button, 事后可以一键点击查询dexscreener api中的相关信息
load_dotenv()
token = os.getenv('token')
chat_id = os.getenv('chat_id')

# 先创建Button对象，再创建Markup对象
# keyboard = [
#   [telegram.InlineKeyboardButton(text = '测试按钮', callback_data = 'test')]
#   ]

# markup = telegram.InlineKeyboardMarkup(keyboard)

# async def send_msg(msg: str):
#   bot = telegram.Bot(token=token)
#   async with bot:
#     await bot.send_message(chat_id = chat_id, text = msg, reply_markup = markup)

async def send_msg(msg: str):
  bot = telegram.Bot(token=token)
  async with bot:
    await bot.send_message(chat_id = chat_id, text = msg, parse_mode=telegram.constants.ParseMode.HTML)


base_url = 'https://etherscan.io/address/'
address = '0xdb767e9626a543BB9b61964421BFA4512185469b'

asyncio.run(send_msg(f'''
*代币创建信息*\n
Pair: <a href="{base_url}+{address}">{address}</a>'''))