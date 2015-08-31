from req import WebRequestHandler
from req import Service
import tornado
import math
from map import *


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
    def check_view(self, meta):
        err, data = yield from Service.Contest.get_contest(meta)
        if err:
            self.write_error(500)
            return False
        print('WPOWER', self.current_group_power)
        if int(data['group_id']) == 1 and int(data['visible']) == 2:
            return True
        if map_group_power['admin_manage'] in self.current_group_power or int(data['visible']) != 0:
            return True
        self.write_error(403)
        return False

    @tornado.gen.coroutine        
    def get(self, id=None, action=None):
        meta = {}
        meta['id'] = id
        meta['group_id'] = self.current_group
        if not (yield from self.check_view(meta)):
            return
        err, data = yield from Service.Contest.get_contest(meta)
        if action == None:
            self.Render('./contests/contest.html', data=data)
        else:
            self.write_error(404)

