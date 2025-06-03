import time
import requests
import winsound
import os

# === 설정 ===
SYMBOL = "BTCUSDT"
GRANULARITY = "1m"
CHECK_INTERVAL = 5              # 5초마다 체크
PRICE_CHANGE_THRESHOLD = 0.1    # 변화 감지 threshold (0.01 이 1퍼센트)
PRODUCT_TYPE = "usdt-futures"
alNum = 0

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


def beep_majestic():
    sequence = [
        (400, 200),
        (500, 200),
        (600, 200),
        (700, 200),
        (800, 200),
        (600, 200),
        (500, 200),
        (400, 200)
    ]
    for freq, dur in sequence:
        print(".", end='', flush=True)  # ← 바로 출력되게 함
        winsound.Beep(freq, dur)
        time.sleep(0.05)

    print("")  # 줄바꿈


def titleprint():
    print("🚨 Crypto Alert 🚨 by Slu Park / Bitget API")
    print(
        f" Threshold Parameter : {PRICE_CHANGE_THRESHOLD} / {SYMBOL} / @ {alNum}")


# === 메인 루프 ===
def main():

    global alNum
    prev_price = get_latest_price()
    if prev_price is None:
        print(" - ")
        return
    titleprint()
    beep_majestic()

    line_count = 0

    while True:

        try:
            curr_price = get_latest_price()
            if curr_price is None:
                print(" - ")
                continue

            delta = (curr_price - prev_price) / prev_price
            print(f"{curr_price:10.2f} | {delta*100:8.3f}%")
            line_count += 1

            if abs(delta*100) >= PRICE_CHANGE_THRESHOLD:
                print("@@@@ 급변 감지함 @@@@")
                alNum += 1
                for _ in range(6):
                    beeplow()
                    beep()

            # === 40줄마다 화면 클리어 ===
            if line_count >= 40:
                os.system('cls')  # Windows에서 콘솔 clear
                titleprint()
                line_count = 0

            prev_price = curr_price
            time.sleep(CHECK_INTERVAL)

        except Exception as e:
            print(f"에러: {e}")


if __name__ == "__main__":
    main()
