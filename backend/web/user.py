from req import WebRequestHandler
from req import Service
import tornado
import math


class WebUsersHandler(WebRequestHandler):
    @tornado.gen.coroutine
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
            self.redirect('/users/')
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


class WebUserHandler(WebRequestHandler):
    """ single user data """
    @tornado.gen.coroutine
    def get(self, id=None, action=None):
        if not id: id = self.account["id"]
        ###err, meta = yield from Service.User.get_user_advanced_info(id)
        err, meta = yield from Service.User.get_user_basic_info(id)
        err, meta['group'] = yield from Service.User.get_user_group_info(id)
        if err:
            self.write_error(500, err)
            return
        self.Render('./users/user.html', data=meta)

class WebUserEditHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self, id):
        err, meta = yield from Service.User.get_user_basic_info(id)
        if err:
            self.write_error(500, err)
            return

class WebUserSignHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self, action):
        if action == "signin":
            if self.account['id'] != 0:
                self.redirect('/')
            self.Render('./users/user_signin.html')
        elif action == "signout":
            Service.User.SignOut(self)
            self.redirect('/')
        elif action == "signup":
            if self.account['id'] != 0:
                self.redirect('/')
            err, school = yield from Service.School.get_school_list()
            self.Render('./users/user_signup.html', school=school)
        else:
            self.write_error(404)

