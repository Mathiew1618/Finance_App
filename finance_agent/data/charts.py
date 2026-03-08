import matplotlib.pyplot as plt
import mplfinance as mpf
from pathlib import Path

def plot_candles(df, symbol, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{symbol}_candles.png"

    # Ensure correct column names
    df = df[["Open", "High", "Low", "Close", "Volume"]]

    mpf.plot(
        df,
        type="candle",
        volume=True,
        style="yahoo",
        title=f"{symbol} – Candlestick Chart",
        savefig=str(out_path)
    )

    return out_path
