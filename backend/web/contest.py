from req import RequestHandler
from req import Service


class WebContestsHandler(RequestHandler):
    def get(self, group_id):
        self.current_group = group_id
        args = ["page"]
        meta = self.get_args(args)
        meta["page"] = meta["page"] if meta["page"] else 1
        meta["group_id"] = group_id
        self.render('./contests/contests.html')
        pass

    def post(self):
        pass

class WebContestHandler(RequestHandler):
    def get(self, id=None, action=None):
        pass

    def post(self): 
        pass
