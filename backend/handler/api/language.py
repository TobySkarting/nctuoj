from req import ApiRequestHandler
from req import Service
import tornado

class Languages(ApiRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        err, res = yield from Service.Language.get_language_list()
        if err:
            self.render(err)
        else:
            self.render(res)
