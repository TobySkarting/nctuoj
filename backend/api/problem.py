from req import RequestHandler
from req import reqenv
from req import Service

class ApiProblemListHandler(RequestHandler):
    @reqenv
    def get(self, page):
        self.success({"page": page})
        return
