from permission.base import PermissionBase
from req import Service
from map import *

class ApiTestdatasPermission(PermissionBase):
    def post(req, data):
        err, problem = yield from Service.Problem.get_problem({'id': data['problem_id']})
        if err: return err
        if not (problem['group_id'] == req.current_group and \
                map_group_power['problem_manage'] in req.current_group_power):
            return (403, 'Permission Denied')
        return None

class ApiTestdataPermission(PermissionBase):
    def get(req, data):
        err, testdata = yield from Service.Testdata.get_testdata({'id': data['id']})
        if err: return err
        err, problem = yield from Service.Problem.get_problem({'id': testdata['problem_id']})
        if problem['group_id'] != req.current_group:
            return (403, 'Permission Denied')
        return None

    def edit(req, data):
        err, testdata = yield from Service.Testdata.get_testdata({'id': data['id']})
        if err: return err
        err, problem = yield from Service.Problem.get_problem({'id': testdata['problem_id']})
        if not (problem['group_id'] == req.current_group and \
                map_group_power['problem_manage'] in req.current_group_power):
            return (403, 'Permission Denied')
        return None

    def put(req, data):
        err = yield from ApiTestdataPermission.edit(req, data)
        if err: return err
        return None

    def delete(req, data):
        err = yield from ApiTestdataPermission.edit(req, data)
        if err: return err
        return None
