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
    def get(self, id, action=None, sub_id=None, sub_action=None):
        meta = {}
        meta['id'] = id
        meta['group_id'] = self.current_group
        print("=============", id, action, sub_id, sub_action)
        if action == None:
            err, data = yield from Service.Problem.get_problem(meta)
            if err: self.error(err)
            else: self.success(data)
        elif action == "basic":
            self.success(action_id)
            pass
        elif action == "tag":
            pass
        elif action == "execute":
            err, data = yield from Service.Problem.get_problem_execute(meta)
            self.success(data)
        elif action == "testdata":
            if sub_id == None:
                err, data = yield from Service.Problem.get_problem_testdata(meta)
                if err: self.error(err)
                else: self.success(data)
        else:
            self.error("404")
        pass
        
    @reqenv
    def post(self, id, action=None, sub_id=None, sub_action=None):
        if 1 not in self.current_group_power:
            self.error("Permission Denied")
            return
        check_meta = {}
        check_meta['group_id'] = self.current_group
        check_meta['id'] = id
        err, data = yield from Service.Problem.get_problem(check_meta)
        if err: self.error(err)
        if int(data['group_id']) != int(check_meta['group_id']):
            self.error('Error mapping problem id and group id')

        ### /api/{{group_id}}/problems/{{problem_id}}/basic/
        if action == "basic":
            args = ["title", "description", "input", "output", "sample_input", "sample_output", "hint", "source", "visible"]
            meta = self.get_args(args)
            meta['group_id'] = self.current_group
            meta['setter_user_id'] = self.account['id']
            meta['id'] = id
            err, data = yield from Service.Problem.post_problem(meta)
            if err: self.error(err)
            else: self.success({"id": data})
        ### /api/{{group_id}}/problems/{{problem_id}}/execute/
        elif action == "execute":
            args = ['execute[]']
            meta = self.get_args(args)
            meta['group_id'] = self.current_group
            meta['id'] = id
            err, data = yield from Service.Problem.post_problem_execute(meta)
            if err: self.error(err)
            else: self.success("")
        elif action == "testdata":
            args = ['input', 'output', 'score', 'time_limit', 'memory_limit']
            meta['group_id'] = self.current_group
            meta['setter_user_id']  = self.account['id']
            pass

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
