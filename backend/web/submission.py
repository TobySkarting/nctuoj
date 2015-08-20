from req import WebRequestHandler
from req import Service
import tornado
import math



class WebSubmissionsHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        args = ["page", "user_id", "problem_id"]
        meta = self.get_args(args)
        meta["count"] = 10
        meta["group_id"] = self.current_group
        ### default page is 1
        if not meta['page']:
            meta['page'] = 1
        ### if get page is not int then redirect to page 1 
        try:
            meta["page"] = int(meta["page"])
        except:
            self.write_error(404)
            return
        ### should in range
        err, count = yield from Service.Submission.get_submission_list_count(meta)
        page_count = max(math.ceil(count / meta['count']), 1)
        if int(meta['page']) < 1 or int(meta['page']) > page_count:
            self.write_error(404)
            return
        
        err, data = yield from Service.Submission.get_submission_list(meta)

        ### about pagination 
        page = {}
        page['total'] = page_count
        page['current'] = meta['page']
        page['url'] = '/group/%s/submissions/' % meta['group_id']
        args = ['user_id', 'problem_id']
        page['get'] = self.get_args(args)
        self.Render('./submissions/submissions.html', data=data, page=page)

class WebSubmissionHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self, id, action=None):
        err, data = yield from Service.Submission.get_submission({'id': id})
        if err:
            self.write_error(404)
        self.Render('./submissions/submission.html', data=data)
