### tornado 
import tornado.ioloop
import tornado.httpserver
import tornado.web
### self define from req import RequestHandler
from req import Service 
### my app
import config
import pg
import mysql
import myredis

### built-in module
import time
import signal
import logging

### service class
from service.user       import UserService
from service.problem    import ProblemService
from service.submission import SubmissionService
from service.bulletin   import BulletinService
from service.execute    import ExecuteService
from service.contest    import ContestService
from service.verdict    import VerdictService

### api class from api.user import ApiUserSignupHandler
from api.user           import ApiUserSignHandler
from api.user           import ApiUsersHandler
from api.user           import ApiUserHandler
from api.bulletin       import ApiBulletinsHandler
from api.bulletin       import ApiBulletinHandler
from api.problem        import ApiProblemsHandler
from api.problem        import ApiProblemHandler
from api.contest        import ApiContestsHandler
from api.contest        import ApiContestHandler
from api.contest        import ApiContestProblemsHandler
from api.contest        import ApiContestProblemHandler
from api.execute        import ApiExecutesHandler
from api.execute        import ApiExecuteHandler
from api.time           import ApiTimeHandler

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

from web.execute        import WebExecuteTypesHandler
from web.execute        import WebExecuteTypeHandler
from web.verdict        import WebVerdictTypesHandler
from web.verdict        import WebVerdictTypeHandler


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
    #db = mysql.AsyncMysql(user=config.DBUSER,
    #        database=config.DBNAME,
    #        passwd=config.DBPASSWORD,
    #        host=config.DBHOST)
    db = pg.AsyncPG(config.DBNAME, config.DBUSER, config.DBPASSWORD, host=config.DBHOST, dbtz='+8')
    rs = myredis.MyRedis(db=1)
    rs.flushdb()
    ui_modules = {
            "Pagination": web.modules.Pagination,
            }
    app = tornado.web.Application([
        ('/',                                                           WebIndexHandler),
        ('/api/users/',                                                 ApiUsersHandler),
        ('/api/user/(\d+)/',                                            ApiUserHandler),
        ('/api/user/(sign\w*)/',                                        ApiUserSignHandler),
        ('/api/user/(resettoken)/',                                     ApiUserSignHandler),
        
        ('/api/group/\d+/bulletins/',                                   ApiBulletinsHandler),
        ('/api/group/\d+/bulletins/(\d+)/',                             ApiBulletinHandler),

        ('/api/group/\d+/problems/',                                    ApiProblemsHandler),
        ('/api/group/\d+/problems/(\d+)/',                              ApiProblemHandler),
        ('/api/group/\d+/problems/(\d+)/(\w*)/',                        ApiProblemHandler),
        ### /api/group/\d+/problems/(\d+)/(\w*)/
        ### /api/group/\d+/problems/(\d+)/(execute)/
        ### /api/group/\d+/problems/(\d+)/(tag)/
        ### /api/group/\d+/problems/(\d+)/(testdata)/
        ('/api/group/\d+/problems/(\d+)/(\w*)/(\d+)/',                  ApiProblemHandler),
        ### /api/group/\d+/problems/(\d+)/(testdata)/(\d+)/'
        ('/api/group/\d+/contests/',                                    ApiContestsHandler),
        ('/api/group/\d+/contests/(\d+)/',                              ApiContestHandler),
        ('/api/group/\d+/contests/(\d+)/problems/',                     ApiContestProblemsHandler),
        ('/api/group/\d+/contests/(\d+)/problems/(\d+)/',               ApiContestProblemHandler),
        ('/api/time/',                                                  ApiTimeHandler),

        ('/api/executes/',                                              ApiExecutesHandler),
        ('/api/executes/(\d+)/',                                        ApiExecuteHandler),

        ('/group/\d+/bulletins/',                                       WebBulletinsHandler),
        ('/group/\d+/bulletins/(\d+)/(\w*)/?',                          WebBulletinHandler),

        ('/group/\d+/problems/',                                        WebProblemsHandler),
        ('/group/\d+/problems/(\d+)/',                                  WebProblemHandler),
        ('/group/\d+/problems/(\d+)/(\w*)/',                            WebProblemHandler),
        ('/group/\d+/problems/(\d+)/(\w*)/edit/',                       WebProblemEditHandler),
        ### /group/\d+/problems/\d+/basic/edit/
        ### /group/\d+/problems/\d+/tag/edit/
        ### /group/\d+/problems/\d+/execute/edit/
        ### /group/\d+/problems/\d+/testdata/edit/

        ('/group/\d+/submissions/',                                     WebSubmissionsHandler),
        ('/group/\d+/submissions/(\d+)/',                               WebSubmissionHandler),

        ('/group/\d+/contests/',                                        WebContestsHandler),
        ('/group/\d+/contests/(\d+)/',                                  WebContestHandler),
        ('/group/\d+/contests/(\d+)/(\w*)/',                            WebContestHandler),
        ('/group/\d+/contests/(\d+)/(\w*)/edit/',                       WebContestEditHandler),
        ### TODO ('/group/\d+/contests/(\d+)/problems/(\d+)/',                   WebContestProblemHandler),
        
        ('/executes/',                                                  WebExecuteTypesHandler),
        ('/executes/(\d+)/',                                            WebExecuteTypeHandler),
        ('/executes/(\d+)/(\w*)/',                                      WebExecuteTypeHandler),
        ('/verdicts/',                                                  WebVerdictTypesHandler),
        ('/verdicts/(\d+)/',                                            WebVerdictTypeHandler),
        ('/verdicts/(\d+)/(\w*)/',                                      WebVerdictTypeHandler),

        ### user list only admin
        ('/users/',                                                     WebUsersHandler),       
        ('/user/',                                                      WebUserHandler),
        ('/user/(sign\w*)/?',                                           WebUserSignHandler),
        ('/user/(\d+)/(\w*)/?',                                         WebUserHandler),


        ('/about/',                                                     WebAboutHandler),
        ('/asset/(.*)', tornado.web.StaticFileHandler, {'path': '../http'}),
        ('/.*',                                                         Web404Handler),
        ],  cookie_secret = config.COOKIE_SECRET, 
            autoescape =    'xhtml_escape', 
            ui_modules =    ui_modules)
    global srv
    srv = tornado.httpserver.HTTPServer(app)
    srv.listen(config.PORT)
    Service.User =          UserService(db, rs)
    Service.Problem =       ProblemService(db, rs)
    Service.Submission =    SubmissionService(db, rs)
    Service.Bulletin =      BulletinService(db, rs)
    Service.Execute =       ExecuteService(db, rs)
    Service.Contest =       ContestService(db, rs)
    Service.Verdict =       VerdictService(db, rs)
    print('Server Started')
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    tornado.ioloop.IOLoop().instance().start()
