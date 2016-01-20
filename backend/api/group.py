from req import ApiRequestHandler
from req import Service
import tornado
from map import *

class ApiGroupHandler(ApiRequestHandler):
    def check_edit(self, meta={}):
        if meta['id'] == 0 and map_power['group_manage'] in self.account['power']:
            return True
        if map_group_power['group_manage'] not in self.current_group_power:
            self.render(403, 'Permission Denied')
            return False
        return True

    @tornado.gen.coroutine
    def get(self):
        meta = {}
        meta['id'] = self.current_group
        err, data = yield from Service.Group.get_group(meta)
        if err: self.render(500, err)
        else: self.render(200, data)

    @tornado.gen.coroutine
    def post(self):
        args = ['name', 'description']
        meta = self.get_args(args)
        meta['id'] = self.current_group
        if not self.check_edit(meta):
            self.render(403)
            return
        err, data = yield from Service.Group.post_group(meta)
        if err: self.render(500, err)
        else:
            meta = {}
            meta['group_id'] = data
            meta['user_id'] = self.account['id']
            print(meta)
            self.render(200, {"id": data})
            err, res = yield from Service.Group.post_group_user(meta)
            for i in range(1, 6):
                yield from Service.User.post_user_group_power(self.account['id'], data, i)

    @tornado.gen.coroutine
    def delete(self):
        meta = {}
        meta['id'] = self.current_group
        if not self.check_edit():
            self.render(403)
        err, res = yield from Service.Group.delete_group(meta)
        if err: self.render(500, err)
        else: self.render(200, res)

class ApiGroupUserHandler(ApiRequestHandler):
    def check_edit(self, meta={}):
        if map_group_power['group_manage'] not in self.current_group_power:
            self.render(403, 'Permission Denied')
            return False
        return True
    @tornado.gen.coroutine
    def get(self, user_id):
        meta = {}
        meta['group_id'] = self.current_group
        meta['user_id'] = user_id
        err, data = yield from Service.User.get_user_group_power_info(self.current_group, user_id)
        if err: self.render(500, err)
        else: self.render(200, data)

    @tornado.gen.coroutine
    def post(self, user_id):
        args = ['power']
        meta = self.get_args(args)
        meta['user_id'] = user_id
        meta['group_id'] = self.current_group
        if not self.check_edit():
            self.render(403)
            return
        if meta['power'] is None:
            err, res = yield from Service.Group.post_group_user(meta)
            if err: self.render(500, err)
            else: self.render(200, res)
        else:
            err, res = yield from Service.User.post_user_group_power(meta)
            if err: self.render(500, err)
            else: self.render(200, res)
    @tornado.gen.coroutine
    def delete(self, user_id):
        meta = {}
        meta['group_id'] = self.current_group
        meta['user_id'] = user_id
        err, res = yield from Service.Group.delete_group_user(meta)
        if err: self.render(500, err)
        else: self.render(200, res)
