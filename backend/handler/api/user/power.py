from req import ApiRequestHandler
from req import Service
import tornado

class Power(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self, user_id):
        err, res = yield from Service.user.Power.get_power({'user_id': user_id})
        if err:
            self.render(err)
        else:
            self.render(res)

    @tornado.gen.coroutine
    def post(self, user_id):
        args = ['power']
        data = self.get_args(args)
        data['user_id'] = user_id
        err, res = yield from Service.user.Power.post_power(data)
        if err:
            self.render(err)
        else:
            err, res = yield from Service.user.Power.get_power(data)
            self.render(res)

    @tornado.gen.coroutine
    def delete(self, user_id):
        args = ['power']
        data = self.get_args(args)
        data['user_id'] = user_id
        err, res = yield from Service.user.Power.delete_power(data)
        if err:
            self.render(err)
        else:
            err, res = yield from Service.user.Power.get_power(data)
            self.render(res)
