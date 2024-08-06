import telegram
from dotenv import load_dotenv
import os
from uniswap import Uniswap
from dexscreener import Dex
import asyncio, time
from util import Tools

# 代币创建事件和dexscreener api之间存在延迟, 需要在tg的每个msg上做个button, 事后可以一键点击查询dexscreener api中的相关信息
load_dotenv()
token = os.getenv('token')
chat_id = os.getenv('chat_id')
base_url = 'https://etherscan.io/address/'

async def send_msg(msg: str):
  bot = telegram.Bot(token=token)
  async with bot:
    await bot.send_message(chat_id = chat_id, text = msg, parse_mode=telegram.constants.ParseMode.HTML)

def main():
  while True:
    # return pair_addr, token0, token1, tx_hash
    tuple = Uniswap.get_event_info()
    # 未在event filter中获取到最新事件
    if tuple is None:
      continue

    # 发生事件，开始从dexscreener上获取相关信息
    else:
      pair_addr = tuple[0]
      token0 = tuple[1]
      token1 = tuple[2]
      tx_hash = tuple[3]

      # info = Dex.get_pair_info(pair_addr)
      method_info = Tools.get_tx_method(tx_hash)
      method_id = method_info[0]
      
      # wETH 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2
      # 这部分在 Uniswap.get_event_info() 中处理掉更好
      if token0 == '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2':
      # 由于存在同一个 method id 对应多个 text_signature 的情况，text_signature 暂时不放进 send_msg() 中
      # text_signature = method_info[1]
        asyncio.run(send_msg(f'''
  <b>代币创建信息</b>\n
  Method ID: {method_id}\n
  Pair: <a href="{base_url}{pair_addr}">{pair_addr}</a>\n
  Token: <a href="{base_url}{token1}">{token1}</a>'''))
      else:
        asyncio.run(send_msg(f'''
  <b>代币创建信息</b>\n
  Method ID: {method_id}\n
  Pair: <a href="{base_url}{pair_addr}">{pair_addr}</a>\n
  Token: <a href="{base_url}{token0}">{token0}</a>'''))
      
#       asyncio.run(send_msg(f'''
# <b>代币创建信息</b>\n
# Method ID: {method_id}\n
# Pair: <a href="{base_url}{pair_addr}">{pair_addr}</a>\n
# Token0: <a href="{base_url}{token0}">{token0}</a>\n
# Token1: <a href="{base_url}{token1}">{token1}</a>\n\n
# <b>Dexscreener信息</b>\n
# {info}'''))

    time.sleep(2)

main()