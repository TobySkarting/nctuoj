from req import ApiRequestHandler
from req import Service
from map import *
import tornado

class ApiContestsHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        args = ['count', 'page']
        meta = self.get_args(args)
        meta['group_id'] = self.current_group
        err, res = yield from Service.Contest.get_contest_list(meta)
        if err: self.render(err)
        self.render(res)

    @tornado.gen.coroutine
    def post(self):
        err = yield from Service.Permission.check(self)
        if err: self.render(err); return
        args = ['visible', 'title', 'description', 'register_start', 'register_end', 'start', 'freeze', 'end', 'type']
        meta = self.get_args(args)
        meta['group_id'] = self.current_group
        meta['setter_user_id'] = self.account['id']
        err, data = yield from Service.Contest.post_contest(meta)
        if err: self.render(err)
        else: self.render(data)
    
class ApiContestHandler(ApiRequestHandler):
    def check_edit(self, meta):
        if map_group_power['contest_manage'] not in self.current_group_power:
            self.render((403, 'Permission Denied'))
            return False
        err, data = yield from Service.Contest.get_contest(meta)
        if err:
            self.render(err)
            return False
        if int(data['group_id']) != int(meta['group_id']):
            self.render((403, 'Permission Denied'))
            return False
        return True

    @tornado.gen.coroutine
    def get(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err); return
        err, data = yield from Service.Contest.get_contest({'id': id})
        if err: self.render(err)
        else: self.render(data)
    
    @tornado.gen.coroutine
    def put(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err); return
        args = ['visible', 'title', 'description', 'register_start', 'register_end', 'start', 'freeze', 'end', 'type']
        meta = self.get_args(args)
        meta['id'] = id
        meta['group_id'] = self.current_group
        meta['setter_user_id'] = self.account['id']
        err, data = yield from Service.Contest.put_contest(meta)
        if err: self.render(err)
        else: self.render(data)

    @tornado.gen.coroutine
    def delete(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err); return
        err, res = yield from Service.Contest.delete_contest({'id': id})
        if err: self.render(err)
        else: self.render(res)

class ApiContestProblemsHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err); return
        err, res = yield from Service.Contest.get_contest_problem_list({'id': id})
        if err: self.render(err)
        else: self.render(res)

    @tornado.gen.coroutine
    def put(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err); return
        args = ['problems[]', 'scores[]']
        meta = self.get_args(args)
        meta['id'] = id
        err, res = yield from Service.Contest.put_contest_problem(meta)
        if err: self.render(err)
        else: self.render(res)
        return

class ApiContestSubmissionsHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err); return
        args = ['count', 'page']
        meta = self.get_args(args)
        meta['count'] = meta['count'] or 10
        meta['page'] = meta['page'] or 10
        meta['id'] = id
        meta['group_id'] = self.current_group
        meta['user_id'] = self.account['id']
        meta['current_group_power'] = self.current_group_power
        err, data = yield from Service.Contest.get_contest_submission_list(meta)
        if err: self.render(err)
        else: self.render(data)

class ApiContestScoreboardHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err); return
        meta = {}
        meta['id'] = id
        meta['current_group_power'] = self.current_group_power
        err, data = yield from Service.Contest.get_contest_submissions_scoreboard(meta)
        if err: self.render(err)
        else: self.render(data)
