from pathlib import Path
from .templates import market_note_template

def write_market_note(vault_dir: Path, symbol: str, summary: str, candle_image: Path, options_image: Path | None):
    """
    Write a market snapshot note into the Obsidian vault root.
    """

    # Ensure chart path is relative to vault
    rel_chart_path = candle_image.relative_to(vault_dir)

    # Build markdown content
    content = market_note_template(
        symbol=symbol,
        summary=summary,
        candle_image=str(rel_chart_path),
        start="unknown",   # agent will fill these in later
        end="unknown",
        rows=0
    )

    # Output file
    note_path = vault_dir / f"{symbol}.md"

    # Write note
    note_path.write_text(content, encoding="utf-8")

    return note_path
