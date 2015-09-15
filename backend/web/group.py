from req import WebRequestHandler
from req import Service
import tornado

class WebGroupHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self, id):
        self.Render('group/group.html')

    @tornado.gen.coroutine
    def post(self, id):
        pass
