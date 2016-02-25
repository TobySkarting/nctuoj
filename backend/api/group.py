from req import ApiRequestHandler
from req import Service
import tornado
from map import *

class ApiGroupsHandler(ApiRequestHandler):
    def check_edit(self, meta={}):
        if map_power['group_manage'] not in self.account['power']:
            self.render((403, 'Permission Denied'))
            return False
        return True

    @tornado.gen.coroutine
    def post(self):
        if not self.check_edit():
            return
        args = ['name', 'description']
        meta = self.get_args(args)
        err, data = yield from Service.Group.post_group(meta)
        if err: self.render(err)
        meta = {}
        meta['group_id'] = data
        meta['user_id'] = self.account['id']
        err, res = yield from Service.Group.post_group_user(meta)
        for i in range(1, 6):
            meta['power'] = i
            try: yield from Service.Group.post_group_user_power(meta)
            except Exception as e: print(e)
        print(data)
        self.render(data)

class ApiGroupHandler(ApiRequestHandler):
    def check_edit(self, meta={}):
        if meta['id'] == 0 and map_power['group_manage'] in self.account['power']:
            return True
        print(self.current_group_power)
        if map_group_power['group_manage'] not in self.current_group_power:
            self.render((403, 'Permission Denied'))
            return False
        return True

    @tornado.gen.coroutine
    def get(self):
        meta = {}
        meta['id'] = self.current_group
        err, data = yield from Service.Group.get_group(meta)
        if err: self.render(err)
        else: self.render(data)

    @tornado.gen.coroutine
    def put(self):
        args = ['name', 'description']
        meta = self.get_args(args)
        meta['id'] = self.current_group
        if not self.check_edit(meta):
            return
        err, data = yield from Service.Group.put_group(meta)
        if err: self.render(err)
        self.render(data)

    @tornado.gen.coroutine
    def delete(self):
        meta = {}
        meta['id'] = self.current_group
        print('META', meta)
        if not self.check_edit(meta):
            print('ERROR')
            return
        err, res = yield from Service.Group.delete_group(meta)
        print('err', err, res)
        if err: self.render(err)
        else: self.render(res)

class ApiGroupUserHandler(ApiRequestHandler):
    def check_edit(self, meta={}):
        if map_group_power['group_manage'] not in self.current_group_power:
            self.render('Permission Denied')
            return False
        return True
    @tornado.gen.coroutine
    def get(self, user_id):
        meta = {}
        meta['group_id'] = self.current_group
        meta['user_id'] = user_id
        err, data = yield from Service.Group.get_group_user_power(meta)
        if err: self.render(err)
        else: self.render(data)

    @tornado.gen.coroutine
    def post(self, user_id):
        meta = {}
        meta['user_id'] = user_id
        meta['group_id'] = self.current_group
        err, res = yield from Service.Group.post_group_user(meta)
        if err: self.render(err)
        else: self.render(res)
    @tornado.gen.coroutine
    def delete(self, user_id):
        meta = {}
        meta['group_id'] = self.current_group
        meta['user_id'] = user_id
        err, res = yield from Service.Group.delete_group_user(meta)
        if err: self.render(err)
        else: self.render(res)

class ApiGroupUserPowerHandler(ApiRequestHandler):
    def check_edit(self, meta={}):
        if map_group_power['group_manage'] not in self.current_group_power:
            self.render((403, 'Permission Denied'))
            return False
        return True
    @tornado.gen.coroutine
    def post(self, id):
        args = ['power']
        meta = self.get_args(args)
        meta['user_id'] = id
        meta['group_id'] = self.current_group
        if not self.check_edit():
            return
        err, res = yield from Service.Group.post_group_user_power(meta)
        if err: self.render(err)
        else: self.render(res)
