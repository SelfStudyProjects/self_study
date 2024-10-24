# 실제 실행 파일

import time
import urllib.parse
import hashlib
import hmac
import base64
import requests
import json

class KrakenAPI:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_url = "https://api.kraken.com"
        self.session = requests.Session()
        self.last_nonce = int(time.time() * 1000000)

    def get_nonce(self):
        self.last_nonce += 1  # 항상 last_nonce를 증가시킵니다.
        return str(self.last_nonce)

    def get_kraken_signature(self, urlpath, data):
        post_data = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + post_data).encode('utf-8')
        message = urlpath.encode('utf-8') + hashlib.sha256(encoded).digest()
        
        mac = hmac.new(base64.b64decode(self.api_secret),
                      message, hashlib.sha512)
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
            response = self.session.post(
                request_uri,
                headers=headers,
                data=data,
                timeout=30
            )
            
            if response.status_code != 200:
                return {
                    "error": [f"HTTP {response.status_code}: {response.text}"],
                    "result": {}
                }
            
            return response.json()
            
        except Exception as e:
            return {"error": [str(e)], "result": {}}

    def get_trading_pairs(self):
        """Get available trading pairs"""
        uri_path = '/0/public/AssetPairs'
        try:
            response = requests.get(self.api_url + uri_path)
            return response.json()
        except Exception as e:
            print(f"Error getting trading pairs: {str(e)}")
            return None

    def get_balance(self):
        """Get account balance"""
        uri_path = '/0/private/Balance'
        data = {}
        
        result = self.kraken_request(uri_path, data)
        print("\n잔액 조회 결과:")
        if 'result' in result and result['result']:
            print(json.dumps(result, indent=2))
        else:
            print("잔액이 없습니다.")
        return result

    def create_sell_order(self, pair="XBTUSDT", volume="0.0001"):
        """Create a sell order"""
        uri_path = '/0/private/AddOrder'
        
        # Volume이 유효한 값인지 확인
        if float(volume) <= 0:
            print("판매 주문을 위한 유효한 볼륨이 필요합니다.")
            return {"error": ["Invalid volume"], "result": {}}
        
        data = {
            "ordertype": "market",
            "type": "sell",
            "pair": pair,
            "volume": 100,
            "validate": True
        }
        
        result = self.kraken_request(uri_path, data)
        print("\n판매 주문 결과:")
        if 'error' in result and result['error']:
            print(f"오류 발생: {result['error']}")
        else:
            print(json.dumps(result, indent=2))
        return result

    def test_rate_limits(self, num_requests=5, sleep_time=2):
        """Test API rate limits"""
        print(f"\n레이트 리밋 테스트 시작 (요청 수: {num_requests}, 대기 시간: {sleep_time}초)")
        
        results = []
        errors_count = 0
        
        for i in range(num_requests):
            start_time = time.time()
            
            try:
                result = self.get_balance()
                success = 'error' not in result or not result['error']
                if not success:
                    errors_count += 1
            except Exception as e:
                result = str(e)
                success = False
                errors_count += 1
            
            end_time = time.time()
            time_taken = end_time - start_time
            
            print(f"\n요청 {i+1}:")
            print(f"소요 시간: {time_taken:.2f}초")
            print(f"성공 여부: {'성공' if success else '실패'}")
            
            if errors_count >= 3:
                print("\n연속된 오류 발생으로 테스트를 중단합니다.")
                break
                
            if i < num_requests - 1:
                time.sleep(sleep_time)
        
        return results

def main():
    # API 키 설정
    API_KEY = "T5pRkr5TgTzAAkxY08LNmiSMpO+P4zEUyMAfp6nTOW91Aq7FdYPEgYdW"
    API_SECRET = "tfUIlLrtKijX/h1QiGos3gfC0mrUoM/3CJA37g6B1ZDMsAfOjQalFIDsc+uk5pRJewySiJ/fkMo5oclX/aYfJA=="
    
    try:
        kraken = KrakenAPI(API_KEY, API_SECRET)
        
        # 거래쌍 조회
        pairs = kraken.get_trading_pairs()
        if pairs and not pairs.get('error'):
            print("\n사용 가능한 거래쌍:")
            for pair in list(pairs['result'].keys())[:5]:
                print(pair)

        # Task A: 잔액 조회
        print("\n=== Task A: 잔액 조회 ===")
        balance_result = kraken.get_balance()
        
        # Task B: 판매 주문
        print("\n=== Task B: 판매 주문 ===")
        order_result = kraken.create_sell_order()
        
        # Task 3: 레이트 리밋 테스트
        print("\n=== Task 3: 레이트 리밋 테스트 ===")
        kraken.test_rate_limits()
            
    except Exception as e:
        print(f"\n프로그램 실행 중 오류 발생: {str(e)}")

if __name__ == "__main__":
    main()