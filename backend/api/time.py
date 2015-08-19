from req import RequestHandler
from req import Service


class ApiTimeHandler(RequestHandler):
    def get(self):
        self.error(404)
