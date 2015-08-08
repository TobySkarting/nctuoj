from req import RequestHandler
from req import reqenv
from req import Service


class Web404Handler(RequestHandler):
    @reqenv
    def get(self):
        self.write_error(404)
        return

    @reqenv
    def post(self):
        return
