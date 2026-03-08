# finance_agent/tools.py

from typing import Dict, Any, List
import datetime

def snapshot_symbol(symbol: str) -> Dict[str, Any]:
    """
    Return a simple snapshot for a symbol.
    In your real version, call your market data API here.
    """
    return {
        "symbol": symbol.upper(),
        "price": 123.45,
        "change": -1.23,
        "percent_change": -0.99,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    }

def get_ohlc(symbol: str, timeframe: str = "1d", limit: int = 50) -> List[Dict[str, Any]]:
    """
    Return OHLC candles for a symbol.
    """
    candles = []
    for i in range(limit):
        candles.append({
            "timestamp": (datetime.datetime.utcnow() - datetime.timedelta(days=i)).isoformat() + "Z",
            "open": 100 + i,
            "high": 105 + i,
            "low":  95 + i,
            "close": 102 + i,
            "volume": 1000000 + i * 1000,
        })
    return list(reversed(candles))

def render_chart(symbol: str, ohlc: List[Dict[str, Any]]) -> str:
    """
    Render a candlestick chart and return the file path.
    """
    import pandas as pd
    import mplfinance as mpf
    from pathlib import Path

    df = pd.DataFrame(ohlc)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.set_index("timestamp", inplace=True)
    df.rename(columns={
        "open": "Open",
        "high": "High",
        "low": "Low",
        "close": "Close",
        "volume": "Volume",
    }, inplace=True)

    charts_dir = Path("charts")
    charts_dir.mkdir(exist_ok=True)
    out_path = charts_dir / f"{symbol.upper()}_chart.png"

    mpf.plot(
        df,
        type="candle",
        volume=True,
        style="yahoo",
        savefig=str(out_path)
    )

    return str(out_path)
