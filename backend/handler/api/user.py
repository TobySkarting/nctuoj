from req import ApiRequestHandler
from req import Service
import tornado

class Users(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        pass

    @tornado.gen.coroutine
    def post(self):
        args = ['email', 'account', 'password', 'repassword', 'name']
        data = self.get_args(args)
        err, res = yield from Service.User.post_user(data)
        if err:
            self.render(err)
        else:
            err, res = yield from Service.User.get_user(res)
            self.render(res)

class User(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self, id):
        err, res = yield from Service.User.get_user({'id': id})
        if err:
            self.render(err)
        else:
            self.render(res)

    @tornado.gen.coroutine
    def put(self, id):
        pass

    @tornado.gen.coroutine
    def delete(self, id):
        err, res = yield from Service.User.delete_user({'id': id})
        self.render()

class Power(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self, user_id):
        err, res = yield from Service.User.get_power({'user_id': user_id})
        if err:
            self.render(err)
        else:
            self.render(res)

    @tornado.gen.coroutine
    def post(self, user_id):
        args = ['power']
        data = self.get_args(args)
        data['user_id'] = user_id
        err, res = yield from Service.User.post_power(data)
        if err:
            self.render(err)
        else:
            err, res = yield from Service.User.get_power(data)
            self.render(res)

    @tornado.gen.coroutine
    def delete(self, user_id):
        args = ['power']
        data = self.get_args(args)
        data['user_id'] = user_id
        err, res = yield from Service.User.delete_power(data)
        if err:
            self.render(err)
        else:
            err, res = yield from Service.User.get_power(data)
            self.render(res)
