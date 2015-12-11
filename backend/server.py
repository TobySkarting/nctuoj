### tornado 
import tornado.ioloop
import tornado.httpserver
import tornado.web
### self define from req import RequestHandler
from req import Service 
### my app
import config
import mysql
import myredis

### built-in module
import time
import signal
import logging
import momoko
import psycopg2.extras

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
from api.submission     import ApiSubmissionsHandler
from api.submission     import ApiSubmissionHandler
from api.testdata       import ApiTestdataHandler
from api.contest        import ApiContestsHandler
from api.contest        import ApiContestHandler
from api.contest        import ApiContestProblemsHandler
from api.contest        import ApiContestSubmissionsHandler
#from api.contest        import ApiContestSubmissionHandler
from api.contest        import ApiContestScoreboardHandler
from api.execute        import ApiExecuteTypesHandler
from api.execute        import ApiExecuteTypeHandler
from api.verdict        import ApiVerdictTypesHandler
from api.verdict        import ApiVerdictTypeHandler
from api.group          import ApiGroupHandler
from api.group          import ApiGroupUserHandler
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
#from web.problem import WebProblemHandler
#from web.problem import WebProblemListHandler





def sig_handler(sig, frame):
    print('Catch Stop Signal')
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)

def shutdown():
    print('Server Stopping')
    srv.stop()
    io_loop = tornado.ioloop.IOLoop.instance()
    deadline = time.time() + config.MAX_WAIT_SECOND_BEFORE_SHUTDOWN

    def stop_loop():
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()
            print('Server Stopped')
    stop_loop()


