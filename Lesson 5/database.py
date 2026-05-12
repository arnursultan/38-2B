import sqlite3


class PlaylistDB:

    MOODS = ["🔥 Hype", "😌 Chill", "😢 Sad", "💪 Workout"]

    def __init__(self, path="playlist.db"):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._init()
        self._seed()

    def _init(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tracks (
                id     INTEGER PRIMARY KEY AUTOINCREMENT,
                title  TEXT NOT NULL,
                artist TEXT,
                mood   TEXT DEFAULT '😌 Chill',
                rating INTEGER DEFAULT 5
            )
        """)
        self.conn.commit()

    def _seed(self):
        self.cursor.execute("SELECT COUNT(*) FROM tracks")
        if self.cursor.fetchone()[0] == 0:
            data = [
                ("Blinding Lights", "The Weeknd", "🔥 Hype",    10),
                ("Lose Yourself",   "Eminem",     "💪 Workout",  9),
                ("Someone Like You","Adele",       "😢 Sad",      9),
                ("Levitating",      "Dua Lipa",    "😌 Chill",    8),
            ]
            self.cursor.executemany(
                "INSERT INTO tracks (title, artist, mood, rating) VALUES (?,?,?,?)", data
            )
            self.conn.commit()

    def add(self, title: str, artist: str, mood: str, rating: int):
        self.cursor.execute(
            "INSERT INTO tracks (title, artist, mood, rating) VALUES (?,?,?,?)",
            (title, artist, mood, rating)
        )
        self.conn.commit()

    def get_all(self) -> list:
        self.cursor.execute("SELECT * FROM tracks ORDER BY rating DESC")
        return self.cursor.fetchall()

    def search(self, query: str) -> list:
        self.cursor.execute(
            "SELECT * FROM tracks WHERE title LIKE ? OR artist LIKE ? ORDER BY rating DESC",
            (f"%{query}%", f"%{query}%")
        )
        return self.cursor.fetchall()

    def delete(self, track_id: int):
        self.cursor.execute("DELETE FROM tracks WHERE id = ?", (track_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()