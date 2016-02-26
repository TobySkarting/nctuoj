from req import ApiRequestHandler
from req import Service
import tornado
from map import map_group_power


class ApiBulletinsHandler(ApiRequestHandler):
    def check(self, meta):
        if map_group_power['bulletin_manage'] not in self.current_group_power:
            self.render((403, "Permission Denied"))
            return False
        if int(meta['id']) != 0:
            err, data = yield from Service.Bulletin.get_bulletin(meta)
            if err: 
                self.render(err)
                return False
            if int(data['group_id']) != int(meta['group_id']):
                self.render((403, "Permission Denied"))
                return False
        return True

    @tornado.gen.coroutine
    def get(self):
        meta = {}
        meta['group_id'] = self.current_group
        meta['page'] = 1
        meta['count'] = 10**9
        err, data = yield from Service.Bulletin.get_bulletin_list(meta)
        if err: self.render(err)
        else: self.render(data)

    @tornado.gen.coroutine
    def post(self):
        err = yield from Service.Permission.check(self)
        if err:
            self.render(err)
            return
        args = ["title", "content"]
        meta = self.get_args(args)
        meta["group_id"] = self.current_group
        meta["setter_user_id"] = self.account['id']
        err, data = yield from Service.Bulletin.post_bulletin(meta)
        if err: self.render(err)
        else: self.render()

class ApiBulletinHandler(ApiRequestHandler):
    def check(self, meta):
        if map_group_power['bulletin_manage'] not in self.current_group_power:
            self.render((403, "Permission Denied"))
            return False
        if int(meta['id']) != 0:
            err, data = yield from Service.Bulletin.get_bulletin(meta)
            if err: 
                self.render(err)
                return False
            if int(data['group_id']) != int(meta['group_id']):
                self.render((403, "Permission Denied"))
                return False
        return True

    @tornado.gen.coroutine
    def get(self, id):
        meta = {}
        meta['id'] = id
        meta['group_id'] = self.current_group
        err, data = yield from Service.Bulletin.get_bulletin(meta)
        if err:
            self.render(err)
        else:
            self.render(data)
    
    @tornado.gen.coroutine
    def put(self, id):
        args = ["title", "content"]
        meta = self.get_args(args)
        meta["group_id"] = self.current_group
        meta["setter_user_id"] = self.account['id']
        meta['id'] = id
        if self.check(meta):
            err, data = yield from Service.Bulletin.put_bulletin(meta)
            if err: self.render(err)
            else: self.render()

    
    @tornado.gen.coroutine
    def delete(self, id):
        meta = {}
        meta["group_id"] = self.current_group
        meta["setter_user_id"] = self.account['id']
        meta['id'] = id
        if self.check(meta):
            err, data = yield from Service.Bulletin.delete_bulletin(meta)
            if err: self.render(err)
            else: self.render()
