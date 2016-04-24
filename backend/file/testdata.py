from req import StaticFileHandler
from req import Service
from map import *
import tornado.gen
import re

class FileTestdataHandler(StaticFileHandler):
    @tornado.gen.coroutine
    def prepare(self):
        try:
            self.testdata_id = int(re.search(r'.*/testdata/(\d+)/.*', self.request.uri).groups(1)[0])
        except:
            raise tornado.web.HTTPError(404)
        yield super().prepare()
        err, testdata = yield from Service.Testdata.get_testdata({'id': self.testdata_id}) 
        if err: raise tornado.web.HTTPError(404)
        err, problem = yield from Service.Problem.get_problem({'id': testdata['problem_id']})
        err, group_power = yield from Service.Group.get_group_user_power({
            'user_id': self.account['id'],
            'group_id': problem['group_id'],
        })
        if map_group_power['problem_manage'] not in group_power:
            raise tornado.web.HTTPError(403)
