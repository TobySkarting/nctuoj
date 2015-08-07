from req import RequestHandler
from req import reqenv
from req import Service
import math


class WebVerdictTypesHandler(RequestHandler):
    @reqenv
    def get(self):
        pass

class WebVerdictTypeHandler(RequestHandler):
    @reqenv
    def get(self, id, action):
        pass
