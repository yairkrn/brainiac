import contextlib
import multiprocessing
import pathlib
import signal
import socket
import subprocess
import sys
import threading
import time

import pytest


_SERVER_ADDRESS = '127.0.0.1', 5000
_SERVER_BACKLOG = 1000
_ROOT = pathlib.Path(__file__).absolute().parent.parent
_SERVER_PATH = 'brainiac'
_CLIENT_PATH = 'brainiac'


def test_client():
    def run_server():
        server = socket.socket()
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(_SERVER_ADDRESS)
        server.listen(_SERVER_BACKLOG)
        try:
            while True:
                connection, address = server.accept()
                connection.close()
        except KeyboardInterrupt:
            pass
        finally:
            server.close()
    server = multiprocessing.Process(target=run_server)
    server.start()
    try:
        time.sleep(0.5)
        host, port = _SERVER_ADDRESS
        process = subprocess.Popen(
            ['python', '-m', _CLIENT_PATH, 'upload-thought', '-a', f'{host}:{port}', '-u', '1', "I'm hungry"],
            stdout = subprocess.PIPE,
            cwd = _ROOT
        )
        stdout, _ = process.communicate()
        assert b'done' in stdout.lower()
        process = subprocess.Popen(
            ['python', '-m', _CLIENT_PATH, 'unknown_command'],
            stderr = subprocess.PIPE,
            cwd = _ROOT
        )
        _, stderr = process.communicate()
        assert b'usage' in stderr.lower()
    finally:
        server.terminate()


def test_server():
    host, port = _SERVER_ADDRESS
    process = subprocess.Popen(
        ['python', '-m', _SERVER_PATH, 'run-server', '-a', f'{host}:{port}', 'data/'],
        stdout = subprocess.PIPE,
        cwd = _ROOT
    )
    stdout = None
    def run_server():
        nonlocal stdout
        stdout, _ = process.communicate()
    thread = threading.Thread(target=run_server)
    thread.start()
    time.sleep(2)
    try:
        connection = socket.socket()
        connection.connect(_SERVER_ADDRESS)
        connection.close()
    finally:
        process.send_signal(signal.SIGINT)
        thread.join()


@contextlib.contextmanager
def _argv(*args):
    command = lambda: None
    try:
        argv = sys.argv[1:]
        sys.argv[1:] = args
        yield command
    except SystemExit as e:
        command.exit_code = e.args[0] if e.args else 0
    finally:
        sys.argv[1:] = argv
