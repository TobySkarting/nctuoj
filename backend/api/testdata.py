from req import ApiRequestHandler
from req import Service
from map import *
import tornado

class ApiTestdataHandler(ApiRequestHandler):
    def check_edit(self, meta):
        err, problem = yield from Service.Problem.get_problem({'id': meta['problem_id']})
        if err: 
            self.render(500, err)
            return False
        if int(meta['group_id']) != int(problem['group_id']) or map_group_power['problem_manage'] not in self.current_group_power:
            self.render(403, 'Permission Denied')
            return False
        if int(meta['id']) == 0:
            return True
        err, testdata = yield from Service.Testdata.get_testdata(meta) 
        if err: 
            self.render(500, err)
            return False
        if int(testdata['problem_id']) != int(problem['id']):
            self.render(404, 'No map testdata ans problem')
            return False
        return True

    def check_view(self, meta={}):
        err, problem = yield from Service.Problem.get_problem({'id': meta['problem_id']})
        if err: 
            self.render(500, err)
            return False
        if int(problem['group_id']) != int(meta['group_id']):
            self.render(403, 'Permission Denied')
            return False
        err, testdata = yield from Service.Testdata.get_testdata(meta)
        if err: 
            self.render(500, err)
            return False
        if int(testdata['problem_id']) != int(problem['id']):
            return (404, 'No testdata')
        return True

    @tornado.gen.coroutine
    def get(self, id):
        args = ['problem_id']
        meta = self.get_args(args)
        meta['id'] = id
        meta['group_id'] = self.current_group
        if not (yield from self.check_view(meta)):
            return
        pass

    @tornado.gen.coroutine
    def post(self, id):
        args = ['problem_id', 'score', 'time_limit', 'memory_limit', 'output_limit', 'input[file]', 'output[file]']
        meta = self.get_args(args)
        meta['id'] = id
        meta['group_id'] = self.current_group
        if not (yield from self.check_edit(meta)):
            return
        err, res = yield from Service.Testdata.post_testdata(meta)
        if err: self.render(500, err)
        else: self.render(200, res)

    @tornado.gen.coroutine
    def delete(self, id):
        args = ['problem_id']
        meta = self.get_args(args)
        meta['group_id'] = self.current_group
        meta['id'] = id
        if not (yield from self.check_edit(meta)):
            return 
        err, res = yield from Service.Testdata.delete_testdata(meta)
        if err: self.render(500, err)
        else: self.render()
