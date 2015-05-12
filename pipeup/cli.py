
import sys

from clint import arguments
from clint.textui import colored, puts
from websocket import create_connection


def main():
    args = arguments.Args()
    server = args.get(0)

    if not server:
        server = 'ws://pipeup.io:8888/ws'

    ws = create_connection(server)

    while True:
        url = ws.recv()

        if url:
            break

    puts(colored.green('Piping to ' + url))

    while True:
        try:
            line = sys.stdin.readline()
            ws.send(line)
        except KeyboardInterrupt:
            break

        if not line:
            break

    ws.close()
