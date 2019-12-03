![build status](https://travis-ci.org/yairkrn/virtual-brain.svg?branch=master)
[![codecov](https://codecov.io/gh/yairkrn/virtual-brain/branch/master/graph/badge.svg)](https://codecov.io/gh/yairkrn/virtual-brain)

# Virtual Brain

An example package. See [full documentation](https://virtual-brain.readthedocs.io/en/latest/).

## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:yairkrn/virtual-brain.git
    ...
    $ cd virtual-brain/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [virtual-brain] $ # you're good to go!
    ```

3. To check that everything is working as expected, run the tests:


    ```sh
    $ pytest tests/
    ...
    ```

## Usage

The `virtualbrain` packages provides the following classes:

- `Thought`

    This class describes a user's thought, consisting of:
    1. Timestamp
    2. The user's unique identifier (int)
    3. The thought's content (string)

    The thought can be serialized and deserialized to and from bytes.
    
    Example:
    ```pycon
	>>> import datetime as dt
	>>> from virtualbrain import Thought
	>>> t = Thought(user_id=1337, timestamp=dt.datetime(1998, 12, 7), thought='What a nice day...')
	>>> t
	Thought(user_id=1337, timestamp=datetime.datetime(1998, 12, 7, 0, 0), thought="What a nice day...")
	>>> t_bytes = t.serialize()
	>>> t_bytes
	b'9\x05\x00\x00\x00\x00\x00\x00`\xfej6\x00\x00\x00\x00\x12\x00\x00\x00What a nice day...'
	>>> Thought.deserialize(t_bytes) == t
	True
    ```


The `virtualbrain` package also provides the following functions, which also server as cli commands:

```sh
python -m virtualbrain --help
Usage: __main__.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  run-server
  run-webserver
  upload-thought
```

- `run-server`
	```sh
	python -m virtualbrain run-server --help
	Usage: __main__.py run-server [OPTIONS] DATA

	Options:
	  -a, --address TEXT  [required]
	  --help              Show this message and exit.
	```
