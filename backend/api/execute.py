from req import ApiRequestHandler
from req import Service
import tornado
from map import *


class ApiExecuteTypesHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        err, data = yield from Service.Execute.get_execute_list()
        if err: self.render(err)
        else: self.render(data)

    @tornado.gen.coroutine
    def post(self):
        err = yield from Service.Permission.check(self)
        if err: self.render(err); return
        args = ["description", "lang", "command[]", "cm_mode"]
        meta = self.get_args(args)
        meta["setter_user_id"] = self.account['id']
        err, data = yield from Service.Execute.post_execute(meta)
        if err: self.render(err)
        else: self.render({"id": data})

class ApiExecuteTypesPriorityHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def post(self):
        err = yield from Service.Permission.check(self)
        if err: self.render(err); return
        args = ['priority[]', 'id[]']
        meta = self.get_args(args)
        meta['priority'] = dict(zip([int(x) for x in meta['id']], [int(x) for x in meta['priority']]))
        err, res = yield from Service.Execute.post_execute_priority(meta)
        if err: self.render(err)
        else: self.render(res)

class ApiExecuteTypeHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self, id):
        err, data = yield from Service.Execute.get_execute({'id': id})
        if err: self.render(err)
        else: self.render(data)

    @tornado.gen.coroutine
    def put(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err); return
        args = ["description", "lang", "command[]", "cm_mode"]
        meta = self.get_args(args)
        meta["setter_user_id"] = self.account['id']
        meta['id'] = id
        err, data = yield from Service.Execute.put_execute(meta)
        if err: self.error(err)
        else: self.render({"id": data})

    @tornado.gen.coroutine
    def delete(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err); return
        err, data = yield from Service.Execute.delete_execute({'id': id})
        if err: self.render(err)
        else: self.render(data)

