import requests
import datetime
from uniswap import Uniswap
# https://requests.readthedocs.io/en/latest/

# dexscreen api
# https://docs.dexscreener.com/api/reference#get-one-or-multiple-pairs-by-chain-and-pair-address

# Get one or multiple pairs by chain and pair address
# GET https://api.dexscreener.com/latest/dex/pairs/:chainId/:pairAddresses

# 示例：https://api.dexscreener.com/latest/dex/pairs/ethereum/0x85cce2cc03ee7a49acd086ee96f9bf873548ca42
# test_addr = '0x93f053DEa19e5606D158Fc0c6E6F4fB32f3beaF0'
class Dex():
    @classmethod
    def get_pair_info(cls, pair_addr: str) -> str:

        # 查询不到交易对时的返回值：{"schemaVersion":"1.0.0","pairs":null,"pair":null}
        token_url = f'https://api.dexscreener.com/latest/dex/pairs/ethereum/{pair_addr}'

        # json viewer
        # https://www.tutorialspoint.com/online_json_editor.htm
        raw = requests.get(token_url)
        r = raw.json()

        # 如果在dexscreener上获取不到相应信息，则抓取Factory的链上事件信息
        if r['pairs'] is None:
            content = '未在dexscreener上找到相关信息。'
            return content

        # telegram 内做二次查询
        else:
            # url
            dexscreener_url = r['pairs'][0]['url']

            # baseToken/name, baseToken/symbol
            token_name = r['pairs'][0]['baseToken']['name']
            token_symbol = r['pairs'][0]['baseToken']['symbol']

            # info/website, info/social
            # 这两个信息实际不一定有
            try:
                website = r['pairs'][0]['info']['websites'][0]['url']
                twitter = r['pairs'][0]['info']['socials'][0]['url']
            except:
                website = 'none'
                twitter = 'none'

            # 流动性数据
            liquidity_usd = r['pairs'][0]['liquidity']['usd']
            liquidity_base = r['pairs'][0]['liquidity']['base']
            liquidity_quote = r['pairs'][0]['liquidity']['quote']

            # 创建时间
            timestamp = r['pairs'][0]['pairCreatedAt']
            time = datetime.datetime.fromtimestamp(timestamp/1000, datetime.timezone.utc)
            content = f'''
        Dexscreener: {dexscreener_url}\n
        Name: {token_name}\n
        Symbol: {token_symbol}\n
        Website: {website}\n
        Twitter: {twitter}\n
        Liquidity_usd: {liquidity_usd}\n
        Liquidity_base: {liquidity_base}\n
        Liquidity_quote: {liquidity_quote}\n
        Created At: {time}
        '''
            return content