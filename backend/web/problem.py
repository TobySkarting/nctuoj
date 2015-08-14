from req import RequestHandler
from req import reqenv
from req import Service
import math


class WebProblemsHandler(RequestHandler):
    @reqenv
    def get(self):
        args = ["page"]
        meta = self.get_args(args)
        meta['count'] = 100
        meta["group_id"] = self.current_group
        meta["is_admin"] = 1 if 1 in self.current_group_power else 0
        ### default page is 1
        if not meta['page']:
            meta['page'] = 1
        ### if get page is not int then redirect to page 1 
        try:
            meta["page"] = int(meta["page"])
        except:
            self.redirect('/group/'+meta['group_id']+'/problems/')
            return
        ### modify page in range (1, page_count)
        err, count = yield from Service.Problem.get_problem_list_count(meta)
        page_count = max(math.ceil(count / meta['count']), 1)
        if int(meta['page']) < 1:
            self.redirect('/group/'+meta['group_id']+'/problems/')
            return
        if int(meta['page']) > page_count:
            self.redirect('/group/'+meta['group_id']+'/problems/?page='+str(page_count))
            return
        ### get data
        err, data = yield from Service.Problem.get_problem_list(meta)
        ### about pagination 
        page = {}
        page['total'] = page_count
        page['current'] = meta['page']
        page['url'] = '/group/' + meta['group_id'] + '/problems/'
        page['get'] = {}
        self.Render('./problems/problems.html', data=data, page=page)

class WebProblemHandler(RequestHandler):
    @reqenv
    def get(self, id):
        meta = {}
        meta['id'] = id
        meta['group_id'] = self.current_group
        err, data = yield from Service.Problem.get_problem(meta)
        if err:
            self.write_error(404)
        else:
            if int(data['visible']) == 2:
                self.Render('./problems/problem.html', data=data)
            elif int(data['group_id']) == int(meta['group_id']) and int(data['visible']==1):
                self.Render('./problems/problem.html', data=data)
            else:
                self.write_error(403)

        


class WebProblemEditHandler(RequestHandler):
    @reqenv
    def get(self, id, action = None):
        meta = {}
        meta['id'] = id
        meta['group_id'] = self.current_group
        if not 1 in self.current_group_power:
            self.write_error(403)
            return
        err, data = yield from Service.Problem.get_problem(meta)
        if err:
            self.write_error(404)
            return
        else:
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
