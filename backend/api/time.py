from req import ApiRequestHandler
from req import Service
import tornado
import datetime


class ApiTimeHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        self.render(msg={'datetime': datetime.datetime.now()})
