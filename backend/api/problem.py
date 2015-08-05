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
    def get(self, id):
        pass
        
    @reqenv
    def post(self, id):
        ### /api/{{group_id}}/problems/{{problem_id}}/
        args = ["title", "description", "input", "output", "sample_input", "sample_output", "hint", "source"]
        meta = self.get_args(args)
        meta['group_id'] = self.current_group
        meta['setter_user_id'] = self.account['id']
        meta['id'] = id
        if not 1 in self.current_group_power:
            self.error("Permission Denied")
            return
        err, data = yield from Service.Problem.post_problem(meta)
        if err: self.error(err)
        else: self.success({"id": data})

    @reqenv
    def delete(self, id):
        meta = {}
        meta["group_id"] = self.current_group
        meta["setter_user_id"] = self.account['id']
        meta['id'] = id
        if not 1 in self.current_group_power:
            self.error("Permission Denied")
            return
        err, data = yield from Service.Problem.delete_problem(meta)
        if err: self.error(err)
        else: self.success("")
