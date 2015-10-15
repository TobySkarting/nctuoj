from req import WebRequestHandler
from req import Service
import tornado
import math
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
        page['url'] = '/group/%s/contests/' % meta['group_id']
        page['get'] = {}
        self.Render('./contests/contests.html', data=data, page=page)

class WebContestHandler(WebRequestHandler):
    def check_view(self, meta):
        err, data = yield from Service.Contest.get_contest(meta)
        if err:
            self.write_error(500)
            return False
        if map_group_power['contest_manage'] in self.current_group_power or int(data['visible']) != 0:
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
        self.Render('./contests/contest.html', contest_data=data)

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
        err, data = yield from Service.Contest.get_contest(meta)
        self.Render('./contests/contest_edit.html', data=data)

class WebContestProblemHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self, contest_id, problem_id, action=None):
        meta = {
            'id': problem_id
        }
        err, data = yield from Service.Problem.get_problem(meta)
        err, contest_data = yield from Service.Contest.get_contest({"id": contest_id, "group_id": self.current_group})
        if action == None:
            self.Render('./contests/contest_problem.html', data=data, contest_data=contest_data)
        elif action == "submit":
            self.Render('./contests/contest_problem_submit.html', data=data, contest_data=contest_data)
        else:
            self.write_error(404)

class WebContestSubmissionsHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self, contest_id):
        err, contest_data = yield from Service.Contest.get_contest({"id": contest_id, "group_id": self.current_group})
        err, data = yield from Service.Contest.get_contest_submission_list({"id": contest_id, "user_id": self.account['account']})
        self.Render('./contests/contest_submissions.html', contest_data=contest_data, data=data)

class WebContestSubmissionHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self, contest_id, id):
        err, contest_data = yield from Service.Contest.get_contest({"id": contest_id, "group_id": self.current_group})
        err, data = yield from Service.Contest.get_contest_submission({"id": contest_id, "submission_id": id})
        self.Render('./contests/contest_submission.html', contest_data=contest_data, data=data)

class WebContestScoreboardHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self, contest_id):
        err, contest_data = yield from Service.Contest.get_contest({"id": contest_id, "group_id": self.current_group})
        self.Render('./contests/contest_scoreboard.html', contest_data=contest_data)
