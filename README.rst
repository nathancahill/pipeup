PipeUp
======

PipeUp is a command line tool for piping to a webpage.

.. code-block:: bash

    $ tail -f /var/log/nginx/access.log | pipeup

Installation
------------

To install PipeUp, simply:

.. code-block:: bash

    $ pip install pipeup

Usage
-----

Pipe the output of a command to ``pipeup``. See available options by running ``pipeup --help``

.. code-block:: bash

    $ command | pipeup

Server
------

To run your own server, install PipeUp from source:

.. code-block:: bash

    $ git clone git@github.com:nathancahill/pipeup.git
    $ cd pipeup
    $ pip install -r requirements-server.txt
    $ cd pipeup/server
    $ cp config.example.py config.py

Edit ``config.py`` with the complete URL of your server. Then run the Tornado server:

.. code-block:: bash

    $ python server.py

To use the ``pipeup`` client with your server, pass the websocket URL as ``--server``:

.. code-block:: bash

    $ command | pipeup --server ws://127.0.0.1:8888/ws

For a more permanent installation, put Tornado behind Nginx using the ``nginx.conf`` file.

Contributing
------------

Pull requests are gladly accepted. Keep it simple.
