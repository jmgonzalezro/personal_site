#!/venv/bin/python3


from markupsafe import Markup
from flask import Flask, render_template, request, make_response
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
                post_date = parsed_post.get('date', datetime.now()),
                if post_date:
                    pass
                elif post_date:
                    post_date = datetime.fromtimestamp(os.path.getctime(post_path))
            posts.append((post, post_date))

    sorted_posts = sorted(posts, key=lambda x: x[1], reverse=True)

    page = request.args.get('page', 1, type=int)
    per_page = 5
    start = (page - 1) * per_page
    end = start + per_page
    paginated_posts = sorted_posts[start:end]

    processed_posts = [
        {
            "url": post[0][:-3],
            "title": post[0][:-3].replace('_', ' '),
            'date': post[1],
        }
        for post in paginated_posts
    ]
    total_pages = (len(sorted_posts) + per_page - 1) // per_page

    response = make_response(render_template('index.html', posts=processed_posts, page=page, total_pages=total_pages))
    return set_no_cache_headers(response)


def set_no_cache_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


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
            pass
            # date = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d')
        else:
            date = datetime.fromtimestamp(os.path.getctime(post_path)).strftime('%Y-%m-%d')

        if subtitle is None:
            subtitle = ' '

    # Reemplazar las etiquetas {marginnote} y {/marginnote} con HTML
    content = re.sub(r'\{marginnote\}(.*?)\{\/marginnote\}', r'<span class="marginnote">\1</span>', content)

    html_content = Markup(markdown.markdown(content, extensions=[FootnoteExtension()]))
    response = make_response(render_template('post.html', content=html_content, title=title, date=date, subtitle=subtitle))
    return set_no_cache_headers(response)


@app.route('/debug/posts')
def debug_posts():
    files = os.listdir(POSTS_DIR)
    return f"Archivos disponibles: {files}"


if __name__ == '__main__':
    app.run(debug=True)
