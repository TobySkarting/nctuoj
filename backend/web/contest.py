from req import WebRequestHandler
from req import Service
import tornado
import math


class WebContestsHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        data = {
                "page": 1,
                "count": 10,
                "group_id": self.current_group,
                }
        err, data = yield from Service.Contest.get_contest_list(data)
        print(data)
        self.Render('./contests/contests.html')

class WebContestHandler(WebRequestHandler):
    def get(self, id=None, action=None):
        pass

