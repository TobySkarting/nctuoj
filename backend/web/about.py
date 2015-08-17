from req import RequestHandler
from req import reqenv
from req import Service


class WebAboutHandler(RequestHandler):
    @reqenv
    def get(self):
        self.Render('about/about.html')
        return

    @reqenv
    def post(self):
        return
