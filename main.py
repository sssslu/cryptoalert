import time
import requests
import winsound
import os

# === 설정 ===
SYMBOL = "BTCUSDT"
GRANULARITY = "1m"
CHECK_INTERVAL = 5              # 5초마다 체크
PRICE_CHANGE_THRESHOLD = 0.004    # 변화 감지 threshold
PRODUCT_TYPE = "usdt-futures"

# === 비트겟 현재 가격 받아오기 ===
def get_latest_price():
    url = "https://api.bitget.com/api/v2/mix/market/candles"
    params = {
        "symbol": SYMBOL,
        "granularity": GRANULARITY,
        "limit": 1,
        "productType": PRODUCT_TYPE
    }
    res = requests.get(url, params=params)
    data = res.json().get("data", [])
    if data:
        return float(data[0][4])  # 종가 (close)
    return None

# === 사운드 시스템 ===
def beep():
    winsound.Beep(frequency=1000, duration=300)
    
def beeplow():
    winsound.Beep(frequency=500, duration=300)
    
def beepshort():
    winsound.Beep(frequency=1200, duration=100)

def beeploww():
    winsound.Beep(frequency=432, duration=80)


# === 메인 루프 ===
def main():
    print("🚨Bitcoin 급등락 감지기🚨 by Slu - Bitget API")
    beeploww()
    beeplow()
    beep()
    beepshort()
    prev_price = get_latest_price()
    if prev_price is None:
        print("초기 가격 로딩 실패")
        return

    print("")
    line_count = 0

    while True:
        
        try:
            curr_price = get_latest_price()
            if curr_price is None:
                print("현재 가격 로딩 실패")
                continue

            delta = (curr_price - prev_price) / prev_price
            print(f" {curr_price:.2f} |  {delta*100:.2f}%")
            line_count += 1

            if abs(delta) >= PRICE_CHANGE_THRESHOLD:
                print("@@@@ 급변 감지함 @@@@")
                for _ in range(7):
                    beeplow()
                    beep()

            # === 40줄마다 화면 클리어 ===
            if line_count >= 40:
                os.system('cls')  # Windows에서 콘솔 clear
                print("🚨Bitcoin 급등락 감지기🚨 by Slu - Bitget API")
                line_count = 0

            prev_price = curr_price
            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            print(f"에러: {e}")

if __name__ == "__main__":
    main()
