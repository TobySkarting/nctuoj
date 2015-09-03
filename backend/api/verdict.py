from req import ApiRequestHandler
from req import Service
from map import *
import tornado

class ApiVerdictTypesHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        err, data = yield from Service.Verdict.get_verdict_list()
        if err: self.render(500, err)
        else: self.render(200, data)

    @tornado.gen.coroutine
    def post(self):
        pass

class ApiVerdictTypeHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self, id):
        meta = {}
        meta['id'] = id
        err, data = yield from Service.Verdict.get_verdict(meta)
        if err: self.render(500, err)
        else: self.render(200, data)

    @tornado.gen.coroutine
    def post(self, id):
        pass

    @tornado.gen.coroutine
    def delete(self, id):
        pass
