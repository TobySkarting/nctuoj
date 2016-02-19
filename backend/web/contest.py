from req import WebRequestHandler
from req import Service
import tornado
import math
import datetime
from map import *


class WebContestsHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        args = ["page"]
        meta = self.get_args(args)
        meta['count'] = 10
        meta["group_id"] = self.current_group
        ### default page is 1
        if not meta['page']:
            meta['page'] = 1
        ### if get page is not int then redirect to page 1 
        try:
            meta["page"] = int(meta["page"])
        except:
            self.write_error(500, 'Argument page error')
            return
        ### should in range
        err, count = yield from Service.Contest.get_contest_list_count(meta)
        page_count = max(math.ceil(count / meta['count']), 1)
        if int(meta['page']) < 1 or int(meta['page']) > page_count:
            self.write_error(404, 'Page out of range')
            return
        ### get data
        err, data = yield from Service.Contest.get_contest_list(meta)
        ### about pagination 
        page = {}
        page['total'] = page_count
        page['current'] = meta['page']
        page['url'] = '/groups/%s/contests/' % meta['group_id']
        page['get'] = {}
        self.render('./contests/contests.html', data=data, page=page)

class WebContestHandler(WebRequestHandler):
    def check_view(self, meta):
        err, data = yield from Service.Contest.get_contest(meta)
        if err:
            self.write_error(500)
            return False
        if map_group_power['contest_manage'] in self.current_group_power or int(data['visible']) > 0:
            return True
        self.write_error(403)
        return False

    @tornado.gen.coroutine        
    def get(self, id=None, action=None):
        meta = {}
        meta['id'] = id
        meta['group_id'] = self.current_group
        if not (yield from self.check_view(meta)):
            return
        err, data = yield from Service.Contest.get_contest(meta)
        self.render('./contests/contest.html', contest_data=data)

class WebContestEditHandler(WebRequestHandler):
    def check_edit(self, meta):
        err, data = yield from Service.Contest.get_contest(meta)
        if err:
            self.write_error(500)
            return False
        if map_group_power['contest_manage'] in self.current_group_power:
            return True
        self.write_error(403)
        return False

    @tornado.gen.coroutine
    def get(self, id, action=None):
        meta = {}
        meta['id'] = id
        meta['group_id'] = self.current_group
        if not (yield from self.check_edit(meta)):
            return
        err, contest_data = yield from Service.Contest.get_contest(meta)
        self.render('./contests/contest_edit.html', contest_data=contest_data)

class WebContestProblemHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self, contest_id, problem_id, action=None):
        meta = {
            'id': problem_id
        }
        err, data = yield from Service.Problem.get_problem(meta)
        err, contest_data = yield from Service.Contest.get_contest({"id": contest_id, "group_id": self.current_group})
        if action == None:
            self.render('./contests/contest_problem.html', data=data, contest_data=contest_data)
        elif action == "submit":
            self.render('./contests/contest_problem_submit.html', data=data, contest_data=contest_data)
        else:
            self.write_error(404)

class WebContestSubmissionsHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self, contest_id):
        err, contest_data = yield from Service.Contest.get_contest({"id": contest_id, "group_id": self.current_group})
        if err:
            self.write_error(500, err)
            return
        args = ['account', 'problem_id', 'page']
        meta = self.get_args(args)
        meta["count"] = 10
        meta['id'] = contest_id
        meta['group_id'] = self.current_group
        meta['user_id'] = self.account['id']
        meta['current_group_power'] = self.current_group_power
        ### default page is 1
        if not meta['page']:
            meta['page'] = 1
        ### if get page is not int then throw the error
        try:
            meta["page"] = int(meta["page"])
        except:
            self.write_error(500, 'Argument page error')
            return
        err, data = yield from Service.Contest.get_contest_submission_list(meta)
        if err: 
            self.write_wrror(500, err)
            return
        ### should in range
        err, count = yield from Service.Contest.get_contest_submission_list_count(meta)
        if err:
            self.write_error(500, err)
            return
        page_count = max(math.ceil(count / meta['count']), 1)
        if int(meta['page']) < 1 or int(meta['page']) > page_count:
            self.write_error(500, 'Page out of range')
            return
        
        ### about pagination 
        page = {}
        page['total'] = page_count
        page['current'] = meta['page']
        page['url'] = '/groups/%s/contests/%s/submissions/' % (meta['group_id'], contest_id)
        page['get'] = self.get_args(args)
        self.render('./contests/contest_submissions.html', contest_data=contest_data, data=data, page=page)

class WebContestSubmissionHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self, contest_id, id):
        err, contest_data = yield from Service.Contest.get_contest({"id": contest_id, "group_id": self.current_group})
        err, data = yield from Service.Contest.get_contest_submission({"id": contest_id, 'user_id': self.account['id'], 'current_group_power': self.current_group_power, "submission_id": id})
        if err:
            self.write_error(500, err)
            return
        self.render('./contests/contest_submission.html', contest_data=contest_data, data=data)

class WebContestScoreboardHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self, contest_id):
        meta = {
            "id": contest_id,
            "current_group_power": self.current_group_power
        }
        err, data = yield from Service.Contest.get_contest_submissions_scoreboard(meta)
        err, contest_data = yield from Service.Contest.get_contest({"id": contest_id, "group_id": self.current_group})
        self.render('./contests/contest_scoreboard.html', data=data, contest_data=contest_data)
