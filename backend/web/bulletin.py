from req import RequestHandler
from req import reqenv
from req import Service


class WebBulletinsHandler(RequestHandler):
    @reqenv
    def get(self, group_id):
        args = ["page"]
        meta = self.get_args(args)
        meta["page"] = meta["page"] if meta["page"] else 1
        meta["group_id"] = group_id
        err, data = yield from Service.Bulletin.get_bulletin_list(meta)
        self.render('./bulletins/bulletins.html', data=data)

    @reqenv
    def post(self):
        pass

class WebBulletinHandler(RequestHandler):
    @reqenv
    def get(self, group_id, id, action):
        meta = {}
        meta["group_id"] = group_id
        meta["id"] = id
        if action == "": action = "view"
        if action == "view":
            err, data = yield from Service.Bulletin.get_bulletin(meta)
            if err: self.render('./404.html')
            else: self.render('./bulletins/bulletin.html', data=data)
        elif action == "edit":
            err, data = yield from Service.Bulletin.get_bulletin(meta)
            if err: self.render('./404.html')
            else: self.render('./bulletins/bulletin_edit.html', data=data)
        else:
            self.render('./404.html')

    @reqenv
    def post(self, group_id, id, action): 
        if action == "edit":
            args = ["title", "content"]
            meta = self.get_args(args)
            meta['group_id'] = group_id
            meta['setter_user_id'] = self.account['id']
            meta['id'] = id
            if not Service.User.check_user_group_power_info(meta['setter_user_id'], meta['group_id'], 1):
                self.render('403.html')
                return
            err, data = yield from Service.Bulletin.post_bulletin(meta)
            self.redirect('/group/'+group_id+'/bulletins/')
        pass
