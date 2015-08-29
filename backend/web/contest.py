from req import WebRequestHandler
from req import Service
import tornado
import math


class WebContestsHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        args = ["page"]
        meta = self.get_args(args)
        meta['count'] = 10
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
        err, count = yield from Service.Contest.get_contest_list_count(meta)
        page_count = max(math.ceil(count / meta['count']), 1)
        if int(meta['page']) < 1 or int(meta['page']) > page_count:
            self.write_error(404)
            return
        ### get data
        err, data = yield from Service.Contest.get_contest_list(meta)
        ### about pagination 
        page = {}
        page['total'] = page_count
        page['current'] = meta['page']
        page['url'] = '/group/%s/contests/' % meta['group_id']
        page['get'] = {}
        self.Render('./contests/contests.html', data=data, page=page)

class WebContestHandler(WebRequestHandler):
    def get(self, id=None, action=None):
        pass

