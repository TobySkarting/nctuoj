from req import ApiRequestHandler
from req import Service
from map import *
import tornado

class ApiTestdatasHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def post(self):
        args = ['problem_id', 'score', 'time_limit', 'memory_limit', 'output_limit', 'input[file]', 'output[file]']
        meta = self.get_args(args)
        meta['group_id'] = self.current_group
        err = yield from Service.Permission.check(self, meta)
        if err: self.render(err); return
        err, res = yield from Service.Testdata.post_testdata(meta)
        if err: self.render(err)
        else: self.render(res)

class ApiTestdataHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err); return
        err, data = yield from Service.Testdata.get_testdata({'id': id})
        if err: self.render(err)
        self.render(data)

    @tornado.gen.coroutine
    def put(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err); return
        args = ['problem_id', 'score', 'time_limit', 'memory_limit', 'output_limit', 'input[file]', 'output[file]']
        meta = self.get_args(args)
        meta['id'] = id
        err, res = yield from Service.Testdata.put_testdata(meta)
        if err: self.render(err)
        else: self.render(res)

    @tornado.gen.coroutine
    def delete(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err); return
        err, res = yield from Service.Testdata.delete_testdata({'id': id})
        if err: self.render(err)
        else: self.render()
