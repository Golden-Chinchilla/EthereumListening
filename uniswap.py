# 参考: https://cryptomarketpool.com/how-to-listen-for-ethereum-events-using-web3-in-python/

# V3 ethereum-deployments
# https://docs.uniswap.org/contracts/v3/reference/deployments/ethereum-deployments

# V2 ethereum-deployments
# https://docs.uniswap.org/contracts/v2/reference/smart-contracts/v2-deployments
# V2 EVENT https://etherscan.io/address/0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f#events

from web3 import Web3
from dotenv import load_dotenv
import os
from util import Tools

load_dotenv()
infura = os.getenv('infura')
w3 = Web3(Web3.HTTPProvider(infura))

# uniswap_router = '0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D'
uniswap_factory = '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f'
uniswap_factory_abi = '[{"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"token0","type":"address"},{"indexed":true,"internalType":"address","name":"token1","type":"address"},{"indexed":false,"internalType":"address","name":"pair","type":"address"},{"indexed":false,"internalType":"uint256","name":"","type":"uint256"}],"name":"PairCreated","type":"event"},{"constant":true,"inputs":[{"internalType":"uint256","name":"","type":"uint256"}],"name":"allPairs","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"allPairsLength","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"}],"name":"createPair","outputs":[{"internalType":"address","name":"pair","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"feeTo","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"feeToSetter","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"getPair","outputs":[{"internalType":"address","name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeTo","type":"address"}],"name":"setFeeTo","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"internalType":"address","name":"_feeToSetter","type":"address"}],"name":"setFeeToSetter","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]'
FactoryContract = w3.eth.contract(address = uniswap_factory, abi = uniswap_factory_abi)

# 代币创建事件筛选
event_filter = FactoryContract.events.PairCreated.create_filter(fromBlock = 'latest')

# get_new_entries() 返回值示例
# [AttributeDict({'args': AttributeDict({'token0': '0x95DE2Dc9d67a0a0e03F0311027e74d94433BAA90', 'token1': '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2', 'pair': '0x7dEe5717E92CA2DDF4CC176EAA823c365a04299F', '': 345790}), 'event': 'PairCreated', 'logIndex': 136, 'transactionIndex': 35, 'transactionHash': HexBytes('0x7662eb76d97b842bcdbb42dcb90f44dae6a015d63e0391bd97a3e6528fadd207'), 'address': '0x5C69bEe701ef814a2B6a3EDD4B1652CB9cc5aA6f', 'blockHash': HexBytes('0x60e5a47c99bee14ecab8ccd035087a16e0c35bb165b6bbbf6e67f590a849da63'), 'blockNumber': 20355044})]
class Uniswap():
    @classmethod
    def get_event_info(cls) -> tuple:
        logs = event_filter.get_new_entries()
        try:
            pair_addr = logs[0]['args']['pair']
            token0 = logs[0]['args']['token0']
            token1 = logs[0]['args']['token1']
            tx_hash = Tools.get_tx_hash_from_event_logs(logs)
            return pair_addr, token0, token1, tx_hash
        except:
            return