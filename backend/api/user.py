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
            pass
        elif action == 'signup':
            pass
        elif action == 'signout':
            pass
        else:
            self.error("404")
