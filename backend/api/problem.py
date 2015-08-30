from req import ApiRequestHandler
from req import Service
from map import map_group_power
import tornado


class ApiProblemsHandler(ApiRequestHandler):
    def get(self):
        pass

    
    def post(self):
        pass

    
    def delete(self):
        pass

class ApiProblemHandler(ApiRequestHandler):
    def check_view(self, meta):
        err, data = yield from Service.Problem.get_problem(meta)
        if err:
            self.render(500, err)
            return False
        else:
            if int(meta['group_id']) == 1 and int(data['visible']) == 2:
                pass
            elif int(data['group_id']) == int(meta['group_id']) and (int(data['visible']) != 0 or 1 in self.current_group_power):
                pass
            else:
                self.render(403, "Permission Denied")
                return False
        return True

    def check_edit(self, meta):
        if map_group_power['admin_manage'] not in self.current_group_power:
            self.render(403, "Permission Denied")
            return False
        if int(meta['id']) != 0:
            err, data = yield from Service.Problem.get_problem(meta)
            if err: 
                self.render(500, err)
                return False
            if int(data['group_id']) != int(meta['group_id']):
                self.render('403', 'Permission Denied')
                return False
        return True

    def check_testdata(self, meta):
        if int(meta['testdata_id']) != 0:
            err, data = yield from Service.Problem.get_problem_testdata(meta)
            if err:
                self.render(500, err)
                return False
            if int(data['problem_id']) != int(meta['id']):
                self.render(403, 'Permission Denied')
                return False
        return True

    @tornado.gen.coroutine
    def get(self, id, action=None, sub_id=None):
        meta = {}
        meta['id'] = id
        meta['group_id'] = self.current_group

        if action == "execute":
            err, data = yield from Service.Problem.get_problem_execute(meta)
            self.render(200, data)
            return
    
        if not (yield from self.check_view(meta)):
            return

        err, data = yield from Service.Problem.get_problem(meta)
        if action == "basic":
            self.render(200, data)
        elif action == "tag":
            pass
        elif action == "testdata":
            if sub_id == None:
                err, data = yield from Service.Problem.get_problem_testdata_list(meta)
                if err: self.render(500, err)
                else: self.render(200, data)
            else:
                meta['testdata_id'] = sub_id
                err, data = yield from Service.Problem.get_problem_testdata(meta)
                if err: self.render(500, err)
                else: self.render()
        else:
            self.render(404)
        
    
    @tornado.gen.coroutine
    def post(self, id, action=None, sub_id=None):
        check_meta = {}
        check_meta['group_id'] = self.current_group
        check_meta['id'] = id

        if action == "submit":
            if (yield from self.check_view(check_meta)):
                args = ['execute_type_id', 'code_file[file]', 'plain_code', 'plain_file_name']
                meta = self.get_args(args)
                meta['user_id'] = self.account['id']
                meta['problem_id'] = id
                err, data = yield from Service.Submission.post_submission(meta)
                if err:
                    self.render(500, err)
                else:
                    self.render(200, data)
            return

        if (yield from self.check_edit(check_meta)):
            ### /api/{{group_id}}/problems/{{problem_id}}/basic/
            if action == "basic":
                args = ["title", "description", "input", "output", "sample_input", "sample_output", "hint", "source", "visible"]
                meta = self.get_args(args)
                meta['group_id'] = self.current_group
                meta['setter_user_id'] = self.account['id']
                meta['id'] = id
                err, data = yield from Service.Problem.post_problem(meta)
                if err: self.render(500, err)
                else: self.render(200, {"id": data})
            ### /api/{{group_id}}/problems/{{problem_id}}/execute/
            elif action == "execute":
                args = ['execute[]']
                meta = self.get_args(args)
                meta['group_id'] = self.current_group
                meta['id'] = id
                err, data = yield from Service.Problem.post_problem_execute(meta)
                if err: self.render(500, err)
                else: self.render()
            elif action == "testdata":
                args = ['score', 'time_limit', 'memory_limit', 'output_limit', 'input[file]', 'output[file]']
                meta = self.get_args(args)
                meta['testdata_id'] = sub_id
                meta['id'] = id
                if (yield from self.check_testdata(meta)):
                    err, data = yield from Service.Problem.post_problem_testdata(meta)
                    if err: self.render(500, err)
                    else: self.render()
            else: self.render(404)

    
    @tornado.gen.coroutine
    def delete(self, id, action=None, sub_id=None):
        check_meta = {}
        check_meta['group_id'] = self.current_group
        check_meta['id'] = id
        if (yield from self.check_edit(check_meta)):
            if action == "basic":
                meta = {}
                meta['id'] = id
                err, data = yield from Service.Problem.delete_problem(meta)
                if err: self.render(500, err)
                else: self.render()
            elif action == "testdata":
                meta = {}
                meta['testdata_id'] = sub_id
                meta['id'] = id
                if (yield from self.check_testdata(meta)):
                    err, data = yield from Service.Problem.delete_problem_testdata(meta)
                    if err: self.render(500, err)
                    else: self.render()
            else: self.render(404)
