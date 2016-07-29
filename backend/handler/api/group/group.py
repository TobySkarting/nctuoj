from req import ApiRequestHandler
from req import Service
import tornado

class Groups(ApiRequestHandler):
    @tornado.gen.coroutine
    def post(self):
        args = ['name', 'type', 'description']
        data = self.get_args(args)
        err, res = yield from Service.group.Group.post_group(data)
        if err:
            self.render(err)
        else:
            err, res = yield from Service.group.Group.get_group(res)
            self.render(res)

class Group(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self, id):
        err, res = yield from Service.group.Group.get_group({'id': id})
        if err:
            self.render(err)
        else:
            self.render(res)

    @tornado.gen.coroutine
    def put(self, id):
        args = ['name', 'type', 'description']
        data = self.get_args(args)
        data['id'] = id
        err, res = yield from Service.group.Group.put_group(data)
        if err:
            self.render(err)
        else:
            err, res = yield from Service.group.Group.get_group({'id': id})
            self.render(res)

    @tornado.gen.coroutine
    def delete(self, id):
        err, res = yield from Service.group.Group.delete_group({'id': id})
        self.render()

