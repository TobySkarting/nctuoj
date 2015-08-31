from req import ApiRequestHandler
from req import Service
from map import *
import tornado

class ApiContestsHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        pass

    @tornado.gen.coroutine
    def post(self):
        pass
    
class ApiContestHandler(ApiRequestHandler):
    def check_view(self, meta):
        err, data = yield from Service.Contest.get_contest(meta)
        if err:
            self.render(500, data)
            return False
        if int(data['group_id']) == 1 and int(data['visible']) == 2:
            return True
        if map_group_power['admin_manage'] in self.current_group_power or int(data['visible']) != 0:
            return True
        print('POWER', self.current_group_power)
        print('')
        self.render(403, 'Permission Denied')
        return False

    def check_edit(self, meta):
        if map_group_power['admin_manage'] not in self.current_group_power:
            self.render(403, 'Permission Denied')
            return False
        if int(meta['id']) != 0:
            err, data = yield from Service.Contest.get_contest(meta)
            if err:
                self.render(500, data)
                return False
        return True

    @tornado.gen.coroutine
    def get(self, id):
        meta = {}
        meta['id'] = id
        meta['group_id'] = self.current_group
        if not (yield from self.check_view(meta)):
            return
        err, data = yield from Service.Contest.get_contest(meta)
        if err:
            self.render(500, err)
            return
        self.render(200, data)
        return


    @tornado.gen.coroutine
    def post(self, id, action=None):
        pass
