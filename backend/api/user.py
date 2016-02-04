from req import ApiRequestHandler
from req import Service
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
            err, data = yield from Service.User.get_user_group_problem_info(meta)
            if err: self.render(500, err)
            else: self.render(200, data)

class ApiUserHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self, id):
        pass
    @tornado.gen.coroutine
    def post(self, id):
        args = ['query']
        meta = self.get_args(args)
        if meta['query'] == "power":
            args = ['power']
            meta = self.get_args(args)
            if self.map_power['user_manage'] not in self.account['power']:
                self.render(403, "Permission Denied")
                return
            yield from Service.User.post_user_power(id, meta['power'])
            self.render()
            return
        if int(id) != int(self.account['id']):
            sefl.render('403', 'Permission Denied')
            return 
        args = ['npasswd', 'rpasswd', 'passwd']
        meta = self.get_args(args)
        meta['id'] = id
        err, res = yield from Service.User.post_user_basic_info(meta)
        if err: self.render(500, err)
        else: self.render(200, res)

class ApiUserSignHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def post(self, action):
        if action == 'signin':
            args = ['account', 'passwd']
            meta = self.get_args(args)
            err, id = yield from Service.User.SignIn(meta, self)
            if err:
                self.render(403, err)
            else:
                self.render()
        elif action == 'signup':
            args = ['email', 'account', 'passwd', 'repasswd', 'name', 'school_id', 'student_id']
            meta = self.get_args(args)
            passwd = meta['passwd']
            err, id = yield from Service.User.SignUp(meta)
            if err: self.render(400, err)
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
            if err: self.render(400, err)
            self.render(msg=token)
        else:
            self.render(404)
