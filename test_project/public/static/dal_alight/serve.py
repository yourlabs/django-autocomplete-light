import os
import urllib

from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server


choices = ['aaa', 'aab', 'abb', 'bbb']

PAGE_SIZE = 2

# Map URL basenames to their paths inside the package static directory.
STATIC_FILE_MAP = {
    'autocomplete-light.js': 'autocomplete_light/static/autocomplete_light/autocomplete-light.js',
    'autocomplete-light.css': 'autocomplete_light/static/autocomplete_light/autocomplete-light.css',
}


def choices_get(environ):
    data = urllib.parse.parse_qs(environ['QUERY_STRING'])
    q = data.get('q', [''])[0]
    selected = data.get('_', [])
    html = '\n'.join([
        f'<div data-value="{i}">{choice}</div>'
        for i, choice in enumerate(choices)
        if choice.startswith(q)
        and str(i) not in selected
    ])
    return html, 'text/html'


def choices_paginated(environ):
    data = urllib.parse.parse_qs(environ['QUERY_STRING'])
    q = data.get('q', [''])[0]
    page = int(data.get('page', ['1'])[0])
    filtered = [
        (i, c) for i, c in enumerate(choices)
        if c.startswith(q)
    ]
    start = (page - 1) * PAGE_SIZE
    end = start + PAGE_SIZE
    html = '\n'.join([
        f'<div data-value="{i}">{choice}</div>'
        for i, choice in filtered[start:end]
    ])
    if end < len(filtered):
        html += f'\n<div data-next-page="{page + 1}">Load more</div>'
    return html, 'text/html'


def choices_create(environ):
    data = urllib.parse.parse_qs(environ['QUERY_STRING'])
    q = data.get('q', [''])[0]
    selected = data.get('_', [])
    html = '\n'.join([
        f'<div data-value="{i}">{choice}</div>'
        for i, choice in enumerate(choices)
        if choice.startswith(q)
        and str(i) not in selected
    ])
    if q:
        html += f'\n<div data-create="true">Create "{q}"</div>'
    return html, 'text/html'


def static(environ):
    ctype = 'text/html'
    if len(environ['PATH_INFO']) > 1:
        path = environ['PATH_INFO'][1:]
        path = STATIC_FILE_MAP.get(path, path)
        if path.endswith('.css'):
            ctype = 'text/css'
        elif path.endswith('.js'):
            ctype = 'text/javascript'
    else:
        path = 'index.html'
    if os.path.exists(path):
        with open(path, 'r') as f:
            html = f.read()
    else:
        html = f'{path} not found'
    return html, ctype


def application(environ, start_response):
    setup_testing_defaults(environ)
    path = environ['PATH_INFO']
    if environ['QUERY_STRING']:
        if path.startswith('/page'):
            html, ctype = choices_paginated(environ)
        elif path.startswith('/create'):
            html, ctype = choices_create(environ)
        else:
            html, ctype = choices_get(environ)
    else:
        html, ctype = static(environ)
    body = html.encode('utf8')
    status = '200 OK'
    headers = [('Content-type', ctype)]
    start_response(status, headers)
    return [body]


with make_server('', 8000, application) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()
