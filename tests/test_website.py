import datetime as dt
import multiprocessing
import pathlib
import pytest
import shutil
import requests
import time

from virtualbrain import web


_ADDRESS = '127.0.0.1', 8000
_URL = f'http://{_ADDRESS[0]}:{_ADDRESS[1]}'
_ROOT = pathlib.Path(__file__).absolute().parent.parent
_DATA_DIR = _ROOT / 'data'


@pytest.fixture
def webserver():
    _DATA_DIR.mkdir(parents=True, exist_ok=True)

    def run_webserver():
        web.run_webserver(_ADDRESS, _DATA_DIR)
    process = multiprocessing.Process(target=run_webserver)
    process.start()
    time.sleep(0.1)
    try:
        yield
    finally:
        process.terminate()


def test_index(webserver):
    response = requests.get(_URL)
    for user_dir in _DATA_DIR.iterdir():
        assert f'user {user_dir.name}' in response.text
        assert f'users/{user_dir.name}' in response.text


def test_user(webserver):
    for user_dir in _DATA_DIR.iterdir():
        response = requests.get(f'{_URL}/users/{user_dir.name}')
        for thought_file in user_dir.iterdir():
            datetime = dt.datetime.strptime(thought_file.stem, '%Y-%m-%d_%H-%M-%S')
            assert f'User {user_dir.name}' in response.text
            assert f'{datetime:%Y-%m-%d %H:%M:%S}' in response.text
            thought_file.read_text() in response.text


def test_invalid_user(webserver):
    for user_id in [112233, 445566]:
        response = requests.get(f'{_URL}/users/{user_id}')
        assert response.status_code == 404
        assert '404 Not Found' in response.text


def test_invalid_path(webserver):
    response = requests.get(f'{_URL}/hello')
    assert response.status_code == 404
    assert '404 Not Found' in response.text


def test_dynamic(webserver):
    user_id = 0
    user_dir = _DATA_DIR / str(user_id)
    user_dir.mkdir()
    try:
        datetime = dt.datetime(2000, 1, 1, 12, 0, 0)
        thought = 'Hello, world!'
        thought_file = user_dir / f'{datetime:%Y-%m-%d_%H-%M-%S}.txt'
        thought_file.write_text(thought)
        response = requests.get(_URL)
        assert f'user {user_dir.name}' in response.text
        assert f'users/{user_dir.name}' in response.text
        response = requests.get(f'{_URL}/users/{user_id}')
        assert f'User {user_dir.name}' in response.text
        assert f'{datetime:%Y-%m-%d %H:%M:%S}' in response.text
        assert thought_file.read_text() in response.text
    finally:
        shutil.rmtree(user_dir)


def test_web():
    _DATA_DIR.mkdir(parents=True, exist_ok=True)

    def run_webserver():
        web.run_webserver(_ADDRESS, _DATA_DIR)
    process = multiprocessing.Process(target=run_webserver)
    process.start()
    time.sleep(0.1)
    try:
        response = requests.get(_URL)
        for user_dir in _DATA_DIR.iterdir():
            assert f'user {user_dir.name}' in response.text
        for user_dir in _DATA_DIR.iterdir():
            response = requests.get(f'{_URL}/users/{user_dir.name}')
            assert f'User {user_dir.name}' in response.text
            for thought_file in user_dir.iterdir():
                assert thought_file.read_text() in response.text
    finally:
        process.terminate()
