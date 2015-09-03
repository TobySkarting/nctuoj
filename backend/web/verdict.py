from req import WebRequestHandler
from req import Service
import tornado
import math


class WebVerdictTypesHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        err, data = yield from Service.Verdict.get_verdict_list()
        self.Render('./verdicts/verdicts.html', data=data)
        pass

class WebVerdictTypeHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self, id, action=None):
        meta = {}
        meta["id"] = id
        if not action : action = "view"
        if action == "view":
            err, data = yield from Service.Verdict.get_verdict(meta)
            if err: self.write_error(500)
            else: self.Render('./verdict/verdict.html', data=data)
        elif action == "edit":
            ### check power
            if self.map_power['verdict_manage'] not in self.account['power']:
                self.write_error(403)
                return
            err, data = yield from Service.Verdict.get_verdict(meta)
            if err: self.write_error(500)
            else: self.Render('./verdict/verdict.html', data=data)
        else:
            self.write_error(404)
