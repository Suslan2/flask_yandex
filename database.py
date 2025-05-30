import sqlite3

def init_db():
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT,
            content TEXT,
            approved INTEGER DEFAULT 0,
            date TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookmarks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            news_id INTEGER
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            news_id INTEGER,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()


def add_news(author, content, date):
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO news (author, content, date) VALUES (?, ?, ?)", (author, content, date))
    news_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return news_id


def get_approve_news(news_id):
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE news SET approved = 1 WHERE id = ?", (news_id,))
    conn.commit()
    conn.close()

def reject_news(news_id):
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM news WHERE id = ?", (news_id,))
    conn.commit()
    conn.close()

def get_approved_news():
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM news WHERE approved = 1 ORDER BY id DESC")
    data = cursor.fetchall()
    conn.close()
    return data

def add_comment(news_id, content):
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO comments (news_id, content) VALUES (?, ?)", (news_id, content))
    conn.commit()
    conn.close()

def select_news():
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()
    s = cursor.execute("SELECT author, content FROM news").fetchall()
    conn.commit()
    conn.close()
    return s
def get_comments(news_id):
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM comments WHERE news_id = ?", (news_id,))
    comments = cursor.fetchall()
    conn.close()
    return comments

def like_news(news_id):
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE news SET likes = likes + 1 WHERE id = ?", (news_id,))
    conn.commit()
    conn.close()

def add_bookmark(news_id):
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM bookmarks WHERE news_id = ?", (news_id,))
    exists = cursor.fetchone()

    if not exists:
        cursor.execute("INSERT INTO bookmarks (news_id) VALUES (?)", (news_id,))
        conn.commit()

    conn.close()


def get_bookmarked_news():
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT news.* FROM news
        JOIN bookmarks ON news.id = bookmarks.news_id
        WHERE news.approved = 1
    """)
    bookmarked = cursor.fetchall()
    conn.close()
    return bookmarked
