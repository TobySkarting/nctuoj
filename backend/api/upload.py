from req import Service
from req import ApiRequestHandler
import tornado

class ApiUploadHandler(ApiRequestHandler):
    @tornado.gen.coroutine
    def post(self):
        err = yield from Service.Permission.check(req)
        if err: self.render(err); return
        args = ['upload_file[file]']
        meta = self.get_args(args)
        meta['group_id'] = self.current_group
        print(meta)
        err , filename = Service.Upload.post_upload(meta)
        if err: self.render(err)
        else: self.render(filename)
