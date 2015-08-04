from req import RequestHandler
from req import reqenv
from req import Service


class ApiProblemsHandler(RequestHandler):
    @reqenv
    def get(self):
        pass

    @reqenv
    def post(self):
        pass

    @reqenv
    def delete(self):
        pass

class ApiProblemHandler(RequestHandler):
    @reqenv
    def get(self):
        pass
        
    @reqenv
    def post(self, id, action):
        ### /api/{{group_id}}/problems/{{problem_id}}/
        """
        args = ["title", "content"]
        meta = self.get_args(args)
        meta["group_id"] = self.current_group
        meta["setter_user_id"] = self.account['id']
        meta['id'] = id
        if not 1 in self.current_group_power:
            self.error("Permission Denied")
            return
        err, data = yield from Service.Bulletin.post_bulletin(meta)
        """
        if err: self.error(err)
        else: self.success("")

    @reqenv
    def delete(self, id):
        meta = {}
        meta["group_id"] = self.current_group
        meta["setter_user_id"] = self.account['id']
        meta['id'] = id
        if not 1 in self.current_group_power:
            self.error("Permission Denied")
            return
        err, data = yield from Service.Bulletin.delete_bulletin(meta)
        if err: self.error(err)
        else: self.success("")
