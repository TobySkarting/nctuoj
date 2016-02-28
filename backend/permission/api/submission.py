from permission.base import PermissionBase
from req import Service
from map import *

class ApiSubmissionsPermission(PermissionBase):
    def get(req, data):
        return None

    def post(req, data):
        err, res = yield from Service.Problem.get_problem({'id': data['problem_id']})
        if err: return err
        if not (req.current_group == res['problem_group_id'] and \
                (map_group_power['submission_manage'] in req.current_group_power or res['visible'] > 0)):
            return (403, 'Permission Denied')
        if req.current_contest:
            err, contest_problem_list = yield from Service.Contest.get_contest_problem_list(req.current_contest)
            if err: return err
            if int(res['id']) not in contest_problem_list:
                return (403, 'You are in contest now')
        return None
    
class ApiSubmissionPermission(PermissionBase):
    def get(req, data):
        err, res = yield from Service.Submission.get_submission({'id': data['id']})
        if err: return err
        if res['problem_group_id'] != req.current_group:
            return (403, 'Permission Denied')
        return None


class ApiSubmissionRejudgePermission(PermissionBase):
    def post(req, data):
        err, res = yield from Service.Submission.get_submission({'id': data['id']})
        if err: return err
        if not (res['problem_group_id'] == req.current_group and \
                map_group_power['submission_manage'] in req.current_group_power):
            return (403, 'Permision Denied')
        return None
