from req import ApiRequestHandler
from req import Service
from map import *
import tornado

class SignSession(ApiRequestHandler):
    @tornado.gen.coroutine
    def post(self):
        args = ['account', 'passwd']
        data = self.get_args(args)
        err, res = yield from Service.user.User.signin_by_password(self, data)
        if err: self.render(err)
        else: self.render(res)

    @tornado.gen.coroutine
    def delete(self):
        pass


class SignUp(ApiRequestHandler):
    @tornado.gen.coroutine
    def post(self):
        pass

