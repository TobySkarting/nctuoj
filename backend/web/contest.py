from req import WebRequestHandler
from req import Service


class WebContestsHandler(WebRequestHandler):
    def get(self):
        args = ["page"]
        meta = self.get_args(args)
        meta["page"] = meta["page"] if meta["page"] else 1
        meta["group_id"] = self.current_group
        self.Render('./contests/contests.html')

    def post(self):
        pass

class WebContestHandler(WebRequestHandler):
    def get(self, id=None, action=None):
        pass

    def post(self): 
        pass
