from markupsafe import Markup
from flask import Flask, render_template
from datetime import datetime
import markdown
import os
from nbconvert import HTMLExporter
import nbformat
from traitlets.config import Config

app = Flask(__name__)


POSTS_DIR = 'posts'


@app.route('/')
def index():
    posts = [
        (post, os.path.getctime(os.path.join(POSTS_DIR, post)))
        for post in os.listdir(POSTS_DIR)
        if post.endswith(".md") or post.endswith(".ipynb")
    ]
    sorted_posts = sorted(posts, key=lambda x: x[1], reverse=True)
    processed_posts = [
        {
            "url": post[0].split('.')[0],
            "title": post[0].split('.')[0].replace('_', ' '),
            'date': datetime.fromtimestamp(post[1]).strftime('%Y-%m-%d'),
        }
        for post in sorted_posts
    ]
    return render_template('index.html', posts=processed_posts)


@app.route('/posts/<post_name>')
def post(post_name):
    post_path = f'{POSTS_DIR}/{post_name}.ipynb'
    if not os.path.exists(post_path):
        return 'Post not found', 404

    with open(post_path, 'r') as f:
        notebook_content = nbformat.read(f, as_version=4)
        html_exporter = HTMLExporter()
        html_exporter.exclude_input = True
        html_content, _ = html_exporter.from_notebook_node(notebook_content)

    # Envolver el contenido en un contenedor
    html_content = f'<div class="notebook-content">{html_content}</div>'

    # Extraer título y subtítulo
    post_title = None
    post_subtitle = None
    for cell in notebook_content['cells']:
        if cell['cell_type'] == 'markdown':
            lines = cell['source'].splitlines()
            for line in lines:
                if line.startswith('# ') and not post_title:
                    post_title = line[2:].strip()
                elif line.startswith('## ') and not post_subtitle:
                    post_subtitle = line[3:].strip()
                if post_title and post_subtitle:
                    break
        if post_title and post_subtitle:
            break

    if not post_title:
        post_title = post_name.replace('_', ' ')
    if not post_subtitle:
        post_subtitle = "Subtítulo no disponible"

    post_date = datetime.fromtimestamp(os.path.getctime(post_path)).strftime('%Y-%m-%d')
    return render_template('post.html', content=html_content, title=post_title, subtitle=post_subtitle, date=post_date)


@app.route('/debug/posts')
def debug_posts():
    files = os.listdir(POSTS_DIR)
    return f"Archivos disponibles: {files}"


@app.route('/debug/html/<post_name>')
def debug_html(post_name):
    post_path = f'{POSTS_DIR}/{post_name}.ipynb'
    if not os.path.exists(post_path):
        return 'Post not found', 404

    with open(post_path, 'r') as f:
        notebook_content = nbformat.read(f, as_version=4)
        html_exporter = HTMLExporter()
        html_exporter.exclude_input = True
        html_content, _ = html_exporter.from_notebook_node(notebook_content)

    return html_content  # Devuelve el HTML generado para inspección


if __name__ == '__main__':
    app.run(debug=True)
