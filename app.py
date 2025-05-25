#!/venv/bin/python3


from markupsafe import Markup
from flask import Flask, render_template
from datetime import datetime
import markdown
from markdown.extensions.footnotes import FootnoteExtension
import re
import os
import frontmatter

app = Flask(__name__)


POSTS_DIR = 'posts'


@app.route('/')
def index():
    posts = []
    for post in os.listdir(POSTS_DIR):
        if post.endswith(".md"):
            post_path = os.path.join(POSTS_DIR, post)
            with open(post_path, 'r') as f:
                parsed_post = frontmatter.load(f)
                post_date = parsed_post.get('date')
                if post_date:
                    post_date = datetime.strptime(post_date, '%Y-%m-%d')
                else:
                    post_date = datetime.fromtimestamp(os.path.getctime(post_path))
            posts.append((post, post_date))

    sorted_posts = sorted(posts, key=lambda x: x[1], reverse=True)

    processed_posts = [
        {
            "url": post[0][:-3],
            "title": post[0][:-3].replace('_', ' '),
            'date': post[1].strftime('%Y-%m-%d'),
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
        parsed_post = frontmatter.load(f)
        content = parsed_post.content
        title = parsed_post.get('title', post_name.replace('_', ' '))
        subtitle = parsed_post.get('subtitle')
        date = parsed_post.get('date')
        if date:
            date = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d')
        else:
            date = datetime.fromtimestamp(os.path.getctime(post_path)).strftime('%Y-%m-%d')

        if subtitle == None:
            subtitle = ' '

    # Reemplazar las etiquetas {marginnote} y {/marginnote} con HTML
    content = re.sub(r'\{marginnote\}(.*?)\{\/marginnote\}', r'<span class="marginnote">\1</span>', content)

    html_content = Markup(markdown.markdown(content, extensions=[FootnoteExtension()]))
    return render_template('post.html', content=html_content, title=title, date=date, subtitle=subtitle)


@app.route('/debug/posts')
def debug_posts():
    files = os.listdir(POSTS_DIR)
    return f"Archivos disponibles: {files}"


if __name__ == '__main__':
    app.run(debug=True)
