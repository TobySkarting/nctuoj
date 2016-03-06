#!/usr/bin/env python3
import sys
import requests
import json
import unittest
import datetime
from util import TestCase
import config
import common

class TestApiBulletinAdminCross(TestCase):
    url = '%s/api/groups/1/bulletins/'%(config.base_url)
    urls = '%s/api/groups/1/bulletins/'%(config.base_url)
    cross_url = None
    token = common.get_user_info({'account': config.user_admin_account, 'passwd': config.user_admin_password})['token']
    title = "Title test @ " + str(datetime.datetime.now())
    content = "Content test @ " + str(datetime.datetime.now())

    def get_cross_url(self):
        if self.cross_url is None:
            url = '%s/api/groups/2/bulletins/'%(config.base_url)
            data = {
                "token": self.token,
            }
            res = requests.get(url, data=data)
            res.connection.close()
            self.cross_url='%s/api/groups/1/bulletins/%s/'%(config.base_url, json.loads(res.text)['msg'][0]['id'])
        return self.cross_url

    def test_admin_cross_get_bulletin(self):
        data = {
            "token": self.token,
        }
        res = requests.get(self.get_cross_url(), data=data)
        res.connection.close()
        expect_result = {
            "status_code": 403,
            "body": {
                "msg": "Permission Denied",
            }
        }
        self.assertEqualR(res, expect_result)

    def test_admin_cross_put_bulletin(self):
        data = {
            "token": self.token,
            "title": self.title,
            "content": self.content,
        }
        res = requests.put(self.get_cross_url(), data=data)
        res.connection.close()
        expect_result = {
            "status_code": 403,
            "body": {
                "msg": "Permission Denied",
            }
        }
        self.assertEqualR(res, expect_result)

    def test_admin_cross_delete_bulletin(self):
        data = {
            "token": self.token,
        }
        res = requests.get(self.get_cross_url(), data=data)
        res.connection.close()
        expect_result = {
            "status_code": 403,
            "body": {
                "msg": "Permission Denied",
            }
        }
        self.assertEqualR(res, expect_result)
