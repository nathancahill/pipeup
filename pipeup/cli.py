
import json
import sys

from clint import arguments
from clint.textui import colored, puts
from websocket import create_connection


def main():
    args = arguments.Args()
    server = args.get(0)

    if not server:
        server = 'ws://pipeup.io/ws'

    ws = create_connection(server)

    while True:
        msg = ws.recv()

        if msg:
            break

    message = json.loads(msg)
    puts(colored.green('Piping to ' + message['msg']))

    while True:
        try:
            line = sys.stdin.readline()
            ws.send(line)
        except KeyboardInterrupt:
            break

        if not line:
            break

    ws.close()
