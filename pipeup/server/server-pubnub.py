
import json
import string
import random
import uuid

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

from Pubnub import Pubnub

from config import SERVER_URL, PUBNUB_SUBSCRIBE_KEY, PUBNUB_PUBLISH_KEY

active_keys = set()

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

        if 'User-Agent' not in self.request.headers:
            self.type = 'client'

            print 'opening client ' + self.ip
        else:
            self.type = 'listener'

    def on_message(self, message):
        try:
            msg = json.loads(message)
        except:
            return

        if self.type == 'client':
            if msg['action'] == 'request':
                if msg['key'] and msg['key'] not in active_keys and len(msg['key']) == 6:
                    self.key = msg['key']
                else:
                    self.key = random_string()

                active_keys.add(self.key)
                self.write('connected', SERVER_URL + self.key)

            elif msg['action'] == 'send':
                pubnub_write(self.key, 'update', msg['msg'])

    def on_close(self):
        if self.type == 'client':
            print 'closing client'

            pubnub_write(self.key, 'close', 'Client ended stream.\n')
            active_keys.discard(self.key)

    def write(self, action, msg):
        self.write_message(json.dumps(dict(action=action, key=self.key, msg=msg)))


class LandingHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello, world')


class StreamHandler(tornado.web.RequestHandler):
    def get(self, key):
        self.render('static/html/stream.html')


application = tornado.web.Application([
    (r'/', LandingHandler),
    (r'/ws', WSHandler),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'static'}),
    (r'/(.*)', StreamHandler),
])


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
