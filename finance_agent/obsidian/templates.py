from datetime import datetime

def market_note_template(symbol: str, summary: str, candle_image: str, start: str, end: str, rows: int) -> str:
    """
    Build the Obsidian markdown note for a market snapshot.
    """

    date_str = datetime.now().strftime("%Y-%m-%d")

    return f"""# {symbol} — Market Snapshot
**Date:** {date_str}  
**Range:** {start} → {end}  
**Rows:** {rows}  

## Summary
{summary}

## Chart
![[{candle_image}]]

"""
