
import json
import string
import random
import uuid

import pydash

import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import tornado.template

streams = dict()


def random_string(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


class WSHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        self.id = uuid.uuid4()

        if 'User-Agent' not in self.request.headers:
            self.key = random_string()
            self.write_message('http://pipeup.io/' + self.key)

            streams[self.id] = dict(
                key=self.key,
                source=self,
                ip=self.request.remote_ip,
                listeners=[],
            )

    def on_message(self, message):
        print streams

        if self.id in streams:
            for listener in streams[self.id]['listeners']:
                try:
                    listener.write_message(json.dumps(dict(key=streams[self.id]['key'], msg=message)))
                except:
                    pass
        else:
            msg = json.loads(message)
            print msg

            if msg['action'] == 'sub':
                _streams = pydash.select(streams, dict(key=msg['key']))

                for stream in _streams:
                    stream['listeners'].append(self)

    def on_close(self):
        if self.id in streams:
            for listener in streams[self.id]['listeners']:
                listener.write_message('Client ended stream')

        print 'connection closed'


class LandingHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Hello, world')


class StreamHandler(tornado.web.RequestHandler):
    def get(self, key):
        self.write(loader.load('stream.html').generate(key=key))


loader = tornado.template.Loader('templates')

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
