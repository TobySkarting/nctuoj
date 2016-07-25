from req import ApiRequestHandler
from req import Service
import tornado

class Bulletins(ApiRequestHandler):
    @tornado.gen.coroutine
    def post(self):
        args = ['group_id', 'title', 'content']
        data = self.get_args(args)
        data['setter_user_id'] = self.account['id']
        err, res = yield from Service.Bulletin.post_bulletin(data)
        if err:
            self.render(err)
        else:
            err, res = yield from Service.Bulletin.get_bulletin(res)
            self.render(res)

class Bulletin(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self, id):
        err, res = yield from Service.Bulletin.get_bulletin({'id': id})
        if err:
            self.render(err)
        else:
            self.render(res)

    @tornado.gen.coroutine
    def put(self, id):
        args = ['title', 'content']
        data = self.get_args(args)
        data['setter_user_id'] = self.account['id']
        data['id'] = id
        err, res = yield from Service.Bulletin.put_bulletin(data)
        if err:
            self.render(err)
        else:
            err, res = yield from Service.Bulletin.get_bulletin({'id': id})
            self.render(res)


    @tornado.gen.coroutine
    def delete(self, id):
        err, res = yield from Service.Bulletin.delete_bulletin({'id': id})
        self.render()

