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
    token = common.get_user_info({'account': config.user_admin_account, 'passwd': config.user_admin_password})['token']

    def test_gets(self):
        data = {
            "token": self.token,
        }
        res = requests.get(self.url, data=data)
        res.connection.close()
        self.assertEqual(res.status_code, 200)

    def test_get_visible(self):
        data = {
            "token": self.token,
        }
        res = requests.get("%s%s/"%(self.url,10004), data=data)
        res.connection.close()
        self.assertEqual(res.status_code, 200)

    def test_get_invisible(self):
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

    def test_post(self):
        data = {
            "token": self.token,
            "visible": 0,
            "verdict_id": 1,
        }
        res = requests.post(self.url, data=data)
        res.connection.close()
        expect_result = {
            "status_code": 403,
            "body": {
                "msg": "Permission Denied",
            }
        }
        self.assertEqualR(res, expect_result)

    def test_put(self):
        data = {
            "token": self.token,
            "visible": 0,
            "verdict_id": 1,
        }
        res = requests.put("%s%s/"%(self.url,10003), data=data)
        res.connection.close()
        expect_result = {
            "status_code": 403,
            "body": {
                "msg": "Permission Denied",
            }
        }
        print(res.status_code, res.text)
        self.assertEqualR(res, expect_result)

    def test_delete(self):
        data = {
            "token": self.token,
        }
        res = requests.delete("%s%s/"%(self.url,10003), data=data)
        res.connection.close()
        expect_result = {
            "status_code": 403,
            "body": {
                "msg": "Permission Denied"
            }
        }
        self.assertEqualR(res, expect_result)

