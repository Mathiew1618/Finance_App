from dotenv import load_dotenv
load_dotenv()

import os
import requests
import pandas as pd
from datetime import datetime, timedelta

API_KEY = os.getenv("MASSIVE_API_KEY")
BASE = "https://api.massive.com/v2/aggs/ticker"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json",
}

def get_ohlc(symbol: str, days=30, multiplier=1, timespan="day"):
    end = datetime.utcnow().date()
    start = end - timedelta(days=days)

    url = (
        f"{BASE}/{symbol}/range/{multiplier}/{timespan}/"
        f"{start}/{end}"
    )

    resp = requests.get(url, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    if "results" not in data:
        raise RuntimeError(f"Unexpected OHLC response: {data}")

    df = pd.DataFrame(data["results"])
    df["t"] = pd.to_datetime(df["t"], unit="ms")
    df = df.rename(columns={
        "t": "Date",
        "o": "Open",
        "h": "High",
        "l": "Low",
        "c": "Close",
        "v": "Volume"
    })
    df = df.set_index("Date")
    return df
