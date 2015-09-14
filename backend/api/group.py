from req import ApiRequestHandler
from req import Service
import tornado

class ApiGroupHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self, id):
        pass

    @tornado.gen.coroutine
    def post(self, id):
        pass
    
