from req import ApiRequestHandler
from req import Service
import tornado

class Problems(ApiRequestHandler):
    @tornado.gen.coroutine
    def post(self):
        args = ['group_id', 'title', 'description', 'input', 'output', 'sample_input', 'sample_output', 'hint', 'source', 'pdf', 'pdf_file[file]', 'score_type_id']
        data = self.get_args(args)
        data['setter_user_id'] = self.account['id']
        err, res = yield from Service.problem.Problem.post_problem(data)
        if err:
            self.render(err)
        else:
            err, res = yield from Service.problem.Problem.get_problem(res)
            self.render(res)

class Problem(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self, id):
        err, res = yield from Service.problem.Problem.get_problem({'id': id})
        if err:
            self.render(err)
        else:
            self.render(res)

    @tornado.gen.coroutine
    def put(self, id):
        args = ['title', 'description', 'input', 'output', 'sample_input', 'sample_output', 'hint', 'source', 'pdf', 'pdf_file[file]', 'score_type_id']
        data = self.get_args(args)
        data['setter_user_id'] = self.account['id']
        data['id'] = id
        err, res = yield from Service.problem.Problem.put_problem(data)
        if err:
            self.render(err)
        else:
            err, res = yield from Service.problem.Problem.get_problem({'id': id})
            self.render(res)

    @tornado.gen.coroutine
    def delete(self, id):
        err, res = yield from Service.problem.Problem.delete_problem({'id': id})
        self.render()

