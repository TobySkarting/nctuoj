from req import ApiRequestHandler
from req import Service
import tornado

class Bulletins(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self, group_id):
        data = {}
        data['group_id'] = group_id
        err, res = yield from Service.group.Bulletin.get_bulletin_list(data)
        if err:
            self.render(err)
        else:
            self.render(res)

