from flask import Flask, render_template, request, redirect, url_for
from database import get_comments, add_comment, add_bookmark, get_bookmarked_news
import sqlite3

app = Flask(__name__)

def get_news_with_stats():
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM news WHERE approved = 1 ORDER BY id DESC LIMIT 3")
    fresh = cursor.fetchall()

    cursor.execute("""
        SELECT news.* FROM news
        JOIN bookmarks ON news.id = bookmarks.news_id
        WHERE news.approved = 1
        ORDER BY bookmarks.id DESC
    """)
    popular = cursor.fetchall()

    cursor.execute("""
        SELECT news.id, news.author, news.content, news.approved, news.date, COUNT(comments.id) as comments_count
        FROM news
        LEFT JOIN comments ON news.id = comments.news_id
        WHERE news.approved = 1
        GROUP BY news.id
        ORDER BY comments_count DESC
        LIMIT 3
    """)
    discussed = cursor.fetchall()

    conn.close()
    return fresh, popular, discussed

@app.route('/')
def index():
    fresh, popular, discussed = get_news_with_stats()

    search_query = request.args.get('q', '')
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()

    if search_query:
        cursor.execute("SELECT * FROM news WHERE approved = 1 AND content LIKE ?", (f"%{search_query}%",))
    else:
        cursor.execute("SELECT * FROM news WHERE approved = 1 ORDER BY id DESC")

    all_news = cursor.fetchall()
    conn.close()

    return render_template(
        'base.html',
        all_news=all_news,
        fresh=fresh,
        popular=popular,
        discussed=discussed,
        search_query=search_query,
        get_comments=get_comments
    )

@app.route('/comment/<int:news_id>', methods=['POST'])
def add_comment_route(news_id):
    comment = request.form['comment']
    add_comment(news_id, comment)
    return redirect(url_for('index'))

@app.route('/bookmark/<int:news_id>', methods=['POST'])
def bookmark(news_id):
    add_bookmark(news_id)
    return redirect(url_for('index'))

@app.route('/bookmarks')
def bookmarks():
    bookmarked = get_bookmarked_news()
    return render_template('base.html',
                           all_news=bookmarked,
                           fresh=[],
                           popular=[],
                           discussed=[],
                           search_query='',
                           get_comments=get_comments)

if __name__ == '__main__':
    app.run(debug=True)
