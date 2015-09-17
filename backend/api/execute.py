from req import ApiRequestHandler
from req import Service
import tornado
from map import *


class ApiExecuteTypesHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        err, data = yield from Service.Execute.get_execute_list()
        if err: self.render(500, err)
        else: self.render(200, data)

    @tornado.gen.coroutine
    def post(self):
        args = ['priority[]', 'id[]']
        meta = self.get_args(args)
        print('META: ', meta)
        meta['priority'] = dict(zip([int(x) for x in meta['id']], [int(x) for x in meta['priority']]))
        err, res = yield from Service.Execute.post_execute_priority(meta)
        if err: self.render(500, err)
        else: self.render(200, res)

class ApiExecuteTypeHandler(ApiRequestHandler):
    def check_edit(self, meta):
        if map_power['execute_manage'] not in self.account['power']:
            self.render(403, 'Permission Denied')
            return False
        err, data = yield from Service.Execute.get_execute(meta)
        if err:
            self.render(500, err)
            return False
        return True

    @tornado.gen.coroutine
    def get(self, id):
        meta = {}
        meta['id'] = id
        err, data = yield from Service.Execute.get_execute(meta)
        if err: self.render(500, err)
        else: self.render(200, data)

    @tornado.gen.coroutine
    def post(self, id):
        check_meta = {}
        check_meta['id'] = id
        if not (yield from self.check_edit(check_meta)):
            return
        args = ["description", "lang", "command[]"]
        meta = self.get_args(args)
        meta["setter_user_id"] = self.account['id']
        meta['id'] = id
        err, data = yield from Service.Execute.post_execute(meta)
        if err: self.error(err)
        else: self.render(200, {"id": data})

    @tornado.gen.coroutine
    def delete(self, id):
        check_meta = {}
        check_meta['id'] = id
        if not (yield from self.check_edit(check_meta)):
            return
        meta = check_meta
        err, data = yield from Service.Execute.delete_execute(meta)
        if err: self.render(500, err)
        else: self.render(200, data)
