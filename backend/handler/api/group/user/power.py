from req import ApiRequestHandler
from req import Service
import tornado

class Power(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self, group_id, user_id):
        data = {}
        data['user_id'] = user_id
        data['group_id'] = group_id
        err, res = yield from Service.group.Power.get_power(data)
        if err:
            self.render(err)
        else:
            self.render(res)

    @tornado.gen.coroutine
    def post(self, group_id, user_id):
        args = ['power']
        data = self.get_args(args)
        data['user_id'] = user_id
        data['group_id'] = group_id
        err, res = yield from Service.group.Power.post_power(data)
        if err:
            self.render(err)
        else:
            err, res = yield from Service.group.Power.get_power(data)
            self.render(res)

    @tornado.gen.coroutine
    def delete(self, group_id, user_id):
        args = ['power']
        data = self.get_args(args)
        data['user_id'] = user_id
        data['group_id'] = group_id
        err, res = yield from Service.group.Power.delete_power(data)
        if err:
            self.render(err)
        else:
            err, res = yield from Service.group.Power.get_power(data)
            self.render(res)
