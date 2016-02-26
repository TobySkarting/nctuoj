from req import ApiRequestHandler
from req import Service
from map import *
import tornado



class ApiUsersHandler(ApiRequestHandler):
    def get(self):
        pass

class ApiUserGroupHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self, id, group_id, action=None):
        if action == 'problems':
            meta = {}
            meta['id'] = id
            meta['group_id'] = group_id
            err, data = yield from Service.Group.get_group_user_problem_info(meta)
            if err: self.render(err)
            else: self.render(data)

class ApiUserHandler(ApiRequestHandler):
    def check_edit(self, meta={}):
        print('POWER', self.account['power'])
        if map_power['user_manage'] not in self.account['power']:
            self.render((403, 'Permission Denied!!'))
            return False
        return True

    @tornado.gen.coroutine
    def get(self, id):
        err, res = yield from Service.User.get_user_basic_info({'id': id})
        if int(self.account['id']) != int(id):
            res.pop('token')
            res.pop('power')
        self.render(res)

    @tornado.gen.coroutine
    def put(self, id):
        if int(id) != int(self.account['id']):
            self.render((403, 'Permission Denied'))
            return 
        args = ['npasswd', 'rpasswd', 'passwd', 'name', 'email', 'student_id', 'school_id']
        meta = self.get_args(args)
        print(meta)
        meta['id'] = id
        err, res = yield from Service.User.put_user_basic_info(meta)
        print(err)
        if err: self.render(err)
        else: self.render(res)

    @tornado.gen.coroutine
    def post(self, id):
        args = ['power']
        meta = self.get_args(args)
        if self.map_power['user_manage'] not in self.account['power']:
            self.render((403, "Permission Denied"))
            return
        meta['id'] = id
        yield from Service.User.post_user_power(meta)
        self.render()
        return

    @tornado.gen.coroutine
    def delete(self, id):
        print(self.account['power'])
        if not self.check_edit():
            return
        meta = {'id': id}
        err, res = yield from Service.User.delete_user(meta)
        if err: self.render(err)
        else: self.render(meta)

class ApiUserSignHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def post(self, action):
        if action == 'signin':
            args = ['account', 'passwd']
            meta = self.get_args(args)
            err, id = yield from Service.User.SignIn(meta, self)
            if err:
                self.render(err)
            else:
                self.render()
        elif action == 'signup':
            args = ['email', 'account', 'passwd', 'repasswd', 'name', 'school_id', 'student_id']
            meta = self.get_args(args)
            passwd = meta['passwd']
            err, id = yield from Service.User.SignUp(meta)
            if err: self.render(err)
            else:
                meta['passwd'] = passwd
                err, id = yield from Service.User.SignIn(meta, self)
                self.render()
        elif action == 'signout':
            Service.User.SignOut(self)
            self.render()
        elif action == 'resettoken':
            args = ['passwd']
            meta = self.get_args(args)
            meta['account'] = self.account
            err, token = yield from Service.User.ResetToken(meta)
            if err: self.render(err)
            self.render(token)
        else:
            self.render((404, 'Not Found'))

class ApiUserGetInfoHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        args = ['account', 'passwd']
        meta = self.get_args(args)
        err, res = yield from Service.User.get_user_info_by_account_passwd(meta)
        if err:
            self.render(err)
        else:
            self.render(res)
