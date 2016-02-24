from req import ApiRequestHandler
from req import Service
from map import map_group_power
import tornado


class ApiProblemsHandler(ApiRequestHandler):
    def check_edit(self, meta):
        if map_group_power['problem_manage'] not in self.current_group_power:
            self.render(403, "Permission Denied")
            return False
    def get(self):
        pass
    @tornado.gen.coroutine
    def post(self):
        args = ["title", "description", "input", "output", "sample_input", "sample_output", "hint", "source", "visible", 'verdict_id', 'verdict_code[file]', 'verdict_execute_type_id', 'pdf', 'pdf_file[file]']
        meta = self.get_args(args)
        meta['group_id'] = self.current_group
        meta['setter_user_id'] = self.account['id']
        err, data = yield from Service.Problem.post_problem(meta)
        if err: self.render(500, err)
        else: self.render(200, {"id": data})

class ApiProblemHandler(ApiRequestHandler):
    def check_view(self, meta):
        err, data = yield from Service.Problem.get_problem(meta)
        if err:
            self.render(500, err)
            return False
        else:
            if int(data['group_id']) == int(meta['group_id']) and (int(data['visible']) > 0 or map_group_power['problem_manage'] in self.current_group_power):
                pass
            else:
                self.render(403, "Permission Denied")
                return False
        return True

    def check_edit(self, meta):
        if map_group_power['problem_manage'] not in self.current_group_power:
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

    @tornado.gen.coroutine
    def get(self, id):
        meta = {}
        meta['id'] = id
        meta['group_id'] = self.current_group

        if not (yield from self.check_view(meta)):
            return

        err, data = yield from Service.Problem.get_problem(meta)
        self.render(200, data)
        
    @tornado.gen.coroutine
    def put(self, id):
        check_meta = {}
        check_meta['group_id'] = self.current_group
        check_meta['id'] = id
        if not (yield from self.check_edit(check_meta)):
            return
        args = ["title", "description", "input", "output", "sample_input", "sample_output", "hint", "source", "visible", 'verdict_id', 'verdict_code[file]', 'verdict_execute_type_id', 'pdf', 'pdf_file[file]']
        meta = self.get_args(args)
        meta['group_id'] = self.current_group
        meta['setter_user_id'] = self.account['id']
        meta['id'] = id
        err, data = yield from Service.Problem.put_problem(meta)
        if err: self.render(500, err)
        else: self.render(200, {"id": data})
    
    @tornado.gen.coroutine
    def delete(self, id):
        check_meta = {}
        check_meta['group_id'] = self.current_group
        check_meta['id'] = id
        if not (yield from self.check_edit(check_meta)):
            return
        meta = {}
        meta['id'] = id
        err, data = yield from Service.Problem.delete_problem(meta)
        if err: self.render(500, err)
        else: self.render()

class ApiProblemExecuteHandler(ApiRequestHandler):
    def check_edit(self, meta):
        if map_group_power['problem_manage'] not in self.current_group_power:
            self.render(403, "Permission Denied")
            return False
        err, data = yield from Service.Problem.get_problem(meta)
        if err: 
            self.render(500, err)
            return False
        if int(data['group_id']) != int(meta['group_id']):
            self.render('403', 'Permission Denied')
            return False
        return True

    def check_view(self, meta):
        err, data = yield from Service.Problem.get_problem(meta)
        print('E', err)
        if err:
            self.render(500, err)
            return False
        else:
            if int(data['group_id']) == int(meta['group_id']) and (int(data['visible']) > 0 or map_group_power['problem_manage'] in self.current_group_power):
                pass
            else:
                self.render(403, "Permission Denied")
                return False
        return True

    @tornado.gen.coroutine
    def get(self, id):
        meta = {}
        meta['id'] = id
        meta['group_id'] = self.current_group
        if not (yield from self.check_view(meta)):
            return
        err, data = yield from Service.Problem.get_problem_execute({"problem_id": meta['id']})
        print(err)
        if err: self.render(500, err)
        self.render(200, data)


    @tornado.gen.coroutine
    def put(self, id):
        print('in')
        args = ['execute[]']
        meta = self.get_args(args)
        meta['group_id'] = self.current_group
        meta['id'] = id
        if not (yield from self.check_edit(meta)):
            return
        err, data = yield from Service.Problem.put_problem_execute(meta)
        if err: self.render(500, err)
        else: self.render()

class ApiProblemRejudgeHandler(ApiRequestHandler):
    def check_edit(self, meta):
        if map_group_power['problem_manage'] not in self.current_group_power:
            self.render(403, "Permission Denied")
            return False
        err, data = yield from Service.Problem.get_problem(meta)
        if err: 
            self.render(500, err)
            return False
        if int(data['group_id']) != int(meta['group_id']):
            self.render('403', 'Permission Denied')
            return False
        return True
    @tornado.gen.coroutine
    def post(self, id):
        meta = {}
        meta['id'] = id
        meta['group_id'] = self.current_group
        if not (yield from self.check_edit(meta)):
            return
        err, res = yield from Service.Problem.post_rejudge_problem(meta)
        if err: self.render(500, err)
        else: self.render()

class ApiProblemTagHandler(ApiProblemHandler):
    def check_view(self, meta):
        err, data = yield from Service.Problem.get_problem(meta)
        print('E', err)
        if err:
            self.render(500, err)
            return False
        else:
            if int(data['group_id']) == int(meta['group_id']) and (int(data['visible']) > 0 or map_group_power['problem_manage'] in self.current_group_power):
                pass
            else:
                self.render(403, "Permission Denied")
                return False
        return True
    def check_edit(self, meta):
        if map_group_power['problem_manage'] not in self.current_group_power:
            self.render(403, "Permission Denied")
            return False
        err, data = yield from Service.Problem.get_problem(meta)
        if err: 
            self.render(500, err)
            return False
        if int(data['group_id']) != int(meta['group_id']):
            self.render('403', 'Permission Denied')
            return False
        return True
    @tornado.gen.coroutine
    def get(self, id):
        meta = {}
        meta['id'] = id
        meta['group_id'] = self.current_group
        if not (yield from self.check_view(meta)):
            return 
        err, data = yield from Service.Problems.get_problem_tag({'problem_id': meta['id']})
        if err: self.redner(500, err)
        else: self.render(200, data)

    @tornado.gen.coroutine
    def post(self, id):
        args = ['tag_id']
        meta = self.get_args(args)
        meta['problem_id'] = id
        meta['group_id'] = self.current_group
        if not (yield from self.check_edit(meta)):
            return 
        err, res = yield from Service.Problems.post_problem_tag(meta)
        if err: self.render(500, err)
        else: self.render()
        pass

    @tornado.gen.coroutine
    def delete(self, id):
        args = ['tag_id']
        meta = self.get_args(args)
        meta['problem_id'] = id
        meta['group_id'] = self.current_group
        if not (yield from self.check_edit(meta)):
            return
        err, res = yield from Service.Problems.delete_problem_tag(meta)
        if err: self.render(500, err)
        else: self.render()
