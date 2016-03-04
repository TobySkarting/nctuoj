#!/usr/bin/env python3
import sys
import requests
import json
import unittest
import datetime
from util import TestCase
import config
import common

class TestApiProblemAdmin(TestCase):
    url = '%s/api/groups/1/problems/'%(config.base_url)
    urls = '%s/api/groups/1/problems/'%(config.base_url)
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
        res = requests.get("%s%s/"%(self.url,10002), data=data)
        res.connection.close()
        self.assertEqual(res.status_code, 200)

    def test_admin_get_invisible_problem(self):
        data = {
            "token": self.token,
        }
        res = requests.get("%s%s/"%(self.url,10001), data=data)
        res.connection.close()
        self.assertEqual(res.status_code, 200)

    def test_admin_edit_problem(self):
        # post
        data = {
            "token": self.token,
        }
        res = requests.post(self.urls, data=data)
        res.connection.close()
        expect_result = {
            "status_code": 400,
            "body": {
                "msg": "visible not in form",
            }
        }
        self.assertEqualR(res, expect_result)
        # put
        # delete
        pass

