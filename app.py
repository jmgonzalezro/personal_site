from markupsafe import Markup
from flask import Flask, render_template
from datetime import datetime
import markdown
import os

app = Flask(__name__)


POSTS_DIR = 'posts'


@app.route('/')
def index():
    posts = [
        (post, os.path.getctime(os.path.join(POSTS_DIR, post)))
        for post in os.listdir(POSTS_DIR)
        if post.endswith(".md")
    ]
    sorted_posts = sorted(posts, key=lambda x: x[1])
    processed_posts = [
        {
            "url": post[0][:-3],
            "title": post[0][:-3].replace('_', ' '),
            'date': datetime.fromtimestamp(post[1]).strftime('%Y-%m-%d'),
        }
        for post in sorted_posts
    ]
    return render_template('index.html', posts=processed_posts)


@app.route('/posts/<post_name>')
def post(post_name):
    post_path = f'{POSTS_DIR}/{post_name}.md'
    if not os.path.exists(post_path):
        return 'Post not found', 404
    with open(post_path, 'r') as f:
        content = f.read()
        html_content = Markup(markdown.markdown(content))
    post_title = post_name.replace('_', ' ')
    post_date = datetime.fromtimestamp(os.path.getctime(post_path)).strftime('%Y-%m-%d')
    return render_template('post.html', content=html_content, title=post_title, date=post_date)


@app.route('/debug/posts')
def debug_posts():
    files = os.listdir(POSTS_DIR)
    return f"Archivos disponibles: {files}"


if __name__ == '__main__':
    app.run(debug=True)
