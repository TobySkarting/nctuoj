from req import WebRequestHandler
from req import Service
import tornado
import math

class WebGroupHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self, id):
        err, data = yield from Service.Group.get_group({"id": id})
        self.Render('group/group.html', data=data)

    @tornado.gen.coroutine
    def post(self, id):
        pass

class WebGroupsHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        args = ["page"]
        meta = self.get_args(args)
        meta['count'] = 100
        ### default page is 1
        if not meta['page']:
            meta['page'] = 1
        ### if get page is not int then redirect to page 1 
        try:
            meta["page"] = int(meta["page"])
        except:
            self.write_error(500, 'Argument page error')
            return
        ### should in range
        err, count = yield from Service.Group.get_group_list_count()
        page_count = max(math.ceil(count / int(meta['count'])), 1)
        if int(meta['page']) < 1 or int(meta['page']) > page_count:
            self.write_error(500, 'Page out of range')
            return
        ### get data
        err, data = yield from Service.Group.get_group_list(meta)
        ### about pagination 
        page = {}
        page['total'] = page_count
        page['current'] = meta['page']
        page['url'] = '/groups/'
        page['get'] = {}
        self.Render('./group/groups.html', data=data, page=page)

