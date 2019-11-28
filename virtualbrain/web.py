import http.server
import re
import os
import functools
from datetime import datetime
from pathlib import Path
import flask


INDEX_HTML = '''
<html>
    <head>
        <title>Brain Computer Interface</title>
    </head>
    <body>
        <ul>
            {users_html}
        </ul>
    </body>
</html>
'''
USER_LINE_HTML = '''
<li><a href="/users/{user_id}">user {user_id}</a></li>
'''
USER_HTML = '''
<html>
    <head>
        <title>Brain Computer Interface: User {user_id}</title>
    </head>
    <body>
        <table>
            {thoughts_html}
        </table>
    </body>
</html>
'''
THOUGHT_HTML = '''
<tr>
    <td>{thought_time}</td>
    <td>{thought_str}</td>
</tr>
'''
TIME_FORMAT_FILE = '%Y-%m-%d_%H-%M-%S'
TIME_FORMAT_HTML = '%Y-%m-%d %H:%M:%S'
VALID_USER_RE = r'\d+'


def is_valid_user_id(user_id, data_dir):
    return re.match(VALID_USER_RE, user_id) and Path(data_dir, user_id).is_dir()


def get_user_ids(data_dir):
    return sorted([user_dir.name for user_dir in Path(data_dir).iterdir() if is_valid_user_id(user_dir.name, data_dir)], key=int)


def get_thought_from_file(thought_file):
    if not thought_file.is_file():
        raise ValueError('Invalid thought: not a file.')
    try:
        thought_time = datetime.strptime(thought_file.stem, TIME_FORMAT_FILE)
    except ValueError:
        raise ValueError('Invalid thought: invalid time format.')
    with open(thought_file, 'rb') as f:
        thought_bytes = f.read()
    return (thought_time, thought_bytes)


def get_user_thoughts(user_id, data_dir):
    user_dir = Path(data_dir, user_id)
    thoughts = []
    for thought_file in Path(user_dir).iterdir():
        try:
            thoughts.append(get_thought_from_file(thought_file))
        except ValueError as e:
            print (e)
    return sorted(thoughts, key = lambda thought: thought[0])  # sort by time


def run_webserver(address, data_dir):
    website = flask.Flask(__name__)

    @website.route('/')
    def get_index_html():
        users_html = [USER_LINE_HTML.format(user_id=user_id) for user_id in get_user_ids(data_dir)]
        return INDEX_HTML.format(users_html=os.linesep.join(users_html))

    @website.route('/users/<int:user_id_int>')
    def get_user_html(user_id_int):
        user_id = str(user_id_int)
        if not is_valid_user_id(user_id, data_dir):
            flask.abort(404)
        thoughts_html = []
        thoughts = get_user_thoughts(user_id, data_dir)
        for thought in thoughts:
            thought_time, thought_bytes = thought
            thought_time_str = thought_time.strftime(TIME_FORMAT_HTML)
            thoughts_html.append(THOUGHT_HTML.format(thought_time=thought_time_str, thought_str=thought_bytes.decode()))
        return USER_HTML.format(user_id=user_id, thoughts_html=os.linesep.join(thoughts_html))

    @website.route('/<path:dummy>')
    def page_not_found(dummy):
        flask.abort(404)

    host, port = address
    website.run(host, port)

