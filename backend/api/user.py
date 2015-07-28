from req import RequestHandler
from req import reqenv
from req import Service


class ApiUserSignupHandler(RequestHandler):
    @reqenv
    def post(self):
        args = ['account', 'student_id', 'passwd', 'repasswd']
        meta = self.get_args(args)
        err, id = yield from Service.User.signup(meta)
        if err:
            self.error(err)
            return
        self.success({'id': id})
        return 

class ApiUserSigninHandler(RequestHandler):
    @reqenv
    def post(self):
        args = ['account', 'passwd']
        meta = self.get_args(args)
        err, id = yield from Service.User.signin(meta, self)
        if err:
            self.error(err)
            return
        self.success({'id': id})
        return

class ApiUserChangePasswordHandler(RequestHandler):
    @reqenv
    def post(self, id):
        args = ['passwd', 'npasswd', 'rnpasswd']
        meta = self.get_args(args)
        meta['id'] = id
        err, id = yield from Service.User.change_password(meta, self.acct)
        if err:
            self.error(err)
            return
        self.success({'id': id})
        return

class ApiUserLogoutHandler(RequestHandler):
    @reqenv
    def post(self):
        self.clear_cookie('id')
        return

    @reqenv
    def get(self):
        self.clear_cookie('id')
        self.redirect('/')
        return

class ApiUserInfoHandler(RequestHandler):
    @reqenv
    def get(self, id):
        err, meta = yield from Service.User.get_user_info(str(id))
        if err:
            self.error(err)
            return
        self.success(meta)
        return

class ApiUserListHandler(RequestHandler):
    @reqenv
    def get(self):
        err, meta = yield from Service.User.get_user_list()
        if err:
            self.error(err)
            return
        self.success(meta)
        return
