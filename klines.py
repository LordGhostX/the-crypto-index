import time
import requests
import pandas as pd


def fetch_recent_klines_data(symbol, interval="1d", limit=1000, start_time=None, end_time=None):
    params = {
        "symbol": symbol,
        "interval": interval,
        "limit": limit,
        "startTime": None if start_time is None else start_time * 1000,
        "endTime": None if end_time is None else end_time * 1000
    }
    r = requests.get("https://api.binance.com/api/v3/klines", params=params)

    klines_data = []
    for i in r.json():
        klines_data.append({
            "timestamp": int(i[0] / 1000),
            "open": float(i[1]),
            "high": float(i[2]),
            "low": float(i[3]),
            "close": float(i[4]),
            "volume": float(i[5])
        })

    return klines_data


def fetch_klines_data(symbol, interval, start_time, end_time=None):
    if end_time is None:
        end_time = int(time.time())

    latest_timestamp, klines_data = start_time, []

    while latest_timestamp < end_time:
        t_klines_data = [i for i in fetch_recent_klines_data(
            symbol, interval, 1000, latest_timestamp) if i["timestamp"] <= end_time]
        klines_data.extend(t_klines_data)
        latest_timestamp = klines_data[-1]["timestamp"] + \
            (klines_data[-1]["timestamp"] - klines_data[-2]["timestamp"])

    return klines_data


def save_klines_to_csv(data, filename, index=None):
    df = pd.DataFrame(data)
    if index:
        df = df.set_index(index)
    df.to_csv(filename)


def load_klines_from_csv(filename, index=None):
    df = pd.read_csv(filename, index_col=index)
    return df.to_dict("records")

if __name__ == "__main__":
    coins = ["BTC", "ETH", "BNB", "NEO", "LTC", "ADA", "XRP", "EOS", "TRX", "ETC"]
    for coin in coins:
        print("Fetching data for", coin)
        data = fetch_klines_data(coin + "USDT", "1d", 1528848000, 1684454399)
        save_klines_to_csv(data, f"data/{coin}USDT_1D.csv", index="timestamp")