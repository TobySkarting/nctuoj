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
        err = yield from Service.Permission.check(self)
        if err: self.render(err); return
        args = ['name', 'description', 'type']
        meta = self.get_args(args)
        err, data = yield from Service.Group.post_group(meta)
        if err: self.render(err)
        meta = {}
        meta['group_id'] = data
        meta['user_id'] = self.account['id']
        meta['force'] = True
        err, res = yield from Service.Group.post_group_user(meta)
        for i in range(1, 6):
            meta['power'] = i
            try: yield from Service.Group.post_group_user_power(meta)
            except Exception as e: print(e)
        print(data)
        self.render(data)

class ApiGroupHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        err, data = yield from Service.Group.get_group({'id': self.current_group})
        if err: self.render(err)
        else: self.render(data)

    @tornado.gen.coroutine
    def put(self):
        err = yield from Service.Permission.check(self, id=self.current_group)
        if err: self.render(err); return
        args = ['name', 'description', 'type']
        meta = self.get_args(args)
        meta['id'] = self.current_group
        err, data = yield from Service.Group.put_group(meta)
        if err: self.render(err)
        else: self.render(data)

    @tornado.gen.coroutine
    def delete(self):
        err = yield from Service.Permission.check(self, id=self.current_group)
        if err: self.render(err); return
        err, res = yield from Service.Group.delete_group({'id': self.current_group})
        if err: self.render(err)
        else: self.render(res)

class ApiGroupAddusersHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def post(self):
        err = yield from Service.Permission.check(self)
        if err: self.render(err); return
        args = ['user_ids[]', 'user_accounts[]', 'user_names[]', 'user_student_ids[]']
        meta = self.get_args(args)
        meta['group_id'] = self.current_group
        err, res = yield from Service.Group.post_group_addusers(meta)
        if err: self.render(err)
        else: self.render()

class ApiGroupUserHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self, user_id):
        err = yield from service.permission.check(self, user_id=user_id)
        if err: self.render(err); return
        meta = {}
        meta['group_id'] = self.current_group
        meta['user_id'] = user_id
        err, data = yield from Service.Group.get_group_user_power(meta)
        if err: self.render(err)
        else: self.render(data)

    @tornado.gen.coroutine
    def post(self, user_id):
        err = yield from Service.Permission.check(self, user_id=user_id)
        if err: self.render(err); return
        args = ['force']
        meta = self.get_args(args)
        meta['user_id'] = user_id
        meta['group_id'] = self.current_group
        err, res = yield from Service.Group.post_group_user(meta)
        if err: self.render(err)
        else: self.render(res)

    @tornado.gen.coroutine
    def delete(self, user_id):
        print('IUN')
        err = yield from Service.Permission.check(self, user_id=user_id)
        print('ERR', err)
        if err: self.render(err); return
        meta = {}
        meta['group_id'] = self.current_group
        meta['user_id'] = user_id
        err, res = yield from Service.Group.delete_group_user(meta)
        if err: self.render(err)
        else: self.render(res)

class ApiGroupUserPowerHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self, user_id):
        err = yield from Service.Permission.check(self, user_id=user_id)
        if err: self.render(err); return
        meta = {}
        meta['group_id'] = self.current_group
        meta['user_id'] = user_id
        err, data = yield from Service.Group.get_group_user_power(meta)
        if err: self.render(err)
        else: self.render(data)

    @tornado.gen.coroutine
    def post(self, user_id):
        err = yield from Service.Permission.check(self)
        if err: self.render(err); return
        args = ['power']
        meta = self.get_args(args)
        meta['user_id'] = user_id
        meta['group_id'] = self.current_group
        err, res = yield from Service.Group.post_group_user_power(meta)
        if err: self.render(err)
        else: self.render(res)
