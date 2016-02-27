from req import WebRequestHandler
from req import Service
import tornado
import math


class WebSubmissionsHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        args = ["page", "account", "problem_id", "verdict"]
        meta = self.get_args(args)
        meta["count"] = 10
        meta["group_id"] = self.current_group

        if not meta['account']:
            meta.pop('account')

        if not meta['problem_id']:
            meta.pop('problem_id')

        if not meta['verdict']:
            meta.pop('verdict')

        ### default page is 1
        if not meta['page']:
            meta['page'] = 1
        ### if get page is not int then throw the error
        try:
            meta["page"] = int(meta["page"])
        except:
            self.write_error(500, 'Argument page error')
            return
        ### should in range
        err, count = yield from Service.Submission.get_submission_list_count(meta)
        if err:
            self.write_error(err)
            return
        page_count = max(math.ceil(count / meta['count']), 1)
        if int(meta['page']) < 1 or int(meta['page']) > page_count:
            self.write_error((500, 'Page out of range'))
            return
        
        err, data = yield from Service.Submission.get_submission_list(meta)
        if err:
            self.write_error(err)
            return
        
        ### about pagination 
        page = {}
        page['total'] = page_count
        page['current'] = meta['page']
        page['url'] = '/groups/%s/submissions/' % meta['group_id']
        args = ['account', 'problem_id', 'verdict']
        page['get'] = self.get_args(args)
        self.render('./submissions/submissions.html', data=data, page=page)

class WebSubmissionHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self, id):
        err, data = yield from Service.Submission.get_submission({'id': id, 'group_id': self.current_group})
        if err:
            self.write_error(err)
            return
        self.render('./submissions/submission.html', data=data)
