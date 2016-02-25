from req import ApiRequestHandler
from req import Service
from map import *
import tornado

class ApiVerdictTypesHandler(ApiRequestHandler):

    def check_edit(self, meta={}):
        if map_power['verdict_manage'] not in self.account['power']:
            self.render(403, 'Permission Denied')
            return False
        return True

    @tornado.gen.coroutine
    def get(self):
        args = ['problem_id']
        meta = self.get_args(args)
        err, data = yield from Service.Verdict.get_verdict_list(meta)
        if err: self.render(500, err)
        else: self.render(200, data)

    @tornado.gen.coroutine
    def post(self):
        if not (self.check_edit()):
            return
        args = ['title', 'code_file[file]', 'execute_type_id']
        meta = self.get_args(args)
        meta['setter_user_id'] = self.account['id']
        err, res = yield from Service.Verdict.post_verdict(meta)
        if err: self.render(500, err)
        else: self.render(200, res)

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
    
    def check_view(self, meta):
        err, data = yield from Service.Verdict.get_verdict(meta)
        if err:
            self.render(500, err)
            return False
        if int(data['problem_id']) != 0:
            err, data = yield from Service.Problem.get_problem({'id': data['problem_id']})
            if err: 
                self.render(500, err)
                return False
            if map_power['verdict_manage'] in self.power:
                return True
            if int(data['group_id']) not in (int(x['id']) for x in self.group):
                self.render(403, 'Permission Denied')
                return False
            if map_group_power['problem_manage'] not in (yield from Service.User.get_user_group_power_info(self.account['id'], data['group_id']))[1]:
                self.render(403, 'Permission Denied')
                return False
        return True

    @tornado.gen.coroutine
    def get(self, id):
        meta = {}
        meta['id'] = id
        if not (yield from self.check_view(meta)):
            return False
        err, data = yield from Service.Verdict.get_verdict(meta)
        if err: self.render(500, err)
        else: self.render(200, data)

    @tornado.gen.coroutine
    def put(self, id):
        meta = {}
        meta['id'] = id
        if not (yield from self.check_edit(meta)):
            return
        args = ['title', 'code_file[file]', 'execute_type_id']
        meta = self.get_args(args)
        meta['id'] = id
        meta['setter_user_id'] = self.account['id']
        err, res = yield from Service.Verdict.put_verdict(meta)
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
