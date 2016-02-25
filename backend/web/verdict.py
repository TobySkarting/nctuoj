from req import WebRequestHandler
from req import Service
from map import *
import tornado
import math


class WebVerdictTypesHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        err, data = yield from Service.Verdict.get_verdict_list()
        if err: self.write_error(err)
        else: self.render('./verdicts/verdicts.html', data=data)

class WebVerdictTypeHandler(WebRequestHandler):
    def check_view(self, meta):
        err, data = yield from Service.Verdict.get_verdict(meta)
        if err:
            self.write_error(err)
            return False
        if int(data['problem_id']) != 0:
            err, data = yield from Service.Problem.get_problem({'id': data['problem_id']})
            if err: 
                self.write_error(500, err)
                return False
            if map_power['verdict_manage'] in self.account['power']:
                return True
            if int(data['group_id']) not in (int(x['id']) for x in self.group):
                self.write_error(403)
                return False
            if map_group_power['problem_manage'] not in (yield from Service.User.get_user_group_power_info(self.account['id'], data['group_id']))[1]:
                self.write_error(403)
                return False
        return True
    @tornado.gen.coroutine
    def get(self, id, action=None):
        meta = {}
        meta["id"] = id
        if not action : action = "view"
        if action == "view":
            if not (yield from self.check_view(meta)):
                return
            err, data = yield from Service.Verdict.get_verdict(meta)
            if err: self.write_error(err)
            else: self.render('./verdicts/verdict.html', data=data)
        elif action == "edit":
            ### check power
            if map_power['verdict_manage'] not in self.account['power']:
                self.write_error(403)
                return
            err, data = yield from Service.Verdict.get_verdict(meta)
            if err:
                self.write_error(err)
                return
            err, data['execute_types'] = yield from Service.Execute.get_execute_list()
            if err: self.write_error(err)
            else: self.render('./verdicts/verdict_edit.html', data=data)
        else:
            self.write_error(404)
