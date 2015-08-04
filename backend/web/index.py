from req import RequestHandler
from req import reqenv
from req import Service


class WebIndexHandler(RequestHandler):
    @reqenv
    def get(self):
        data = {}
        data['bulletins'] = []
        for x in self.group:
            meta = {}
            meta['group_id'] = x['id']
            err, res = yield from Service.Bulletin.get_latest_bulletin(meta)
            if res:
                res['group_name'] = x['name']
                data['bulletins'].append(res)
        self.Render('index.html', data=data)
        return

    @reqenv
    def post(self):
        return
