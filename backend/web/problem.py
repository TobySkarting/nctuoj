from req import RequestHandler
from req import reqenv
from req import Service


class WebProblemsHandler(RequestHandler):
    @reqenv
    def get(self, group_id):
        self.current_group = group_id
        args = ["page"]
        meta = self.get_args(args)
        meta["page"] = meta["page"] if meta["page"] else 1
        meta["group_id"] = group_id
        err, data = yield from Service.Problem.get_problem_list(meta)
        self.render('./problems/problems.html', data=data)

    @reqenv
    def post(self):
        return

class WebProblemHandler(RequestHandler):
    @reqenv
    def get(self, id=None, action=None):
        print(id, action)
        if action == "edit":
            self.render('./problems/problem_edit.html')
        elif action == "submit":
            self.render('./problems/problem_submit.html')
        else:
            self.render('./problems/problem.html')
        pass

    """ update """
    @reqenv
    def post(self): 
        pass
