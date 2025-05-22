import time
import requests
import winsound

# === 설정 ===
SYMBOL = "BTCUSDT"
GRANULARITY = "1m"
CHECK_INTERVAL = 10              # 10초마다 체크
PRICE_CHANGE_THRESHOLD = 0.01    # 1% 이상 변화 감지
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

# === 사운드 시스템템 ===
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
    print("🚨비트겟 급등락 감지기 by Slu")
    beepshort()
    prev_price = get_latest_price()
    if prev_price is None:
        print("초기 가격 로딩 실패")
        return

    print("")

    while True:
        time.sleep(CHECK_INTERVAL)
        try:
            curr_price = get_latest_price()
            if curr_price is None:
                print("현재 가격 로딩 실패")
                continue

            delta = (curr_price - prev_price) / prev_price
            print(f" {curr_price:.2f} |  {delta*100:.2f}%")

            if abs(delta) >= PRICE_CHANGE_THRESHOLD:
                print("10초 내 급변 감지함")
                beeplow()
                beep()
                beeplow()
                beep()
                beeplow()
                beep()
                beeplow()
                beep()
                beeplow()
                beep()
                beeplow()
                beep()

            prev_price = curr_price  # 현재 가격을 다음 비교용으로 저장

        except Exception as e:
            print(f"에러: {e}")

if __name__ == "__main__":
    main()
