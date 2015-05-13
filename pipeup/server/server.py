
import json
import string
import random
import uuid

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

from config import SERVER_URL

listeners = dict()


def random_string(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class WSHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        self.key = None
        self.ip = self.request.remote_ip

        if 'User-Agent' not in self.request.headers:
            self.type = 'client'
            self.key = random_string()
            self.write('connected', SERVER_URL + self.key)

            listeners[self.key] = set()

            print 'opening client piping to ' + self.key
        else:
            self.type = 'listener'

            print 'opening listener'

    def on_message(self, message):
        if self.type == 'client':
            print 'message from client'

            if self.key in listeners:
                for listener in listeners[self.key]:
                    try:
                        listener.write('update', message)
                    except:
                        listener.close()
                        listeners[self.key].discard(listener)

        elif self.type == 'listener':
            try:
                msg = json.loads(message)
            except:
                return

            if msg['action'] == 'sub' and 'key' in msg and len(msg['key']) == 6:
                print 'adding listener to ' + msg['key']

                self.key = msg['key']

                if self.key in listeners:
                    listeners[self.key].add(self)
                else:
                    listeners[self.key] = set([self])

    def on_close(self):
        if self.type == 'client':
            print 'closing client'

            if self.key in listeners:
                for listener in listeners[self.key]:
                    try:
                        listener.write('close', 'Client ended stream.\n')
                    except:
                        listener.close()
                        listeners[self.key].discard(listener)

        elif self.type == 'listener':
            if self.key in listeners:
                listeners[self.key].discard(listener)

            print 'closing listener'

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
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
