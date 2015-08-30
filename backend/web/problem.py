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
        ### default page is 1
        if not meta['page']:
            meta['page'] = 1
        ### if get page is not int then redirect to page 1 
        try:
            meta["page"] = int(meta["page"])
        except:
            self.write_error(404)
            return
        ### should in range
        err, count = yield from Service.Problem.get_problem_list_count(meta)
        page_count = max(math.ceil(count / meta['count']), 1)
        if int(meta['page']) < 1 or int(meta['page']) > page_count:
            self.write_error(404)
            return
        ### get data
        err, data = yield from Service.Problem.get_problem_list(meta)
        ### about pagination 
        page = {}
        page['total'] = page_count
        page['current'] = meta['page']
        page['url'] = '/group/%s/problems/' % meta['group_id']
        page['get'] = {}
        self.Render('./problems/problems.html', data=data, page=page)
class WebProblemHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self, id, action = None):
        meta = {}
        meta['id'] = id
        meta['group_id'] = self.current_group
        err, data = yield from Service.Problem.get_problem(meta)
        if err:
            self.write_error(404)
            return
        if int(meta['group_id'])==1 and int(data['visible']) == 2:
            pass
        elif int(data['group_id']) == int(meta['group_id']) and (map_group_power['admin_manage'] in self.current_group_power or int(data['visible']) != 0):
            pass
        else:
            self.write_error(403)
            return
        if action == None:
            self.Render('./problems/problem.html', data=data)
        elif action == "submit":
            self.Render('./problems/problem_submit.html', data=data)

class WebProblemEditHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self, id, action = None):
        meta = {}
        meta['id'] = id
        meta['group_id'] = self.current_group
        if map_group_power['admin_manage'] not in self.current_group_power:
            self.write_error(403)
            return
        err, data = yield from Service.Problem.get_problem(meta)
        if err:
            self.write_error(404)
            return
        elif int(id) != 0:
            if int(data['group_id']) != int(meta['group_id']):
                self.write_error(403)
                return

        if not action: action = "basic"
        if action == "basic":
            self.Render('./problems/problem_edit.html', data=data)
        elif action == "tag":
            self.Render('./problems/problem_edit_tag.html', data=data)
        elif action == "execute":
            self.Render('./problems/problem_edit_execute.html', data=data)
        elif action == "testdata":
            self.Render('./problems/problem_edit_testdata.html', data=data)
        else:
            self.write_error(404)
