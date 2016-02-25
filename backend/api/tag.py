from req import ApiRequestHandler
from req import Service
import tornado

class ApiTagsHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        err, data = yield from Service.Tags.get_tag_list()
        if err: self.render(err)
        else: self.render(data)

    @tornado.gen.coroutine
    def post(self):
        args = ['tag', 'description']
        meta = self.get_args(args)
        err, res = yield from Service.Tags.put_tag(meta)
        if err: self.render(err)
        else: self.render(res)


class ApiTagHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self, id):
        meta = {}
        meta['id'] = id
        err, data = yield from Service.Tags.get_tag(meta)
        if err: self.render(err)
        else: self.render(data)

    @tornado.gen.coroutine
    def post(self, id):
        args = ['tag', 'description']
        meta = self.get_args(args)
        meta['id'] = id
        err, res = yield from Service.Tags.post_tag(meta)
        if err: self.render(err)
        else: self.render(res)

    @tornado.gen.coroutine
    def delete(self, id):
        meta = {}
        meta['id'] = id
        err, res = yield from Service.Tags.delete_tag(meta)
        if err: self.render(data)
        else: self.render(res)

