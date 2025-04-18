from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    with open("news.json", "rt", encoding="utf8") as f:
        news_list = json.loads(f.read())
    title = "Новости"
    return render_template('base.html', title=title, news =news_list)

if __name__ == '__main__':
    app.run(debug=True)
