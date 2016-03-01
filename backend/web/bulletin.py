from req import WebRequestHandler
from req import Service
from map import map_group_power
import tornado
import math


class WebBulletinsHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self, action=None):
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
            self.redirect('/groups/%s/bulletins/'%meta['group_id'])
            return
        ### modify page in range (1, page_count)
        if action == None: err, count = yield from Service.Bulletin.get_bulletin_list_count_with_public(meta)
        else: err, count = yield from Service.Bulletin.get_bulletin_list_count(meta)
        if err: print(err)
        page_count = max(math.ceil(count / meta['count']), 1)
        if int(meta['page']) < 1:
            self.redirect('/groups/%s/bulletins/'%meta['group_id'])
            return
        if int(meta['page']) > page_count:
            self.redirect('/groups/%s/bulletins/?page=%s'%(meta['group_id'], str(page_count)))
            return
        ### get data
        if action == None: err, data = yield from Service.Bulletin.get_bulletin_list_with_public(meta)
        else: err, data = yield from Service.Bulletin.get_bulletin_list(meta)
        ### about pagination 
        page = {}
        page['total'] = page_count
        page['current'] = meta['page']
        page['url'] = '/groups/%s/bulletins/' % meta['group_id']
        page['get'] = {}
        self.render('./bulletins/bulletins.html', data=data, page=page)

class WebBulletinHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self, id, action):
        meta = {}
        meta["group_id"] = self.current_group
        meta["id"] = id
        if action == "": action = "view"
        if action == "view":
            err, data = yield from Service.Bulletin.get_bulletin(meta)
            if err: self.write_error(err)
            else: self.render('./bulletins/bulletin.html', data=data)
        elif action == "edit":
            ### check power
            if map_group_power['bulletin_manage'] not in self.current_group_power:
                self.write_error((403, ''))
                return
            err, data = yield from Service.Bulletin.get_bulletin(meta)
            if err: self.write_error(err)
            else: self.render('./bulletins/bulletin_edit.html', data=data)
        else:
            self.write_error((404, ''))

