from req import WebRequestHandler
from req import Service
import tornado
import math


class WebContestsHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        self.Render('./contests/contests.html')

class WebContestHandler(WebRequestHandler):
    def get(self, id=None, action=None):
        pass

