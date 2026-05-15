import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QLineEdit,
    QLabel, QComboBox, QSpinBox, QMessageBox, QHeaderView,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from database import PlaylistDB

MOOD_COLORS = {
    "🔥 Hype":    "#1565C0",   # тёмно-синий
    "😌 Chill":   "#00838F",   # тёмная бирюза
    "😢 Sad":     "#6D6D6D",   # серый
    "💪 Workout": "#2E7D32",   # тёмно-зелёный
    "💪 Party":   "#6A1B9A",   # фиолетовый
}


class PlaylistWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.db = PlaylistDB()
        self.selected_id = None
        self.setWindowTitle("🎵 My Playlist")
        self.resize(720, 520)
        self.init_ui()
        self.load_table()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        layout.addWidget(QLabel("🎵 Мой плейлист"))

        search_row = QHBoxLayout()
        self.inp_search = QLineEdit()
        self.inp_search.setPlaceholderText("Поиск...")
        self.inp_search.textChanged.connect(self.on_search)
        btn_reset = QPushButton("Сбросить")
        btn_reset.clicked.connect(self.reset_search)
        search_row.addWidget(self.inp_search)
        search_row.addWidget(btn_reset)
        layout.addLayout(search_row)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Трек", "Исполнитель", "Настроение", "★"]
        )
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.table.setColumnWidth(0, 40)
        self.table.setColumnWidth(3, 120)
        self.table.setColumnWidth(4, 50)

        self.table.clicked.connect(self.on_row_click)
        layout.addWidget(self.table)

        btn_delete = QPushButton("🗑 Удалить выбранный")
        btn_delete.setStyleSheet(
            "background:#e53935; color:white; font-weight:bold;"
            "padding:6px; border-radius:6px;"
        )
        btn_delete.clicked.connect(self.delete_track)
        layout.addWidget(btn_delete)

        self.form_label = QLabel("Добавить трек:")
        self.form_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(self.form_label)

        form = QHBoxLayout()

        self.inp_title = QLineEdit()
        self.inp_title.setPlaceholderText("Название...")

        self.inp_artist = QLineEdit()
        self.inp_artist.setPlaceholderText("Исполнитель...")

        self.inp_mood = QComboBox()
        self.inp_mood.addItems(PlaylistDB.MOODS)

        self.inp_rating = QSpinBox()
        self.inp_rating.setRange(1, 10)
        self.inp_rating.setValue(7)
        self.inp_rating.setPrefix("★ ")

        self.btn_save = QPushButton("Добавить")
        self.btn_save.setStyleSheet(
            "background:#6200ea; color:white; font-weight:bold;"
            "padding:6px 14px; border-radius:6px;"
        )
        self.btn_save.clicked.connect(self.save_track)

        btn_cancel = QPushButton("Отмена")
        btn_cancel.clicked.connect(self.cancel_edit)

        form.addWidget(self.inp_title)
        form.addWidget(self.inp_artist)
        form.addWidget(self.inp_mood)
        form.addWidget(self.inp_rating)
        form.addWidget(self.btn_save)
        form.addWidget(btn_cancel)
        layout.addLayout(form)

    def load_table(self, rows=None):
        if rows is None:
            rows = self.db.get_all()
        self.table.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, val in enumerate([row["id"], row["title"], row["artist"],
                                     row["mood"], row["rating"]]):
                item = QTableWidgetItem(str(val))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                item.setBackground(QColor(MOOD_COLORS.get(row["mood"], "#fff")))
                self.table.setItem(i, j, item)

    def on_row_click(self):
        row = self.table.currentRow()
        if row < 0:
            return

        self.selected_id = int(self.table.item(row, 0).text())
        track = self.db.get_by_id(self.selected_id)

        self.inp_title.setText(track["title"])
        self.inp_artist.setText(track["artist"] or "")
        self.inp_mood.setCurrentText(track["mood"])
        self.inp_rating.setValue(track["rating"])

        self.form_label.setText(f'✏️ Редактировать: {track["title"]}')
        self.btn_save.setText("Сохранить")
        self.btn_save.setStyleSheet(
            "background:#f57c00; color:white; font-weight:bold;"
            "padding:6px 14px; border-radius:6px;"
        )

    def save_track(self):
        title = self.inp_title.text().strip()
        if not title:
            QMessageBox.warning(self, "Ошибка", "Введи название!")
            return

        if self.selected_id:
            self.db.update(
                self.selected_id, title,
                self.inp_artist.text().strip(),
                self.inp_mood.currentText(),
                self.inp_rating.value()
            )
        else:
            self.db.add(
                title, self.inp_artist.text().strip(),
                self.inp_mood.currentText(), self.inp_rating.value()
            )

        self.cancel_edit()
        self.load_table()

    def delete_track(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Удаление", "Выбери трек в таблице!")
            return
        title    = self.table.item(row, 1).text()
        track_id = int(self.table.item(row, 0).text())
        reply = QMessageBox.question(
            self, "Удалить?", f'Удалить "{title}"?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.db.delete(track_id)
            self.cancel_edit()
            self.load_table()

    def cancel_edit(self):
        self.selected_id = None
        self.inp_title.clear()
        self.inp_artist.clear()
        self.inp_rating.setValue(7)
        self.inp_mood.setCurrentIndex(0)
        self.form_label.setText("Добавить трек:")
        self.btn_save.setText("Добавить")
        self.btn_save.setStyleSheet(
            "background:#6200ea; color:white; font-weight:bold;"
            "padding:6px 14px; border-radius:6px;"
        )
        self.table.clearSelection()

    def on_search(self, text: str):
        if text.strip():
            self.load_table(self.db.search(text.strip()))
        else:
            self.load_table()

    def reset_search(self):
        self.inp_search.clear()
        self.load_table()

    def closeEvent(self, event):
        self.db.close()
        event.accept()


def main():
    app = QApplication(sys.argv)
    w = PlaylistWindow()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()