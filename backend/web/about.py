from req import WebRequestHandler
from req import Service
import tornado

class WebAboutHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        self.Render('about/about.html')
        return
