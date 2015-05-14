
import json
import logging
import sys
import time
from threading import Thread

import click

from websocket import WebSocketApp, WebSocketConnectionClosedException

logging.basicConfig()


def on_message(ws, msg):
    message = json.loads(msg)

    if message['action'] == 'connected':
        click.echo(click.style('Piping to ' + message['msg'], fg='green'))


def on_error(ws, error):
    pass


def on_close(ws):
    click.echo(click.style('Lost connection.', fg='red'))

def wrapper(key):
    def on_open(ws):
        click.echo(click.style('Connected.', fg='green'))

        def run(key):
            ws.send(json.dumps(dict(action='request', key=key)))

            while True:
                try:
                    line = sys.stdin.readline()
                    ws.send(json.dumps(dict(action='send', msg=line)))
                except KeyboardInterrupt:
                    break
                except WebSocketConnectionClosedException:
                    break

                if not line.strip():
                    break

            ws.close()

        Thread(target=run, args=(key,)).start()

    return on_open


@click.command()
@click.option('--server', default='ws://pipeup.io/ws', help='Websocket URL to pipe to.')
@click.option('--key', default=None, help='Key on the server to pipe to.')
def main(server, key):
    click.echo('')

    for i in range(10):
        click.echo('Connecting...')

        try:
            ws = WebSocketApp(server,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close,
                              on_open=wrapper(key))

            ws.run_forever(ping_interval=15)
        except KeyboardInterrupt:
            break
        except:
            pass

        time.sleep(i * 1.5 + 1.5)
    else:
        click.echo(click.style('Failed to reconnect.', fg='red'))
        sys.exit()
