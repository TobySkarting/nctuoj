from req import RequestHandler
from req import reqenv
from req import Service


class WebSubmissionsHandler(RequestHandler):
    @reqenv
    def get(self):
        args = ["page"]
        meta = self.get_args(args)
        meta["page"] = meta["page"] if meta["page"] else 1
        meta["count"] = 10
        meta["group_id"] = self.current_group
        self.Render('./submissions/submissions.html')

class WebSubmissionHandler(RequestHandler):
    @reqenv
    def get(self, id, action):
        pass

