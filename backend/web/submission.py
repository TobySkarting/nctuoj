from req import RequestHandler
from req import reqenv
from req import Service


class WebSubmissionsHandler(RequestHandler):
    @reqenv
    def get(self):
        args = ["page", "user_id", "problem_id"]
        meta = self.get_args(args)
        meta["page"] = meta["page"] if meta["page"] else 1
        meta["count"] = 10
        meta["group_id"] = self.current_group
        err, data = yield from Service.Submission.get_submission_list(meta)
        self.Render('./submissions/submissions.html', data=data)

class WebSubmissionHandler(RequestHandler):
    @reqenv
    def get(self, id, action):
        pass

