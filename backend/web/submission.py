from req import WebRequestHandler
from req import Service
import tornado



class WebSubmissionsHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        args = ["page", "user_id", "problem_id"]
        meta = self.get_args(args)
        meta["page"] = meta["page"] if meta["page"] else 1
        meta["count"] = 10
        meta["group_id"] = self.current_group
        err, data = yield from Service.Submission.get_submission_list(meta)
        self.Render('./submissions/submissions.html', data=data)

class WebSubmissionHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self, id, action=None):
        err, data = yield from Service.Submission.get_submission({'id': id})
        if err:
            self.write_error(404)
        self.Render('./submissions/submission.html', data=data)
