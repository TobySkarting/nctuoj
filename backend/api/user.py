from req import ApiRequestHandler
from req import Service
import tornado



class ApiUsersHandler(ApiRequestHandler):
    def get(self):
        pass

class ApiUserHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def post(self, id):
        args = ['basic_info', 'power']
        meta = self.get_args(args)
        print('META', meta)
        if meta['power']:
            if self.map_power['user_manage'] not in self.account['power']:
                self.render(403, "Permission Denied")
                return
            yield from Service.User.post_user_power(id, meta['power'])
            self.render()
            return

class ApiUserSignHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def post(self, action):
        if action == 'signin':
            args = ['account', 'passwd']
            meta = self.get_args(args)
            err, id = yield from Service.User.SignIn(meta, self)
            if err:
                self.render(403, 'Wrong Password')
            else:
                self.render()
        elif action == 'signup':
            args = ['email', 'account', 'passwd', 'repasswd', 'school_id', 'student_id']
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
