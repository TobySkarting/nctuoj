from req import ApiRequestHandler
from req import Service
import tornado

class ApiTagsHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        err, data = yield from Service.Tags.get_tag_list()
        if err: self.render(500, err)
        else: self.render(200, data)

    @tornado.gen.coroutine
    def post(self):
        pass


class ApiTagHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self, id):
        pass

    @tornado.gen.coroutine
    def post(self, id):
        pass

    @tornado.gen.coroutine
    def delete(self, id):
        pass
