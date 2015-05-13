
import json
import logging
import sys
from threading import Thread

from clint import arguments
from clint.textui import colored, puts
from websocket import WebSocketApp

logging.basicConfig()


def on_message(ws, msg):
    message = json.loads(msg)

    if message['action'] == 'connected':
        puts(colored.green('Piping to ' + message['msg']))


def on_error(ws, error):
    print error


def on_close(ws):
    print 'Lost connection'


def on_open(ws):
    def run(*args):
        while True:
            try:
                line = sys.stdin.readline()
                ws.send(line)
            except KeyboardInterrupt:
                break

            if not line.strip():
                break

        ws.close()

    Thread(target=run).start()


def main():
    args = arguments.Args()
    server = args.get(0)

    if not server:
        server = 'ws://pipeup.io/ws'

    ws = WebSocketApp(server, on_message=on_message, on_error=on_error, on_close=on_close)

    ws.on_open = on_open
    ws.run_forever(ping_interval=15)
