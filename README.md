![build status](https://travis-ci.org/yairkrn/brainiac.svg?branch=master)
[![codecov](https://codecov.io/gh/yairkrn/brainiac/branch/master/graph/badge.svg)](https://codecov.io/gh/yairkrn/brainiac)

# Brainiac

Final project for Advanced System Design Course.

See [full documentation](https://brainiac.readthedocs.io/en/latest/).

## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:yairkrn/brainiac.git
    ...
    $ cd brainiac/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [brainiac] $ # you're good to go!
    ```

3. To check that everything is working as expected, run the tests:


    ```sh
    $ pytest tests/
    ...
    ```

## Usage

The `brainiac` package provides the following classes:

- `Thought`

    This class describes a user's thought, consisting of:
    1. Timestamp
    2. The user's unique identifier (int)
    3. The thought's content (string)

    The thought can be serialized and deserialized to and from bytes.
    
    Example:
    ```pycon
	>>> import datetime as dt
	>>> from brainiac import Thought
	>>> t = Thought(user_id=1337, timestamp=dt.datetime(1998, 12, 7), thought='What a nice day...')
	>>> t
	Thought(user_id=1337, timestamp=datetime.datetime(1998, 12, 7, 0, 0), thought="What a nice day...")
	>>> t_bytes = t.serialize()
	>>> t_bytes
	b'9\x05\x00\x00\x00\x00\x00\x00`\xfej6\x00\x00\x00\x00\x12\x00\x00\x00What a nice day...'
	>>> Thought.deserialize(t_bytes) == t
	True
    ```


The `brainiac` package also provides the following functions, which also serve as cli commands:

```sh
$ python -m brainiac --help
Usage: __main__.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  run-server
  run-webserver
  upload-thought
```

- `run_server(address, data_dir)`
	```sh
	$ python -m brainiac run-server --help
	Usage: __main__.py run-server [OPTIONS] DATA_DIR

	  Run the thought server, which accepts and stores thoughts.

	Options:
	  -a, --address TEXT  The server's address, in format <ip>:<port>  [required]
	  --help              Show this message and exit.
	```

- `run_webserver(address, data_dir)`
	```sh
	$ python -m brainiac run-webserver --help
	Usage: __main__.py run-webserver [OPTIONS] DATA_DIR

	  Run the web server, which keeps track of stored thoughts.

	Options:
	  -a, --address TEXT  The server's address, in format <ip>:<port>  [required]
	  --help              Show this message and exit.
	```

- `upload_thought(address, user_id)`
	```sh
	$ python -m brainiac upload-thought --help
	Usage: __main__.py upload-thought [OPTIONS] THOUGHT

	  Upload a thought to the thought server.

	Options:
	  -a, --address TEXT     The server's address, in format <ip>:<port>
	                         [required]
	  -u, --user-id INTEGER  The user's unique identifying number  [required]
	  --help                 Show this message and exit.
	```