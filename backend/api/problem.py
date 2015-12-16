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
    def get(self, id, action=None, sub_id=None):
        meta = {}
        meta['id'] = id
        meta['group_id'] = self.current_group

        if action == "execute":
            err, data = yield from Service.Execute.get_problem_execute({"problem_id": meta['id']})
            self.render(200, data)
            return
    
        if not (yield from self.check_view(meta)):
            return

        err, data = yield from Service.Problem.get_problem(meta)
        if action == "basic":
            self.render(200, data)
        elif action == "tag":
            err, data = yield from Service.Tags.get_problem_tag({'problem_id': meta['id']})
            if err: self.redner(500, err)
            else: self.render(200, data)
            pass
        else:
            self.render(404)
        
    
    @tornado.gen.coroutine
    def post(self, id, action=None, sub_id=None):
        check_meta = {}
        check_meta['group_id'] = self.current_group
        check_meta['id'] = id

        if (yield from self.check_edit(check_meta)):
            ### /api/{{group_id}}/problems/{{problem_id}}/basic/
            if action == "basic":
                args = ["title", "description", "input", "output", "sample_input", "sample_output", "hint", "source", "visible", 'verdict_id', 'verdict_code[file]', 'verdict_execute_type_id', 'pdf', 'pdf_file[file]']
                meta = self.get_args(args)
                print('META: ', meta)
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
                meta['problem_id'] = id
                err, data = yield from Service.Execute.post_problem_execute(meta)
                if err: self.render(500, err)
                else: self.render()
            elif action == "rejudge":
                meta = {}
                meta['id'] = id
                err, res = yield from Service.Problem.post_rejudge_problem(meta)
                if err: self.render(500, err)
                else: self.render()
            elif action == 'tag':
                args = ['tag_id']
                meta = self.get_args(args)
                meta['problem_id'] = id
                err, res = yield from Service.Tags.post_problem_tag(meta)
                if err: self.render(500, err)
                else: self.render()
            else: self.render(404)
        else: self.render(403, 'Permission Denied')

    
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
            elif action == "tag":
                args = ['tag_id']
                meta = self.get_args(args)
                meta['problem_id'] = id
                err, res = yield from Service.Tags.delete_problem_tag(meta)
                if err: self.render(500, err)
                else: self.render()
            else: self.render(404)
