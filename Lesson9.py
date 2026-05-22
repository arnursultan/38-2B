import sys

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QRadioButton,
    QPushButton,
    QMessageBox,
    QButtonGroup
)

from PyQt6.QtGui import QIcon


groups = [
    "35-1",
    "36-1",
    "37-1",
    "38-1",
    "38-2",
    "39-1",
    "40-1"
]


class Quiz(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Backend Quiz")
        self.setWindowIcon(QIcon("icon.ico"))
        self.resize(320, 280)

        layout = QVBoxLayout()

        title = QLabel("Какая backend-группа лучшая?")
        title.setStyleSheet("font-size:18px; font-weight:bold;")
        layout.addWidget(title)

        self.group = QButtonGroup()

        for i, g in enumerate(groups):
            rb = QRadioButton(g)
            self.group.addButton(rb, i)
            layout.addWidget(rb)

        btn = QPushButton("Проверить")
        btn.clicked.connect(self.check)
        layout.addWidget(btn)

        self.setLayout(layout)

    def check(self):
        selected = self.group.checkedButton()

        if not selected:
            QMessageBox.warning(self, "Ошибка", "Сначала выберите группу.")
            return

        group = selected.text()

        if group == "38-2":
            text = f"""
Вы выбрали {group}.

Система завершила проверку...

✅ Верно.

38-2 — лучшая backend-группа.
"""
        else:
            text = f"""
Вы выбрали {group}.

Система завершила проверку...

❌ Неверно.

После анализа выяснилось,
что лучшая backend-группа — 38-2 😎
"""

        QMessageBox.information(self, "Результат", text)


app = QApplication(sys.argv)

window = Quiz()
window.show()

sys.exit(app.exec())