from web3 import Web3
import requests

w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/5c70aefd4b02485c97031081e7d11720'))

class Tools():
    @classmethod
    def _check_signature(cls, hex_signature: str) -> str:
        hex_signature_url = f'https://www.4byte.directory/api/v1/signatures/?format=json&hex_signature={hex_signature}'
        r = requests.get(hex_signature_url).json()
        text_signature = r['results'][0]['text_signature']
        return text_signature
    
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