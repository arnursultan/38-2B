# import sys # Работа с параметрами запуска и завершения программы
# from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel # Основные элементы PyQt6
#
# app = QApplication(sys.argv) # Создаем приложение (обязателен для PyQt)
#
# window = QMainWindow() # Создаем главное окно
# window.setWindowTitle("Моё первое окно") # Устанавливаем заголовок
# window.resize(400, 300) # Размер окна: ширина, высота
#
# label = QLabel("Привет, PyQt6!", window) # Добавляем текст в окно
# label.move(150, 180) # Размещаем текст по координатам х, у
#
# window.show() # Показываем окно на экране
# sys.exit(app.exec()) # Запускаем цикл событий и корректно завершаем программу

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.count=0
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Пример с Декомпозицией")
        self.resize(400, 300)

        self.label = QLabel("Счёт: 0", self)
        self.label.move(160, 100)
        self.label.resize(100, 30)

        self.button = QPushButton("Нажать", self)
        self.button.move(155, 150)
        self.button.resize(100, 35)

        self.button.clicked.connect(self.on_button_click)

    def on_button_click(self):
        self.count+=1
        self.label.setText(f"Счёт: {self.count}")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()