from req import ApiRequestHandler
from req import Service
from map import *
import tornado



class ApiUsersHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        err = yield from Service.Permission.check(self)
        if err: self.render(err); return
        args = ['count', 'page']
        meta = self.get_args(args)
        meta['page'] = meta['page'] or 1
        meta['count'] = meta['count'] or 10
        err, data = yield from Service.User.get_user_list(meta)
        if err: self.render(err)
        else: self.render(data)

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
    @tornado.gen.coroutine
    def get(self, id):
        err, res = yield from Service.User.get_user_basic_info({'id': id})
        if int(self.account['id']) != int(id):
            res.pop('token')
            res.pop('power')
        self.render(res)

    @tornado.gen.coroutine
    def put(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err); return
        args = ['npasswd', 'rpasswd', 'passwd', 'name', 'email', 'student_id', 'school_id']
        meta = self.get_args(args)
        meta['id'] = id
        err, res = yield from Service.User.put_user_basic_info(meta)
        if err: self.render(err)
        else: self.render(res)

    @tornado.gen.coroutine
    def post(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err); return
        args = ['power']
        meta = self.get_args(args)
        meta['id'] = id
        err, res = yield from Service.User.post_user_power(meta)
        if err: self.render(err)
        else: self.render()

    @tornado.gen.coroutine
    def delete(self, id):
        err = yield from Service.Permission.check(self, id=id)
        if err: self.render(err); return
        err, res = yield from Service.User.delete_user({'id': id})
        if err: self.render(err)
        else: self.render({'id': id})

class ApiUserSigninHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def post(self):
        args = ['account', 'passwd']
        meta = self.get_args(args)
        err, id = yield from Service.User.signin(meta, self)
        if err: self.render(err)
        else: self.render()

class ApiUserSignupHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def post(self):
        args = ['email', 'account', 'passwd', 'repasswd', 'name', 'school_id', 'student_id']
        meta = self.get_args(args)
        passwd = meta['passwd']
        err, id = yield from Service.User.signup(meta)
        if err: self.render(err)
        else:
            meta['passwd'] = passwd
            err, id = yield from Service.User.signin(meta, self)
            self.render()

class ApiUserSignoutHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def post(self):
        Service.User.signout(self)
        self.render()

class ApiUserResettokenHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def post(self):
        args = ['passwd']
        meta = self.get_args(args)
        meta['account'] = self.account
        err, token = yield from Service.User.resettoken(meta)
        if err: self.render(err)
        else: self.render(token)

class ApiUserGetInfoHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def post(self):
        args = ['account', 'passwd']
        meta = self.get_args(args)
        err, res = yield from Service.User.get_user_info_by_account_passwd(meta)
        if err: self.render(err)
        else: self.render(res)
