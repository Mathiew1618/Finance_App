# finance_agent/gui/__main__.py

import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel
)
from PySide6.QtCore import Qt

from finance_agent.agent import chat


class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Local Market Assistant")
        self.resize(900, 600)

        main_layout = QHBoxLayout(self)

        # -----------------------------
        # LEFT: Chat area
        # -----------------------------
        left_layout = QVBoxLayout()
        main_layout.addLayout(left_layout, 3)

        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        left_layout.addWidget(self.chat_area)

        input_layout = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText(
            "Ask about a symbol, chart, or market condition..."
        )
        self.send_button = QPushButton("Send")

        input_layout.addWidget(self.input_box, 4)
        input_layout.addWidget(self.send_button, 1)
        left_layout.addLayout(input_layout)

        # -----------------------------
        # RIGHT: Chart / info panel
        # -----------------------------
        right_layout = QVBoxLayout()
        main_layout.addLayout(right_layout, 2)

        self.chart_label = QLabel("Chart preview will appear here.")
        self.chart_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(self.chart_label)

        # -----------------------------
        # Signals
        # -----------------------------
        self.send_button.clicked.connect(self.on_send)
        self.input_box.returnPressed.connect(self.on_send)

    def append_message(self, role: str, content: str):
        if role == "user":
            prefix = "<b>You:</b> "
        else:
            prefix = "<b>Assistant:</b> "

        self.chat_area.append(prefix + content)

    def set_busy(self, busy: bool):
        self.input_box.setDisabled(busy)
        self.send_button.setDisabled(busy)
        if busy:
            self.send_button.setText("Thinking...")
        else:
            self.send_button.setText("Send")

    def on_send(self):
        text = self.input_box.text().strip()
        if not text:
            return

        self.append_message("user", text)
        self.input_box.clear()
        self.set_busy(True)

        try:
            reply = chat(text)
        except Exception as e:
            reply = f"[Error] {e}"

        self.append_message("assistant", reply)
        self.set_busy(False)
        self.input_box.setFocus()


def main():
    app = QApplication(sys.argv)
    win = ChatWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
