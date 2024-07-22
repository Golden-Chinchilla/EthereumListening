from telegram import Bot
from dotenv import load_dotenv
import os
from uniswap import Uniswap
from dexscreener import Dex
import asyncio, time

# 代币创建事件和dexscreener api之间存在延迟, 需要在tg的每个msg上做个button, 事后可以一键点击查询dexscreener api中的相关信息
load_dotenv()
token = os.getenv('token')
chat_id = os.getenv('chat_id')

async def send_msg(msg: str):
  bot = Bot(token=token)
  async with bot:
    await bot.send_message(chat_id = chat_id, text = msg)

def main():
  while True:
    pair_addr = Uniswap.get_pair_addr()[0]

    # 未在event filter中获取到最新事件
    if pair_addr is None:
      continue

    # 发生事件，开始从dexscreener上获取相关信息 
    else:
      info = Dex.get_pair_info(pair_addr)
      asyncio.run(send_msg(info))

    time.sleep(3)

main()