if __name__ == '__main__':
    print('Server Starting')
    '''
    logging.basicConfig(level=logging.DEBUG,
            format='[%(asctime)s]: %(message)s',
            datefmt='%a, %d %b %Y %H:%M:%S',
            filename=config.LOG_FILE_PATH,
            filemode='a')
    '''
    db = momoko.Pool(
            dsn = 'dbname=%s user=%s password=%s host=%s port=%s'%(config.DBNAME, config.DBUSER, config.DBPASSWORD, config.DBHOST, config.DBPORT),
            size = config.DBMIN_SIZE,
            max_size = config.DBMAX_SIZE,
            ioloop = tornado.ioloop.IOLoop.instance(),
            setsession = ("SET TIME ZONE +8",),
            raise_connect_errors=False,
            cursor_factory = psycopg2.extras.RealDictCursor 
            )
    future = db.connect()
    tornado.ioloop.IOLoop.instance().add_future(future, lambda f: tornado.ioloop.IOLoop.instance().stop())
    tornado.ioloop.IOLoop.instance().start()
    rs = myredis.MyRedis(db=1)
    rs.flushdb()
    ui_modules = {
            "Pagination": web.modules.Pagination,
            }
    app = tornado.web.Application([
        ('/',                                                           WebIndexHandler),
        ('/api/users/',                                                 ApiUsersHandler),
        ('/api/users/(\d+)/',                                           ApiUserHandler),
        ('/api/users/(\d+)/groups/(\d+)/(problems)/',                    ApiUserGroupHandler),
        ('/api/users/(sign\w*)/',                                       ApiUserSignHandler),
        ('/api/users/(resettoken)/',                                    ApiUserSignHandler),
        
        ('/api/groups/\d+/',                                             ApiGroupHandler),
        ('/api/groups/\d+/(\d+)/',                                       ApiGroupUserHandler),
        ('/api/groups/\d+/bulletins/',                                   ApiBulletinsHandler),
        ('/api/groups/\d+/bulletins/(\d+)/',                             ApiBulletinHandler),

        ('/api/groups/\d+/problems/',                                    ApiProblemsHandler),
        ('/api/groups/\d+/problems/(\d+)/',                              ApiProblemHandler),
        ('/api/groups/\d+/problems/(\d+)/(\w*)/',                        ApiProblemHandler),
        ### /api/groups/\d+/problems/(\d+)/(\w*)/
        ### /api/groups/\d+/problems/(\d+)/(execute)/
        ### /api/groups/\d+/problems/(\d+)/(tag)/
        ### /api/groups/\d+/problems/(\d+)/(testdata)/
        ('/api/groups/\d+/problems/(\d+)/(\w*)/(\d+)/',                  ApiProblemHandler),
        ### /api/groups/\d+/problems/(\d+)/(testdata)/(\d+)/'
        ('/api/groups/\d+/testdata/(\d+)/',                              ApiTestdataHandler),
        ('/api/groups/\d+/submissions/',                                 ApiSubmissionsHandler),
        ('/api/groups/\d+/submissions/(\d+)/',                           ApiSubmissionHandler),
        ('/api/groups/\d+/submissions/(\d+)/(\w*)/',                     ApiSubmissionHandler),

        ('/api/groups/\d+/contests/',                                    ApiContestsHandler),
        ### TODO
        ('/api/groups/\d+/contests/(\d+)/',                              ApiContestHandler),
        ('/api/groups/\d+/contests/(\d+)/problems/',                     ApiContestProblemsHandler),
        ('/api/groups/\d+/contests/(\d+)/submissions/',                  ApiContestSubmissionsHandler),
        ('/api/groups/\d+/contests/(\d+)/scoreboard/',                   ApiContestScoreboardHandler),
        ('/api/groups/\d+/contests/(\d+)/(\w+)/',                        ApiContestHandler),
        ('/api/time/',                                                  ApiTimeHandler),

        ('/api/executes/',                                              ApiExecuteTypesHandler),
        ('/api/executes/priority/',                                     ApiExecuteTypesHandler),
        ('/api/executes/(\d+)/',                                        ApiExecuteTypeHandler),
        ('/api/verdicts/',                                              ApiVerdictTypesHandler),
        ('/api/verdicts/(\d+)/',                                        ApiVerdictTypeHandler),
        ('/api/tags/',                                                  ApiTagsHandler),
        ('/api/tags/(\d+)/',                                            ApiTagHandler),

        ('/groups/',                                                    WebGroupsHandler),

        ('/groups/(\d+)/',                                               WebGroupHandler),
        ('/groups/(\d+)/manage/(\w*/)?',                                 WebGroupManageHandler),
        ('/groups/\d+/bulletins/',                                       WebBulletinsHandler),
        ('/groups/\d+/bulletins/(\d+)/(\w*)/',                           WebBulletinHandler),

        ('/groups/\d+/problems/',                                        WebProblemsHandler),
        ('/groups/\d+/problems/(\d+)/',                                  WebProblemHandler),
        ('/groups/\d+/problems/(\d+)/(\w*)/',                            WebProblemHandler),
        ('/groups/\d+/problems/(\d+)/(\w*)/edit/',                       WebProblemEditHandler),
        ### /groups/\d+/problems/\d+/basic/edit/
        ### /groups/\d+/problems/\d+/tag/edit/
        ### /groups/\d+/problems/\d+/execute/edit/
        ### /groups/\d+/problems/\d+/testdata/edit/
        ### /groups/\d+/problems/\d+/submit/

        ('/groups/\d+/submissions/',                                     WebSubmissionsHandler),
        ('/groups/\d+/submissions/(\d+)/',                               WebSubmissionHandler),

        ('/groups/\d+/contests/',                                        WebContestsHandler),
        ('/groups/\d+/contests/(\d+)/',                                  WebContestHandler),
        ### TODO
        ('/groups/\d+/contests/(\d+)/edit/',                             WebContestEditHandler),
        ('/groups/\d+/contests/(\d+)/problems/(\d+)/',                   WebContestProblemHandler),
        ('/groups/\d+/contests/(\d+)/problems/(\d+)/(\w*)/',             WebContestProblemHandler),
        ('/groups/\d+/contests/(\d+)/submissions/',                      WebContestSubmissionsHandler),
        ('/groups/\d+/contests/(\d+)/submissions/(\d+)/',                WebContestSubmissionHandler),
        ('/groups/\d+/contests/(\d+)/scoreboard/',                       WebContestScoreboardHandler),

        #('/groups/\d+/contests/(\d+)/rank/',                             WebContestRankHandler),


        
        ('/executes/',                                                  WebExecuteTypesHandler),
        ('/executes/(\d+)/',                                            WebExecuteTypeHandler),
        ('/executes/(\d+)/(\w*)/',                                      WebExecuteTypeHandler),
        ('/verdicts/',                                                  WebVerdictTypesHandler),
        ('/verdicts/(\d+)/',                                            WebVerdictTypeHandler),
        ('/verdicts/(\d+)/(\w*)/',                                      WebVerdictTypeHandler),

        ### user list only admin
        ('/users/',                                                     WebUsersHandler),       
        ('/users/(\d+)/',                                               WebUserHandler),
        ('/users/(sign\w*)/?',                                          WebUserSignHandler),
        ('/users/(\d+)/(\w*)/?',                                        WebUserHandler),


        ('/about/',                                                     WebAboutHandler),
        ('/asset/(.*)', tornado.web.StaticFileHandler, {'path': '../http'}),
        ('/(google4e9e359eaf9accab.html)', tornado.web.StaticFileHandler, {'path': '../http'}),
        ('/.*',                                                         Web404Handler),
        ],  cookie_secret = config.COOKIE_SECRET, 
            compress_response = True,
            debug = config.DEBUG,
            autoescape =    'xhtml_escape', 
            ui_modules =    ui_modules,
            xheaders=True,)
    global srv
    srv = tornado.httpserver.HTTPServer(app)
    srv.listen(config.PORT)
    Service.User =          UserService(db, rs)
    Service.Problem =       ProblemService(db, rs)
    Service.Submission =    SubmissionService(db, rs)
    Service.Testdata =      TestdataSerivce(db, rs)
    Service.Bulletin =      BulletinService(db, rs)
    Service.Execute =       ExecuteService(db, rs)
    Service.Contest =       ContestService(db, rs)
    Service.Verdict =       VerdictService(db, rs)
    Service.Group =         GroupService(db, rs)
    Service.Tags =          TagService(db, rs)
    Service.School =        SchoolService(db, rs)
    Service.VerdictString = VerdictStringService(db, rs)
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    print('Server Started')
    tornado.ioloop.IOLoop().instance().start()
