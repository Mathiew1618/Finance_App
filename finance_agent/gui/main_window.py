from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QTextEdit
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from finance_agent.agent import snapshot_symbol
import os


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Finance Agent Dashboard")
        self.setMinimumSize(900, 700)

        layout = QVBoxLayout()

        # -----------------------------
        # Input Row
        # -----------------------------
        input_row = QHBoxLayout()
        self.symbol_input = QLineEdit()
        self.symbol_input.setPlaceholderText("Enter symbol (e.g., AAPL)")
        snapshot_btn = QPushButton("Snapshot")
        snapshot_btn.clicked.connect(self.run_snapshot)

        input_row.addWidget(self.symbol_input)
        input_row.addWidget(snapshot_btn)

        # -----------------------------
        # Chart Display
        # -----------------------------
        self.chart_label = QLabel("Chart will appear here")
        self.chart_label.setAlignment(Qt.AlignCenter)

        # -----------------------------
        # Summary Display
        # -----------------------------
        self.summary_box = QTextEdit()
        self.summary_box.setReadOnly(True)

        # -----------------------------
        # Open Note Button
        # -----------------------------
        self.open_note_btn = QPushButton("Open Note in Obsidian")
        self.open_note_btn.clicked.connect(self.open_note)
        self.open_note_btn.setEnabled(False)

        # -----------------------------
        # Add widgets to layout
        # -----------------------------
        layout.addLayout(input_row)
        layout.addWidget(self.chart_label)
        layout.addWidget(self.summary_box)
        layout.addWidget(self.open_note_btn)

        self.setLayout(layout)

    # ---------------------------------------
    # Run Snapshot Tool
    # ---------------------------------------
    def run_snapshot(self):
        symbol = self.symbol_input.text().strip().upper()
        if not symbol:
            self.summary_box.setText("Please enter a symbol.")
            return

        result = snapshot_symbol(symbol)

        # Load chart
        pixmap = QPixmap(result["candle_image"])
        self.chart_label.setPixmap(
            pixmap.scaledToWidth(800, Qt.SmoothTransformation)
        )

        # Summary text
        summary_text = (
            f"Symbol: {result['symbol']}\n"
            f"Rows: {result['rows']}\n"
            f"Range: {result['start']} → {result['end']}\n"
            f"Note: {result['note']}\n"
        )
        self.summary_box.setText(summary_text)

        # Store note path for "Open Note" button
        self.last_note_path = result["note"]
        self.open_note_btn.setEnabled(True)

    # ---------------------------------------
    # Open Note in Obsidian
    # ---------------------------------------
    def open_note(self):
        if hasattr(self, "last_note_path"):
            os.startfile(self.last_note_path)
