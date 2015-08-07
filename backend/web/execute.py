from req import RequestHandler
from req import reqenv
from req import Service
import math


class WebExecuteTypesHandler(RequestHandler):
    @reqenv
    def get(self):
        err, data = yield from Service.Execute.get_execute_list()
        self.Render('./executes/executes.html', data=data)
        pass

class WebExecuteTypeHandler(RequestHandler):
    @reqenv
    def get(self, id, action):
        pass
