from req import RequestHandler
from req import reqenv
from req import Service


class Web404Handler(RequestHandler):
    @reqenv
    def get(self):
        self.Render('404.html')
        return

    @reqenv
    def post(self):
        return
