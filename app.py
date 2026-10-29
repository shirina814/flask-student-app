
from flask import Flask, render_template
import sqlite3
from pathlib import Path

app = Flask(__name__)
DB_PATH = Path(__file__).with_name("students.db")


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                course TEXT NOT NULL
            )
        """)

        count = conn.execute(
            "SELECT COUNT(*) FROM students"
        ).fetchone()[0]

        if count == 0:
            conn.executemany(
                "INSERT INTO students (name, course) VALUES (?, ?)",
                [
                    ("Aisha", "CSE"),
                    ("Rahul", "ECE"),
                    ("Priya", "IT")
                ]
            )


@app.route("/")
def home():
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        students = conn.execute(
            "SELECT id, name, course FROM students"
        ).fetchall()

    return render_template("index.html", students=students)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)