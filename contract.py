from web3 import Web3
from dotenv import load_dotenv
import os
import requests

load_dotenv()
infura = os.getenv('infura')
etherscan_api = os.getenv('etherscan_api')
w3 = Web3(Web3.HTTPProvider(infura))
# token = '0x07598534E57655B2B5c20CD466fEc55043F9A905'
class Contract():
    @classmethod
    def token_name_and_symbol(cls, address: str) -> tuple:
        abi_req = f'https://api.etherscan.io/api?module=contract&action=getabi&address={address}&apikey={etherscan_api}'
        r = requests.get(abi_req)
        abi = r.json()['result']
        contract = w3.eth.contract(address = address, abi = abi)
        name = contract.functions.name().call()
        symbol = contract.functions.symbol().call()
        return name, symbol