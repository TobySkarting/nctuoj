from req import ApiRequestHandler
from req import Service
import tornado
from map import *

class ApiGroupHandler(ApiRequestHandler):

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
        if not self.check_edit():
            return
        err, data = yield from Service.Group.post_group(meta)
        if err: self.render(500, err)
        else: self.render(200, data)

    @tornado.gen.coroutine
    def delete(self):
        meta = {}
        meta['id'] = self.current_group
        if not self.check_edit():
            return
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
