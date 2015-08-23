from req import ApiRequestHandler
from req import Service
import tornado


class ApiBulletinsHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        pass

class ApiBulletinHandler(ApiRequestHandler):
    def check(self, meta):
        if 1 not in self.current_group_power:
            self.render(403, "Permission Denied")
            return False
        if int(meta['id']) != 0:
            err, data = yield from Service.Bulletin.get_bulletin(meta)
            if err: 
                self.render(500, err)
                return False
            if int(data['group_id']) != int(meta['group_id']):
                self.render(403, "Permission Denied")
                return False
        return True

    @tornado.gen.coroutine
    def get(self, id):
        pass

    
    @tornado.gen.coroutine
    def post(self, id):
        args = ["title", "content"]
        meta = self.get_args(args)
        meta["group_id"] = self.current_group
        meta["setter_user_id"] = self.account['id']
        meta['id'] = id
        if self.check(meta):
            err, data = yield from Service.Bulletin.post_bulletin(meta)
            if err: self.render(500 ,err)
            else: self.render()

    
    @tornado.gen.coroutine
    def delete(self, id):
        meta = {}
        meta["group_id"] = self.current_group
        meta["setter_user_id"] = self.account['id']
        meta['id'] = id
        if self.check(meta):
            err, data = yield from Service.Bulletin.delete_bulletin(meta)
            if err: self.render(500, err)
            else: self.render()
