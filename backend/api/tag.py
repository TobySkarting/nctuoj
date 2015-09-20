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
        meta = {}
        meta['id'] = id
        err, data = yield from Service.Tags.get_tag(meta)
        if err: self.render(500, err)
        else: self.render(200, data)

    @tornado.gen.coroutine
    def post(self, id):
        args = ['tag', 'description']
        meta = self.get_args(args)
        meta['id'] = id
        err, res = yield from Service.Tags.post_tag(meta)
        if err: self.render(500, err)
        else: self.render(200, res)

    @tornado.gen.coroutine
    def delete(self, id):
        meta = {}
        meta['id'] = id
        err, res = yield from Service.Tags.delete_tag(meta)
        if err: self.render(500, data)
        else: self.render(200, res)

