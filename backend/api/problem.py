from req import ApiRequestHandler
from req import Service
from map import map_group_power
import tornado


class ApiProblemsHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        err = yield from Service.Permission.check(self)
        if err: self.render(err); return
        args = ['page', 'count']
        meta = self.get_args(args)
        meta['page'] = meta['page'] or 1
        meta['count'] = meta['count'] or 10
        meta['group_id'] = self.current_group
        meta['user_id'] = self.account['id']
        err, data = yield from Service.Problem.get_problem_list(meta)
        if err: self.render(err)
        else: self.render(data)

    @tornado.gen.coroutine
    def post(self):
        err = yield from Service.Permission.check(self)
        if err: self.render(err); return
        args = ["title", "description", "input", "output", "sample_input", "sample_output", "hint", "source", "visible", 'verdict_id', 'verdict_code[file]', 'verdict_execute_type_id', 'pdf', 'pdf_file[file]', 'score_type_id']
        meta = self.get_args(args)
        meta['group_id'] = self.current_group
        meta['setter_user_id'] = self.account['id']
        err, data = yield from Service.Problem.post_problem(meta)
        if err: self.render(err)
        else: self.render({"id": data})

class ApiProblemHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err); return
        err, data = yield from Service.Problem.get_problem({'id': id})
        if err: return err
        else: self.render(data)
        
    @tornado.gen.coroutine
    def put(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err); return
        args = ["title", "description", "input", "output", "sample_input", "sample_output", "hint", "source", "visible", 'verdict_id', 'verdict_code[file]', 'verdict_execute_type_id', 'pdf', 'pdf_file[file]', 'score_type_id']
        meta = self.get_args(args)
        meta['group_id'] = self.current_group
        meta['setter_user_id'] = self.account['id']
        meta['id'] = id
        err, data = yield from Service.Problem.put_problem(meta)
        if err: self.render(err)
        else: self.render({"id": data})
    
    @tornado.gen.coroutine
    def delete(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err); return
        err, data = yield from Service.Problem.delete_problem({'id': id})
        if err: self.render(err)
        else: self.render()

class ApiProblemExecuteHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err); return
        err, data = yield from Service.Problem.get_problem_execute({"problem_id": id})
        if err: self.render(err)
        else: self.render(data)

    @tornado.gen.coroutine
    def put(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err); return
        args = ['execute[]']
        meta = self.get_args(args)
        meta['problem_id'] = id
        print(meta)
        err, data = yield from Service.Problem.put_problem_execute(meta)
        if err: self.render(err)
        else: self.render()

class ApiProblemRejudgeHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def post(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: return err
        err, res = yield from Service.Problem.post_rejudge_problem({'id': id})
        if err: self.render(err)
        else: self.render()

class ApiProblemTagHandler(ApiProblemHandler):
    @tornado.gen.coroutine
    def get(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err)
        err, data = yield from Service.Problems.get_problem_tag({'problem_id': id})
        if err: self.redner(err)
        else: self.render(data)

    @tornado.gen.coroutine
    def post(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err)
        args = ['tag_id']
        meta = self.get_args(args)
        meta['problem_id'] = id
        err, res = yield from Service.Problems.post_problem_tag(meta)
        if err: self.render(err)
        else: self.render()

    @tornado.gen.coroutine
    def delete(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err)
        args = ['tag_id']
        meta = self.get_args(args)
        meta['problem_id'] = id
        err, res = yield from Service.Problems.delete_problem_tag(meta)
        if err: self.render(err)
        else: self.render()
