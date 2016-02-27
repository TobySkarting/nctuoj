import tornado
import types
### service class
from service.user       import UserService
from service.problem    import ProblemService
from service.submission import SubmissionService
from service.testdata   import TestdataSerivce
from service.bulletin   import BulletinService
from service.execute    import ExecuteService
from service.contest    import ContestService
from service.verdict    import VerdictService
from service.group      import GroupService
from service.tag        import TagService
from service.school     import SchoolService
from service.verdictstring import VerdictStringService


### api class from api.user import ApiUserSignupHandler
from api.user           import ApiUserSignHandler
from api.user           import ApiUsersHandler
from api.user           import ApiUserHandler
from api.user           import ApiUserGroupHandler
from api.bulletin       import ApiBulletinsHandler
from api.bulletin       import ApiBulletinHandler
from api.problem        import ApiProblemsHandler
from api.problem        import ApiProblemHandler
from api.problem        import ApiProblemExecuteHandler
from api.problem        import ApiProblemRejudgeHandler
from api.problem        import ApiProblemTagHandler
from api.submission     import ApiSubmissionsHandler
from api.submission     import ApiSubmissionHandler
from api.testdata       import ApiTestdatasHandler
from api.testdata       import ApiTestdataHandler
from api.contest        import ApiContestsHandler
from api.contest        import ApiContestHandler
from api.contest        import ApiContestProblemsHandler
from api.contest        import ApiContestSubmissionsHandler
#from api.contest        import ApiContestSubmissionHandler
from api.contest        import ApiContestScoreboardHandler
from api.execute        import ApiExecuteTypesHandler
from api.execute        import ApiExecuteTypesPriorityHandler
from api.execute        import ApiExecuteTypeHandler
from api.verdict        import ApiVerdictTypesHandler
from api.verdict        import ApiVerdictTypeHandler
from api.group          import ApiGroupHandler
from api.group          import ApiGroupsHandler
from api.group          import ApiGroupUserHandler
from api.group          import ApiGroupUserPowerHandler
from api.time           import ApiTimeHandler
from api.tag            import ApiTagsHandler
from api.tag            import ApiTagHandler

#from api.execute_type import ApiExecuteTypesHandler
#from api.execute_type import ApiExecuteTypeHandler


### web class
import web.modules

from web.err            import Web404Handler
from web.index          import WebIndexHandler
from web.bulletin       import WebBulletinsHandler
from web.bulletin       import WebBulletinHandler

from web.problem        import WebProblemsHandler
from web.problem        import WebProblemHandler
from web.problem        import WebProblemEditHandler

from web.submission     import WebSubmissionsHandler
from web.submission     import WebSubmissionHandler
from web.contest        import WebContestsHandler
from web.contest        import WebContestHandler
from web.contest        import WebContestEditHandler
from web.contest        import WebContestProblemHandler
from web.contest        import WebContestSubmissionsHandler
from web.contest        import WebContestSubmissionHandler
from web.contest        import WebContestScoreboardHandler

from web.execute        import WebExecuteTypesHandler
from web.execute        import WebExecuteTypeHandler
from web.verdict        import WebVerdictTypesHandler
from web.verdict        import WebVerdictTypeHandler

from web.group          import WebGroupHandler
from web.group          import WebGroupManageHandler
from web.group          import WebGroupsHandler

from web.about          import WebAboutHandler


#from web.execute_type import WebExecuteTypesHandler

from web.user           import WebUsersHandler
from web.user           import WebUserSignHandler
from web.user           import WebUserHandler
from web.user           import WebUserEditHandler
#from web.problem import WebProblemHandler
#from web.problem import WebProblemListHandler

### static file handler
from file.testdata import FileTestdataHandler

from permission.api.bulletin import ApiBulletinsPermission
from permission.api.bulletin import ApiBulletinPermission
from permission.api.problem import ApiProblemsPermission
from permission.api.problem import ApiProblemPermission
from permission.api.problem import ApiProblemExecutePermission
from permission.api.problem import ApiProblemTagPermission
from permission.api.problem import ApiProblemRejudgePermission
from permission.api.submission import ApiSubmissionsPermission
from permission.api.submission import ApiSubmissionRejudgePermission


class PermissionService:
    def check(req, data={}, **kwargs):
        data.update(kwargs)
        res = None
        if isinstance(req, ApiBulletinsHandler):
            res = ApiBulletinsPermission.check(req, data) 
        elif isinstance(req, ApiBulletinHandler):
            res = ApiBulletinPermission.check(req, data)
        elif isinstance(req, ApiProblemsHandler):
            res = ApiProblemsPermission.check(req, data)
        elif isinstance(req, ApiProblemHandler):
            res = ApiProblemPermission.check(req, data)
        elif isinstance(req, ApiProblemExecuteHandler):
            res = ApiProblemExecutePermission.check(req, data)
        elif isinstance(req, ApiProblemTagHandler):
            res = ApiProblemTagPermission.check(req, data)
        elif isinstance(req, ApiProblemRejudgeHandler):
            res = ApiProblemRejudgePermission.check(req, data)
        elif isinstance(req, ApiSubmissionsHandler):
            res = ApiSubmissionsPermission.check(req, data)
        elif isinstance(req, ApiSubmissionRejudgeHandler):
            res = ApiSubmissionRejudgePermission.check(req, data)
        print('type', type(res)) 
        if isinstance(res, types.GeneratorType):
            res = yield from res
        return res

