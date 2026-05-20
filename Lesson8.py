import os
import sys

import psycopg2

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
    QLabel, QListWidget
)

conn = psycopg2.connect(
    dbname="test_db",
    user="user_test",
    password="1234",
    host="localhost",
    port="5432",
)

cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100)
    )
""")
conn.commit()

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt6 + PostgreSQL")
        self.resize(400, 400)

        self.layout = QVBoxLayout()

        self.label = QLabel("Введите товар")

        self.input = QLineEdit()

        self.button = QPushButton("Добавить")

        self.list_widget = QListWidget()

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.list_widget)

        self.setLayout(self.layout)

        self.button.clicked.connect(self.add_product)

        self.load_products()

    def load_products(self):
        self.list_widget.clear()
        cursor.execute("SELECT title FROM products")
        products = cursor.fetchall()

        for product in products:
            self.list_widget.addItem(product[0])

    def add_product(self):
        title = self.input.text()
        if title:
            cursor.execute("INSERT INTO products (title) VALUES (%s)", (title,))
            conn.commit()
            self.input.clear()
            self.load_products()

app = QApplication(sys.argv)
window = Window()
window.show()

sys.exit(app.exec())