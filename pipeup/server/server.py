
import json
import string
import random

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web

from config import SERVER_URL

listeners = dict()
unbounded = dict()


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

            print 'opening client ' + self.ip
        else:
            self.type = 'listener'

            print 'opening listener ' + self.ip

    def on_message(self, message):
        try:
            msg = json.loads(message)
        except:
            return

        if self.type == 'client':
            if msg['action'] == 'request':
                if msg['key'] and len(msg['key']) == 6 and \
                                  msg['key'].isalnum() and \
                                  msg['key'] not in listeners:
                    self.key = msg['key']
                else:
                    self.key = random_string()

                listeners[self.key] = set()

                if self.key in unbounded:
                    listeners[self.key] = listeners[self.key] | unbounded.pop(self.key)

                self.write('connected', SERVER_URL + self.key)

            elif msg['action'] == 'send':
                if self.key in listeners:
                    for listener in listeners[self.key]:
                        try:
                            listener.write('update', msg['msg'])
                        except:
                            listener.close()
                            listeners[self.key].discard(listener)

        elif self.type == 'listener':
            if msg['action'] == 'sub' and 'key' in msg and len(msg['key']) == 6:
                print 'adding listener to ' + msg['key']

                self.key = msg['key']

                if self.key in listeners:
                    listeners[self.key].add(self)
                else:
                    if self.key in unbounded:
                        unbounded[self.key].add(self)
                    else:
                        unbounded[self.key] = set([self])

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

                listeners.pop(self.key)

        elif self.type == 'listener':
            if self.key in listeners:
                listeners[self.key].discard(self)

            print 'closing listener'

    def write(self, action, msg):
        self.write_message(json.dumps(dict(action=action, key=self.key, msg=msg)))


class StreamHandler(tornado.web.RequestHandler):
    def get(self, key):
        self.render('static/html/stream.html')


application = tornado.web.Application([
    (r'/ws', WSHandler),
    (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': 'static'}),
    (r'/(.*)', StreamHandler),
])


if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
