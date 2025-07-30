import sqlite3
from logger_config import setup_logger

logger = setup_logger("parser")
DB_PATH = "reviews.db"

def create_table():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id TEXT PRIMARY KEY,
            branch_id TEXT,
            author TEXT,
            date_created TEXT,
            rating INTEGER,
            text TEXT
        )
    """)
    conn.commit()
    conn.close()

def init_db():
    create_table()

def is_review_exists(review_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM reviews WHERE id = ?", (review_id,))
    found = cur.fetchone()
    conn.close()
    return found is not None

def save_review(review, branch_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT OR IGNORE INTO reviews 
            (id, branch_id, author, date_created, rating, text)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            review.get("id"),
            branch_id,
            review.get("user", {}).get("name", "Неизвестный автор"),
            review.get("date_created"),
            review.get("rating"),
            review.get("text")
        ))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"Ошибка при сохранении в базу: {e}")
    finally:
        conn.close()
