
import datetime
import json
import string
import random

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
from tornado.options import define, options

import redis
from Pubnub import Pubnub

from config import SERVER_URL, LINES_LIMIT, PUBNUB_SUBSCRIBE_KEY, PUBNUB_PUBLISH_KEY


define('port', default=8888, help='run on the given port', type=int)

r = redis.StrictRedis()
pubnub = Pubnub(publish_key=PUBNUB_PUBLISH_KEY, subscribe_key=PUBNUB_SUBSCRIBE_KEY)


def random_string(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def pubnub_write(key, action, msg):
    pubnub.publish(key, json.dumps(dict(action=action, key=key, msg=msg)))


class WSHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        self.key = None
        self.ip = self.request.remote_ip
        self.lines = 0
        self.pro = False

        if 'User-Agent' not in self.request.headers:
            self.type = 'client'
        else:
            self.type = 'listener'

    def on_message(self, message):
        try:
            msg = json.loads(message)
        except:
            return

        if self.type != 'client':
            return

        if msg['action'] == 'request':
            if msg['key'] and len(msg['key']) == 6 and \
                              msg['key'].isalnum() and \
                              not r.sismember('pipes', msg['key']):
                self.key = msg['key']
            else:
                self.key = random_string()

            r.sadd('pipes', self.key)
            r.lpush('log', self.ip + ' - ' + self.key + ' - ' + datetime.datetime.now().isoformat())

            if r.sismember('pro', msg['key']):
                self.pro = True

            self.write('connected', SERVER_URL + self.key)

        elif msg['action'] == 'send':
            self.lines += 1

            if not self.pro and self.lines >= LINES_LIMIT:
                self.write('limited', 'You hit the 2,000 line limit. Please upgrade your account.')
                pubnub_write(self.key, 'limited', 'You hit the 2,000 line limit. Please upgrade your account.\n')
            else:
                pubnub_write(self.key, 'update', msg['msg'])

    def on_close(self):
        if self.type != 'client':
            return

        pubnub_write(self.key, 'close', 'Client ended stream.\n')
        r.srem('pipes', self.key)

    def write(self, action, msg):
        try:
            self.write_message(json.dumps(dict(action=action, key=self.key, msg=msg)))
        except:
            pass


class SignupHandler(tornado.web.RequestHandler):
    def post(self):
        email = self.get_argument('email', None)

        if email:
            r.sadd('signups', email)

        self.write('OK')


class StreamHandler(tornado.web.RequestHandler):
    def get(self, key):
        self.render('static/html/stream.html')


application = tornado.web.Application([
    (r'/signup', SignupHandler),
    (r'/ws', WSHandler),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'static'}),
    (r'/(.*)', StreamHandler),
])


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(options.port, address='127.0.0.1')
    tornado.ioloop.IOLoop.instance().start()
