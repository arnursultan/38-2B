import sys
import sqlite3
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QVBoxLayout

)

class UserWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Урок 4 - PyQt6 + SQlite")
        self.setGeometry(300, 200, 400, 250)


        self.name_label = QLabel("Имя:")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Введите имя")

        self.button = QPushButton("Сохранить в БД")
        self.button.clicked.connect(self.save_to_db)

        self.result = QLabel("")

        layout = QVBoxLayout()


        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.button)
        layout.addWidget(self.result)
        self.setLayout(layout)


        self.init_db()

    def init_db(self):
        self.conn =sqlite3.connect('users.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS users (
                                                                 id INTEGER PRIMARY KEY,
                                                                 name TEXT NOT NULL
                            )
                            ''')
        self.conn.commit()


    def save_to_db(self):
        name = self.name_input.text()

        if not name:
            self.result.setText("Введите имя")
            return

        self.cursor.execute(
            "INSERT INTO users (name) VALUES (?)",
            (name,)
        )

        self.conn.commit()

        self.result.setText(f"Имя '{name}' сохранено!")
        self.name_input.clear()

app = QApplication(sys.argv)
window = UserWindow()
window.show()
sys.exit(app.exec())