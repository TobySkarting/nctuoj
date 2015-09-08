from req import ApiRequestHandler
from req import Service
from map import *
import tornado

class ApiVerdictTypesHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        err, data = yield from Service.Verdict.get_verdict_list()
        if err: self.render(500, err)
        else: self.render(200, data)

    @tornado.gen.coroutine
    def post(self):
        pass

class ApiVerdictTypeHandler(ApiRequestHandler):
    def check_edit(self, meta):
        if map_power['verdict_manage'] not in self.account['power']:
            self.render(403, 'Permission Denied')
            return False
        err, data = yield from Service.Verdict.get_verdict(meta)
        if err:
            self.render(500, err)
            return False
        return True

    @tornado.gen.coroutine
    def get(self, id):
        meta = {}
        meta['id'] = id
        err, data = yield from Service.Verdict.get_verdict(meta)
        if err: self.render(500, err)
        else: self.render(200, data)

    @tornado.gen.coroutine
    def post(self, id):
        meta = {}
        meta['id'] = id
        if not (yield from self.check_edit(meta)):
            return
        args = ['title', 'code_file[file]', 'execute_type_id']
        meta = self.get_args(args)
        meta['id'] = id
        meta['setter_user_id'] = self.account['id']
        err, res = yield from Service.Verdict.post_verdict(meta)
        if err: self.render(500, err)
        else: self.render(200, res)

    @tornado.gen.coroutine
    def delete(self, id):
        meta = {}
        meta ['id'] = id
        if not (yield from self.check_edit(meta)):
            return
        err, data = yield from Service.Verdict.delete_verdict(meta)
        if err: self.render(500, err)
        else: self.render(200, data)
