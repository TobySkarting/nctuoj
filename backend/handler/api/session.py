from req import ApiRequestHandler
from req import Service
import tornado

class Session(ApiRequestHandler):
    @tornado.gen.coroutine
    def post(self):
        args = ['email', 'password']
        data = self.get_args(args)
        err, res = yield from Service.Session.post_session_by_password(self, data)
        if err:
            self.render(err)
        else:
            self.render(res)

    @tornado.gen.coroutine
    def delete(self):
        err, res = Service.Session.delete_session(self)
        self.render()

