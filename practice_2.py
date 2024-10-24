import os
import time
import urllib.parse
import hashlib
import hmac
import base64
import requests
import json
from dotenv import load_dotenv

class KrakenAPI:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_url = "https://api.kraken.com"
        self.last_nonce = int(time.time() * 1000000)

    def get_nonce(self):
        self.last_nonce += 1
        return str(self.last_nonce)

    def get_kraken_signature(self, urlpath, data):
        post_data = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + post_data).encode('utf-8')
        message = urlpath.encode('utf-8') + hashlib.sha256(encoded).digest()
        
        mac = hmac.new(base64.b64decode(self.api_secret), message, hashlib.sha512)
        sigdigest = base64.b64encode(mac.digest())
        return sigdigest.decode('utf-8')

    def kraken_request(self, uri_path, data):
        data['nonce'] = self.get_nonce()
        
        headers = {
            'API-Key': self.api_key,
            'API-Sign': self.get_kraken_signature(uri_path, data),
            'User-Agent': 'Kraken API Client',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        request_uri = self.api_url + uri_path
        print(f"요청 URI: {request_uri}")
        print(f"전송 데이터: {data}")
        
        try:
            response = requests.post(request_uri, headers=headers, data=data, timeout=30)
            if response.status_code != 200:
                return {"error": [f"HTTP {response.status_code}: {response.text}"], "result": {}}
            return response.json()
        except Exception as e:
            return {"error": [str(e)], "result": {}}

    def get_trading_pairs(self):
        uri_path = '/0/public/AssetPairs'
        try:
            response = requests.get(self.api_url + uri_path)
            return response.json()
        except Exception as e:
            print(f"Error getting trading pairs: {str(e)}")
            return None

    def get_balance(self):
        uri_path = '/0/private/Balance'
        data = {}
        result = self.kraken_request(uri_path, data)
        print("\n잔액 조회 결과:")
        if 'result' in result and result['result']:
            print(json.dumps(result, indent=2))
        else:
            print("잔액이 없습니다.")
        return result

    def simulate_sell_order(self, pair, volume, price=None):
        """판매 주문 시뮬레이션"""
        print(f"\n판매 주문 시뮬레이션:")
        print(f"거래쌍: {pair}, 볼륨: {volume}, 가격: {price}")
        print("잔액이 없으므로 실제 판매 주문을 실행할 수 없습니다.")

def main():
    load_dotenv()
    API_KEY = os.getenv("KRAKEN_API_KEY")
    API_SECRET = os.getenv("KRAKEN_API_SECRET")

    if not API_KEY or not API_SECRET:
        print("API 키나 비밀 키가 설정되지 않았습니다.")
        return

    kraken = KrakenAPI(API_KEY, API_SECRET)

    print("\n=== 거래쌍 조회 ===")
    pairs = kraken.get_trading_pairs()
    if pairs and not pairs.get('error'):
        print("\n사용 가능한 거래쌍:")
        for pair in list(pairs['result'].keys())[:5]:
            print(pair)

    print("\n=== 잔액 조회 ===")
    balance_result = kraken.get_balance()

    # 충분한 대기 시간 추가
    time.sleep(10)  # 10초 대기

    print("\n=== 판매 주문 시뮬레이션 ===")
    kraken.simulate_sell_order(pair="1INCHUSD", volume="1.25", price="27500")

if __name__ == "__main__":
    main()