#!/usr/bin/env python3
import sys
import requests
import json
import unittest
import datetime
from util import TestCase
import config
import common

class TestApiProblemUser(TestCase):
    url = '%s/api/groups/2/problems/'%(config.base_url)
    urls = '%s/api/groups/2/problems/'%(config.base_url)
    token = common.get_user_info({'account': config.user_admin_account, 'passwd': config.user_admin_password})['token']

    def test_admin_get_problems(self):
        data = {
            "token": self.token,
        }
        res = requests.get(self.urls, data=data)
        res.connection.close()
        self.assertEqual(res.status_code, 200)

    def test_admin_get_visible_problem(self):
        data = {
            "token": self.token,
        }
        res = requests.get("%s%s/"%(self.url,10004), data=data)
        res.connection.close()
        self.assertEqual(res.status_code, 200)

    def test_admin_get_invisible_problem(self):
        data = {
            "token": self.token,
        }
        res = requests.get("%s%s/"%(self.url,10003), data=data)
        res.connection.close()
        expect_result = {
            "status_code": 403,
            "body": {
                "msg": "Permission Denied",
            }
        }
        self.assertEqualR(res, expect_result)

