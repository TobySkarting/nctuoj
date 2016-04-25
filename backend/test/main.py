#!/usr/bin/env python3
from api.user.signin import TestApiUserSignin
from api.user.signup import TestApiUserSignup
from api.bulletin.admin import TestApiBulletinAdmin
from api.bulletin.admin_cross import TestApiBulletinAdminCross
from api.bulletin.user import TestApiBulletinUser
from api.bulletin.guest import TestApiBulletinGuest
from api.problem.admin import TestApiProblemAdmin
from api.problem.user import TestApiProblemUser
from api.problem.guest import TestApiProblemGuest
from util import *
import unittest
if __name__ == '__main__':
    InitDB()
    unittest.main()
