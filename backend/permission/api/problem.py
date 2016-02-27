from permission.base import PermissionBase
from req import Service
from map import *

class ApiProblemsPermission(PermissionBase):
    def post(req, data):
        if map_group_power['problem_manage'] not in req.current_group_power:
            return (403, 'Permission Denied')
        return None

class ApiProblemPermission(PermissionBase):
    def view(req, data):
        err, res = yield from Service.Problem.get_problem({'id': data['id']})
        if err: return err
        if not (res['group_id'] == req.current_group and \
                (res['visible'] > 0 or map_group_power['problem_manage'] in req.current_group_power)):
            return (403, 'Permission Denied')
        return None

    def edit(req, data):
        if map_group_power['problem_manage'] not in req.current_group_power:
            return ('403', 'Permission Denied')
        err, res = yield from Service.Problem.get_problem({'id': data['id']})
        if err: return err
        if res['group_id'] != req.current_group:
            return (403, 'Permission Denied')
        return None

    def get(req, data):
        err = yield from ApiProblemPermission.view(req, data)
        if err: return err
        return None

    def put(req, data):
        err = yield from ApiProblemPermission.edit(req, data)
        if err: return err
        return None

    def delete(req, data):
        err = yield from ApiProblemPermission.edit(req, data)
        if err: return err
        return None

class ApiProblemExecutePermission(PermissionBase):
    def get(req, data):
        err = yield from ApiProblemPermission.view(req, data)
        if err: return err
        return None

    def put(req, data):
        err = yield from ApiProblemPermission.edit(req, data)
        if err: return err
        return None

class ApiProblemTagPermission(PermissionBase):
    def get(req, data):
        err = yield from ApiProblemPermission.view(req, data)
        if err: return err
        return None

    def post(req, data):
        err = yield from ApiProblemPermission.edit(req, data)
        if err: return err
        return None

    def delete(req, data):
        err = yield from ApiProblemPermission.edit(req, data)
        if err: return err
        return None

class ApiProblemRejudgePermission(PermissionBase):
    def post(req, data):
        err = yield from ApiProblemPermission.edit(req, data)
        if err: return err
        return None
