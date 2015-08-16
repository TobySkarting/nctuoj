from service.base import BaseService
import os
import config

class SubmissionService(BaseService):
    def __init__(self, db, rs):
        super().__init__(db, rs)
        SubmissionService.inst = self
    
    def get_submission_list(self, data):
        required_args = ['page', 'count']
        err = self.check_required_args(required_args, data)
        if err: return (err, None)
        ### if exist data['problem_id']
        ### else exist data['group_id']

    def get_submission_list_count(self, data):
        ### if exist data['problem_id']
        ### else exist data['group_id']
        if 'problem_id' in data and data['problem_id']:
            pass
        elif 'group_id' in data and data['group_id']:
            res = self.rs.get('submission_list_count@%s' % (str(data['group_id'])))

