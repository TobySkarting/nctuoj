from req import RequestHandler
from req import reqenv
from req import Service


class WebContestsHandler(RequestHandler):
    @reqenv
    def get(self, group_id):
        self.current_group = group_id
        args = ["page"]
        meta = self.get_args(args)
        meta["page"] = meta["page"] if meta["page"] else 1
        meta["group_id"] = group_id
        self.render('./contests/contests.html')
        pass

    @reqenv
    def post(self):
        pass

class WebContestHandler(RequestHandler):
    @reqenv
    def get(self, id=None, action=None):
        pass

    @reqenv
    def post(self): 
        pass
