from req import RequestHandler
from req import reqenv
from req import Service


class WebIndexHandler(RequestHandler):
    @reqenv
    def get(self):
        self.render('index.html')
        return

    @reqenv
    def post(self):
        return
