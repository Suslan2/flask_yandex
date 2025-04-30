from flask import Flask, render_template, request, redirect, url_for
from database import get_approved_news, get_comments, like_news, add_comment
import sqlite3

app = Flask(__name__)


def get_news_with_stats():
    conn = sqlite3.connect("news.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM news WHERE approved = 1 ORDER BY id DESC LIMIT 3")
    fresh = cursor.fetchall()

    cursor.execute("SELECT * FROM news WHERE approved = 1 ORDER BY likes DESC LIMIT 3")
    popular = cursor.fetchall()

    cursor.execute("""SELECT news.*, COUNT(comments.id) as comments_count 
                    FROM news LEFT JOIN comments ON news.id = comments.news_id 
                    WHERE approved = 1 
                    GROUP BY news.id 
                    ORDER BY comments_count DESC LIMIT 3""")
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


@app.route('/like/<int:news_id>', methods=['POST'])
def like(news_id):
    from database import like_news
    like_news(news_id)
    return redirect(url_for('index'))


@app.route('/comment/<int:news_id>', methods=['POST'])
def add_comment(news_id):
    from database import add_comment
    comment = request.form['comment']
    add_comment(news_id, comment)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
