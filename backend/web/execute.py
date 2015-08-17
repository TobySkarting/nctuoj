from req import RequestHandler
from req import reqenv
from req import Service
import math


class WebExecuteTypesHandler(RequestHandler):
    @reqenv
    def get(self):
        err, data = yield from Service.Execute.get_execute_list()
        self.Render('./executes/executes.html', data=data)
        pass

class WebExecuteTypeHandler(RequestHandler):
    @reqenv
    def get(self, id, action=None):
        meta = {}
        meta["id"] = id
        if not action : action = "view"
        if action == "view":
            err, data = yield from Service.Execute.get_execute(meta)
            if err: self.write_error(404)
            else: self.Render('./executes/execute.html', data=data)
        elif action == "edit":
            ### check power
            if self.map_power['execute_manage'] not in self.account['power']:
                self.write_error(403)
                return
            err, data = yield from Service.Execute.get_execute(meta)
            if err: self.write_error(404)
            else: self.Render('./executes/execute_edit.html', data=data)
        else:
            self.write_error(404)
