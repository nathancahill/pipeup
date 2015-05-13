
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
        if 'User-Agent' not in self.request.headers:
            self.type = 'client'
            self.key = random_string()
            self.ip = self.request.remote_ip

            self.write_message(json.dumps(dict(action='connected', key=self.key, msg=SERVER_URL + self.key)))

            listeners[self.key] = []

            print 'opening client piping to ' + self.key
        else:
            self.type = 'listener'

            print 'opening listener'

    def on_message(self, message):
        if self.type == 'client':
            print 'message from client'

            if self.key in listeners:
                for i, listener in enumerate(reversed(listeners[self.key])):
                    try:
                        listener.write_message(json.dumps(dict(action='update', key=self.key, msg=message)))
                    except:
                        listener.close()

                        del listeners[self.key][i]

        elif self.type == 'listener':
            msg = json.loads(message)

            if msg['action'] == 'sub':
                print 'adding listener to ' + msg['key']

                self.key = msg['key']

                if self.key in listeners:
                    listeners[self.key].append(self)
                else:
                    listeners[self.key] = [self]

    def on_close(self):
        if self.type == 'client':
            print 'closing client'

            if self.key in listeners:
                for i, listener in enumerate(reversed(listeners[self.key])):
                    try:
                        listener.write_message(json.dumps(dict(action='close', key=self.key, msg='Client ended stream.\n')))
                    except:
                        listener.close()

                        del listeners[self.key][i]

        elif self.type == 'listener':
            # remove listener
            print 'closing listener'


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
