from req import WebRequestHandler
from req import Service
from map import map_group_power
import tornado
import math


class WebProblemsHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        args = ["page"]
        meta = self.get_args(args)
        meta['count'] = 100
        meta["group_id"] = self.current_group
        meta['user_id'] = self.account['id']
        ### default page is 1
        if not meta['page']:
            meta['page'] = 1
        ### if get page is not int then redirect to page 1 
        try:
            meta["page"] = int(meta["page"])
        except:
            self.write_error((500, 'Argument page error'))
            return
        ### should in range
        err, count = yield from Service.Problem.get_problem_list_count(meta)
        page_count = max(math.ceil(count / meta['count']), 1)
        if int(meta['page']) < 1 or int(meta['page']) > page_count:
            self.write_error((500, 'Page out of range'))
            return
        ### get data
        err, data = yield from Service.Problem.get_problem_list(meta)
        ### about pagination 
        page = {}
        page['total'] = page_count
        page['current'] = meta['page']
        page['url'] = '/groups/%s/problems/' % meta['group_id']
        page['get'] = {}
        self.render('./problems/problems.html', data=data, page=page)

class WebProblemHandler(WebRequestHandler):
    def check_view(self, meta={}):
        err, data = yield from Service.Problem.get_problem(meta)
        if err:
            self.write_error(err)
            return False
        if int(data['group_id']) == int(meta['group_id']) and (map_group_power['problem_manage'] in self.current_group_power or int(data['visible']) > 0):
            return True
        self.write_error(403)
        return False

    @tornado.gen.coroutine
    def get(self, id, action = None):
        meta = {}
        meta['id'] = id
        meta['group_id'] = self.current_group
        if not (yield from self.check_view(meta)):
            return
        err, data = yield from Service.Problem.get_problem(meta)
        if action == None:
            self.title = str(data['id']) + ". " + data['title']
            self.render('./problems/problem.html', data=data)
        elif action == "submit":
            self.title = "Submit " + str(data['id']) + ". " + data['title']
            self.render('./problems/problem_submit.html', data=data)
        else:
            self.write_error(404)

class WebProblemEditHandler(WebRequestHandler):
    def check_edit(self, meta={}):
        if int(meta['id']) == 0:
            return True
        err, data = yield from Service.Problem.get_problem(meta)
        if int(meta['group_id']) == int(data['group_id']) and map_group_power['problem_manage'] not in self.current_group_power:
            self.write_error(403)
            return False
        if err:
            self.write_error(500)
            return False
        return True

    @tornado.gen.coroutine
    def get(self, id, action = None):
        meta = {}
        meta['id'] = id
        if map_group_power['problem_manage'] not in self.current_group_power:
            self.write_error(403)
        meta['group_id'] = self.current_group
        if not (yield from self.check_edit(meta)):
            return
        err, data = yield from Service.Problem.get_problem(meta)
        err, data['verdict_list'] = yield from Service.Verdict.get_verdict_list({'problem_id': data['id']})
        err, data['execute_types'] = yield from Service.Execute.get_execute_list()

        if not action: action = "basic"
        if action == "basic":
            self.render('./problems/problem_edit.html', data=data)
        elif action == "tag":
            self.render('./problems/problem_edit_tag.html', data=data)
        elif action == "execute":
            self.render('./problems/problem_edit_execute.html', data=data)
        elif action == "testdata":
            self.render('./problems/problem_edit_testdata.html', data=data)
        else:
            self.write_error(404)
