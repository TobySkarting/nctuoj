from req import ApiRequestHandler
from req import Service
import tornado


class ApiExecuteTypesHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        err, data = yield from Service.Execute.get_execute_list()
        self.render(200, data)

class ApiExecuteTypeHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self, id):
        pass

    @tornado.gen.coroutine
    def post(self, id):
        args = ["description", "lang", "command[]"]
        meta = self.get_args(args)
        meta["setter_user_id"] = self.account['id']
        meta['id'] = id
        if self.map_power['execute_manage'] not in self.account['power']:
            self.render(403, 'Permission Denied')
            return
        err, data = yield from Service.Execute.post_execute(meta)
        if err: self.error(err)
        else: self.render(200, {"id": data})

    @tornado.gen.coroutine
    def delete(self, id):
        pass
