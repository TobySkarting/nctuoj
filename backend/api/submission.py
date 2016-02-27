from req import ApiRequestHandler
from req import Service
from map import *
import tornado

class ApiSubmissionsHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        args = ['page', 'count']
        meta = self.get_args(args)
        meta['page'] = meta['page'] or 1
        meta['count'] = meta['count'] or 10
        meta['group_id'] = self.current_group
        err, data = yield from Service.Submission.get_submission_list(meta)
        if err: self.render(err)
        else: self.render(data)

    @tornado.gen.coroutine
    def post(self):
        args = ['problem_id', 'execute_type_id', 'code_file[file]', 'plain_code', 'plain_file_name']
        meta = self.get_args(args)
        meta['group_id'] = self.current_group
        meta['user_id'] =  self.account['id']
        meta['ip'] = self.remote_ip
        err = yield from Service.Permission.check(self, {'problem_id': meta['problem_id']})
        if err: self.render(err); return
        err, res = yield from Service.Submission.post_submission(meta)
        if err: self.render(err)
        else: self.render(res)

class ApiSubmissionHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err); return
        err, data = yield from Service.Submission.get_submission({'id': id})
        if self.account['id'] != data['user_id'] and \
                map_group_power['submission_manage'] not in self.current_group_power:
            data.pop('code')
        if err: self.render(err)
        else: self.render(data)

class ApiSubmissionRejudgeHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def post(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err); return
        err, res = yield from Service.Submission.post_rejudge({'id': id})
        if err: self.render(err)
        else: self.render(res)
