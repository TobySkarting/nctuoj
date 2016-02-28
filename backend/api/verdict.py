from req import ApiRequestHandler
from req import Service
from map import *
import tornado

class ApiVerdictTypesHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        args = ['problem_id']
        meta = self.get_args(args)
        err, data = yield from Service.Verdict.get_verdict_list(meta)
        if err: self.render(err)
        else: self.render(data)

    @tornado.gen.coroutine
    def post(self):
        err = yield from Service.Permission.check(self)
        if err: self.render(err); return
        args = ['title', 'code_file[file]', 'execute_type_id']
        meta = self.get_args(args)
        meta['setter_user_id'] = self.account['id']
        err, res = yield from Service.Verdict.post_verdict(meta)
        if err: self.render(err)
        else: self.render(res)

class ApiVerdictTypeHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err); return
        err, data = yield from Service.Verdict.get_verdict({'id': id})
        if err: self.render(err)
        else: self.render(data)

    @tornado.gen.coroutine
    def put(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err); return
        args = ['title', 'code_file[file]', 'execute_type_id']
        meta = self.get_args(args)
        meta['id'] = id
        meta['setter_user_id'] = self.account['id']
        err, res = yield from Service.Verdict.put_verdict(meta)
        if err: self.render(err)
        else: self.render(res)

    @tornado.gen.coroutine
    def delete(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err); return
        err, data = yield from Service.Verdict.delete_verdict({'id': id})
        if err: self.render(err)
        else: self.render(data)
