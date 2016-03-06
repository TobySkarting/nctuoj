from req import ApiRequestHandler
from req import Service
import tornado
from map import map_group_power


class ApiBulletinsHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        err = yield from Service.Permission.check(self)
        if err: self.render(err); return
        args = ['page', 'count']
        meta = self.get_args(args)
        meta['page'] = meta['page'] or 1
        meta['count'] = meta['count'] or 10
        meta['group_id'] = self.current_group
        err, data = yield from Service.Bulletin.get_bulletin_list(meta)
        if err: self.render(err)
        else: self.render(data)

    @tornado.gen.coroutine
    def post(self):
        err = yield from Service.Permission.check(self)
        if err: self.render(err); return
        args = ["title", "content"]
        meta = self.get_args(args)
        meta["group_id"] = self.current_group
        meta["setter_user_id"] = self.account['id']
        err, data = yield from Service.Bulletin.post_bulletin(meta)
        if err: self.render(err)
        else: self.render()

class ApiBulletinHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err); return
        meta = {}
        meta['id'] = id
        meta['group_id'] = self.current_group
        err, data = yield from Service.Bulletin.get_bulletin(meta)
        if err: self.render(err)
        else: self.render(data)
    
    @tornado.gen.coroutine
    def put(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err); return
        args = ["title", "content"]
        meta = self.get_args(args)
        meta["group_id"] = self.current_group
        meta["setter_user_id"] = self.account['id']
        meta['id'] = id
        err, data = yield from Service.Bulletin.put_bulletin(meta)
        if err: self.render(err)
        else: self.render()

    
    @tornado.gen.coroutine
    def delete(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err); return
        err, data = yield from Service.Bulletin.delete_bulletin({"id": id})
        if err: self.render(err)
        else: self.render()
