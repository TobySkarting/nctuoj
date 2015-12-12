from req import WebRequestHandler
from req import Service
import tornado


class WebIndexHandler(WebRequestHandler):
    @tornado.gen.coroutine
    def get(self):
        """
        data = {}
        data['bulletins'] = []
        for x in self.group:
            meta = {}
            meta['group_id'] = x['id']
            err, res = yield from Service.Bulletin.get_latest_bulletin(meta)
            if res:
                res['group_name'] = x['name']
                data['bulletins'].append(res)
        self.render('index.html', data=data)
        """
        self.render('index.html')

