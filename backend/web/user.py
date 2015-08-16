from req import RequestHandler
from req import reqenv
from req import Service
import math


class WebUsersHandler(RequestHandler):
    @reqenv
    def get(self):
        if self.map_power['user_manage'] not in self.account['power']:
            self.write_error(403)
            return
        args = ["page"]
        meta = self.get_args(args)
        meta['count'] = 10
        ### default page is 1
        if not meta['page']:
            meta['page'] = 1
        ### if get page is not int then redirect to page 1 
        try:
            meta["page"] = int(meta["page"])
        except:
            self.redirect('/executes/')
            return
        ### modify page in range (1, page_count)
        err, count = yield from Service.User.get_user_list_count()
        print(count, type(count))
        page_count = max(math.ceil(count / meta['count']), 1)
        if int(meta['page']) < 1:
            self.redirect('/users/')
            return
        if int(meta['page']) > page_count:
            self.redirect('/users/?page=%s'%str(page_count))
            return
        err, data = yield from Service.User.get_user_list(meta)
        ### about pagination
        page = {}
        page['total'] = page_count
        page['current'] = meta['page']
        page['url'] = '/users/'
        page['get'] = {}
        self.Render('./users/users.html', data=data, page=page)

    @reqenv
    def post(self):
        pass

class WebUserHandler(RequestHandler):
    """ single user data """
    @reqenv
    def get(self, id=None, action=None):
        if not id: id = self.account["id"]
        err, meta = yield from Service.User.get_user_advanced_info(id)
        self.Render('./users/user.html', data=meta)

    """ update user data """
    @reqenv
    def post(self, id=None, action=None):
        pass

class WebUserSignHandler(RequestHandler):
    @reqenv
    def get(self, action):
        print(action)
        if action == "signin":
            self.Render('./users/user_signin.html')
        elif action == "signout":
            Service.User.SignOut(self)
            self.redirect('/')
        elif action == "signup":
            self.Render('./users/user_signup.html')
        else:
            self.write_error(404)

    @reqenv
    def post(self, action): 
        if action == "signin":
            args = ['account', 'passwd']
            meta = self.get_args(args)
            err, id = yield from Service.User.SignIn(meta, self)
            if err:
                self.Render('./users/user_signin.html')
            else:
                self.redirect('/')
        elif action == "signout":
            Service.User.SignOut(self)
            self.redirect('/')
        elif action == "signup":
            args = ['email', 'account', 'passwd', 'repasswd', 'school_id', 'student_id']
            meta = self.get_args(args)
            passwd = meta['passwd']
            err, id = yield from Service.User.SignUp(meta)
            if err:
                self.Render('./users/user_signup.html')
            else:
                meta['passwd'] = passwd
                err, id = yield from Service.User.SignIn(meta, self)
                self.redirect('/')
        else:
            self.write_error(404)
