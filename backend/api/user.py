from req import RequestHandler
from req import Service



class ApiUsersHandler(RequestHandler):
    def get(self):
        pass

class ApiUserHandler(RequestHandler):
    def post(self, id):
        args = ['basic_info', 'power']
        meta = self.get_args(args)
        if meta['power']:
            if self.map_power['user_manage'] not in self.account['power']:
                self.error("Permission Denied")
                return
            yield from Service.User.post_user_power(id, meta['power'])
            self.success("")
            return

class ApiUserSignHandler(RequestHandler):
    def post(self, action):
        if action == 'signin':
            pass
        elif action == 'signup':
            pass
        elif action == 'signout':
            pass
        else:
            self.error("404")
