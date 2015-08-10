from req import RequestHandler
from req import reqenv
from req import Service


class ApiProblemsHandler(RequestHandler):
    @reqenv
    def get(self):
        pass

    @reqenv
    def post(self):
        pass

    @reqenv
    def delete(self):
        pass

class ApiProblemHandler(RequestHandler):
    @reqenv
    def get(self, id, action):
        meta = {}
        meta['id'] = id
        if action == "basic":
            pass
        elif action == "tag":
            pass
        ### /api/0/problems/{{problem_id}}/execute/
        elif action == "execute":
            err, data = yield from Service.Problem.get_problem_execute(meta)
            self.success(data)
        elif action == "testdata":
            pass
        else:
            self.error("404")
        pass
        
    @reqenv
    def post(self, id, action):
        ### /api/{{group_id}}/problems/{{problem_id}}/basic/
        if 1 not in self.current_group_power:
            self.error("Permission Denied")
            return
        if action == "basic":
            args = ["title", "description", "input", "output", "sample_input", "sample_output", "hint", "source", "visible"]
            meta = self.get_args(args)
            meta['group_id'] = self.current_group
            meta['setter_user_id'] = self.account['id']
            meta['id'] = id
            err, data = yield from Service.Problem.post_problem(meta)
            if err: self.error(err)
            else: self.success({"id": data})

    @reqenv
    def delete(self, id, action):
        if action == "basic":
            meta = {}
            meta["group_id"] = self.current_group
            meta["setter_user_id"] = self.account['id']
            meta['id'] = id
            if 1 not in self.current_group_power:
                self.error("Permission Denied")
                return
            err, data = yield from Service.Problem.delete_problem(meta)
            if err: self.error(err)
            else: self.success("")
