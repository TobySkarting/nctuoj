from req import RequestHandler
from req import reqenv
from req import Service


class ApiBulletinsHandler(RequestHandler):
    @reqenv
    def get(self):
        self.success({'group_id': self.current_group})
        pass

    @reqenv
    def post(self):
        pass

    @reqenv
    def delete(self):
        pass

class ApiBulletinHandler(RequestHandler):
    @reqenv
    def get(self):
        pass

    @reqenv
    def post(self):

        pass

    @reqenv
    def delete(self):
        pass
