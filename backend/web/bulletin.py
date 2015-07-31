from req import RequestHandler
from req import reqenv
from req import Service
import math


class WebBulletinsHandler(RequestHandler):
    @reqenv
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
            self.redirect('/group/'+meta['group_id']+'/bulletins/')
            return
        ### modify page in range (1, page_count)
        err, count = yield from Service.Bulletin.get_bulletin_list_count(meta)
        page_count = max(math.ceil(count / meta['count']), 1)
        if int(meta['page']) < 1:
            self.redirect('/group/'+meta['group_id']+'/bulletins/')
            return
        if int(meta['page']) > page_count:
            self.redirect('/group/'+meta['group_id']+'/bulletins/?page='+str(page_count))
            return
        ### get data
        err, data = yield from Service.Bulletin.get_bulletin_list(meta)
        for x in data:
            x['content'] = x['content'].replace('\n', '<br>')
        ### about pagination 
        page = {}
        page['total'] = page_count
        page['current'] = meta['page']
        page['url'] = '/group/' + meta['group_id'] + '/bulletins/'
        page['get'] = {}
        self.Render('./bulletins/bulletins.html', data=data, page=page)

class WebBulletinHandler(RequestHandler):
    @reqenv
    def get(self, id, action):
        meta = {}
        meta["group_id"] = self.current_group
        meta["id"] = id
        if action == "": action = "view"
        if action == "view":
            err, data = yield from Service.Bulletin.get_bulletin(meta)
            if err: self.Render('./404.html')
            else: self.Render('./bulletins/bulletin.html', data=data)
        elif action == "edit":
            ### check power
            if not Service.User.check_user_group_power_info(self.account['id'], meta['group_id'], 1):
                self.Render('403.html')
                return
            err, data = yield from Service.Bulletin.get_bulletin(meta)
            if err: self.Render('./404.html')
            else: self.Render('./bulletins/bulletin_edit.html', data=data)
        else:
            self.Render('./404.html')

