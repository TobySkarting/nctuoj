from req import ApiRequestHandler
from req import Service
import tornado

class Executes(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        err, res = yield from Service.Execute.get_execute_list()
        if err:
            self.render(err)
        else:
            self.render(res)

    @tornado.gen.coroutine
    def post(self):
        args = ['description', 'language_id', 'commands[]', 'file_name']
        data = self.get_args(args)
        data['setter_user_id'] = self.account['id']
        err, res = yield from Service.Execute.post_execute(data)
        if err:
            self.render(err)
        else:
            err, res = yield from Service.Execute.get_execute_with_steps(res)
            self.render(res)

class Execute(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self, id):
        data = {}
        data['id'] = id
        err, res = yield from Service.Execute.get_execute_with_steps(data)
        if err:
            self.render(err)
        else:
            self.render(res)

    @tornado.gen.coroutine
    def put(self, id):
        args = ['description', 'language_id', 'commands[]', 'file_name']
        data = self.get_args(args)
        data['setter_user_id'] = self.account['id']
        data['id'] = id
        err, res = yield from Service.Execute.put_execute(data)
        if err:
            self.render(err)
        else:
            err, res = yield from Service.Execute.get_execute_with_steps({'id': id})
            self.render(res)

    @tornado.gen.coroutine
    def delete(self, id):
        data = {}
        data['id'] = id
        err, res = yield from Service.Execute.delete_execute(data)
        self.render()
