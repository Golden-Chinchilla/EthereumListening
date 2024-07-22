from web3 import Web3
import requests
from dotenv import load_dotenv
import os

load_dotenv()
infura = os.getenv('infura')
w3 = Web3(Web3.HTTPProvider(infura))

class Tools():
    @classmethod
    def _check_signature(cls, hex_signature: str) -> str:
        hex_signature_url = f'https://www.4byte.directory/api/v1/signatures/?format=json&hex_signature={hex_signature}'
        r = requests.get(hex_signature_url).json()
        try:
            text_signature = r['results'][0]['text_signature']
            return text_signature
        except:
            return 'Not Found'
        
    @classmethod
    # logs = event_filter.get_new_entries()
    def get_tx_hash_from_event_logs(cls, logs) -> str:
        binary = logs[0]['transactionHash']
        tx_hash = Web3.to_hex(binary)
        return tx_hash
    
    @classmethod
    def get_tx_method(cls, tx_hash: str) -> str:
        details = w3.eth.get_transaction(tx_hash)
        # 获取二进制数据
        input = details['input']
        # 转换成十六进制
        hex = Web3.to_hex(input)
        # 取前十位字符串（包含0x在内）
        method_id = hex[:10]
        text_signature = cls._check_signature(method_id)
        return method_id, text_signature