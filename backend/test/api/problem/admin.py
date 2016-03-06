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

    def test_post_visible(self):
        data = {
            "token": self.token,
            "verdict_id": 1,
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

    def test_post_verdict(self):
        data = {
            "token": self.token,
            "visible": 0,
        }
        res = requests.post(self.urls, data=data)
        res.connection.close()
        expect_result = {
            "status_code": 400,
            "body": {
                "msg": "verdict_id not in form",
            }
        }
        self.assertEqualR(res, expect_result)

        ### out of range
        """
        data['verdict_id'] = 9999
        res = requests.post(self.urls, data=data)
        res.connection.close()
        expect_result = {
            "status_code": 400,
            "body": {
                "msg": "",
            }
        }
        self.assertEqualR(res, expect_result)
        """


    def test_admin_post_put_delete_problem(self):
        data = {
            "token": self.token,
            "visible": 0,
            "verdict_id": 1,
        }
        res = requests.post(self.urls, data=data)
        res.connection.close()
        self.assertEqual(res.status_code, 200)
        id = json.loads(res.text)['msg']['id']

        modify_url = '%s%s/'%(self.url, id)
        data['title'] = 'modify ' + str(datetime.datetime.now())
        res = requests.put(modify_url, data=data)
        res.connection.close()

        expect_result = {
            "status_code": 200,
            "body": {
                "msg": {
                    "id": id,
                }
            }
        }
        self.assertEqualR(res, expect_result)

        data = {
            "token": self.token,
        }
        res = requests.delete(modify_url, data=data)
        res.connection.close()
        expect_result = {
            "status_code": 200,
            "body": {
                "msg": ""
            }
        }
        self.assertEqualR(res, expect_result)


