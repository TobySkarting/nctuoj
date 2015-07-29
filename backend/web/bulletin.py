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
            if not err:
                self.render('./bulletins/bulletin.html', data=data)
                return
        if action == "edit":
            self.render('./bulletins/bulletin_edit.html')
            return
            
        
        
        self.render('./404.html')

    @reqenv
    def post(self): 
        pass
