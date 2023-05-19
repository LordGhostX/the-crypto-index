import pandas as pd
import numpy as np
import plotly.graph_objects as go


def compile_data():
    data = list()
    coins = ["BTC", "ETH", "BNB", "NEO", "LTC", "ADA", "XRP", "EOS", "TRX", "ETC"]
    for coin in coins:
        df = pd.read_csv(f"data/{coin}USDT_1D.csv")
        data.append((coin, df))
        
    open, high, low, close = pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    for d in data:
        coin, df = d
        open[coin] = df["open"]
        high[coin] = df["high"]
        low[coin] = df["low"]
        close[coin] = df["close"]
    return data[0][1]["timestamp"], open, high, low, close

def compute_harmonic_mean(df):
    reciprocal_df = 1 / df
    reciprocal_df.replace([np.inf, -np.inf], np.nan, inplace=True)
    harmonic_mean = list()
    for index, row in reciprocal_df.iterrows():
        harmonic_mean.append(10 / sum(row))
    return harmonic_mean

def compute_index(timestamp, open, high, low, close):
    index_ohlc = pd.DataFrame({
        "timestamp": timestamp,
        "open": compute_harmonic_mean(open),
        "high": compute_harmonic_mean(high),
        "low": compute_harmonic_mean(low),
        "close": compute_harmonic_mean(close)
    })
    return index_ohlc

if __name__ == "__main__":
    timestamp, open, high, low, close = compile_data()
    index = compute_index(timestamp, open, high, low, close)
    index.to_csv("data/INDEX.csv", index=False)
    index["timestamp"] = pd.to_datetime(index["timestamp"], unit="s")
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=index["timestamp"],
                open=index["open"],
                high=index["high"],
                low=index["low"],
                close=index["close"]
            )
        ]
    )
    fig.update_layout(
        xaxis_rangeslider_visible=False,
        title="The Crypto Index"
    )
    fig.show()