#!/usr/bin/env python3
import sys
import requests
import json
import unittest
import datetime
from util import TestCase
import config
import common

class TestApiBulletinGuest(TestCase):
    url = '%s/api/groups/3/bulletins/'%(config.base_url)
    urls = '%s/api/groups/3/bulletins/'%(config.base_url)
    token = common.get_user_info({'account': config.user_admin_account, 'passwd': config.user_admin_password})['token']
    title = "Title test @ " + str(datetime.datetime.now())
    content = "Content test @ " + str(datetime.datetime.now())

    def test_guest_get_bulletins(self):
        data = {
            "token": self.token,
        }
        res = requests.get(self.urls, data=data)
        res.connection.close()
        self.assertEqual(res.status_code, 200)

    def test_guest_post_bulletin(self):
        data = {
            "token": self.token,
            "title": self.title,
            "content": self.content,
        }
        res = requests.post(self.urls, data=data)
        res.connection.close()
        expect_result = {
            "status_code": 403,
            "body": {
                "msg": "Permission Denied",
            }
        }
        self.assertEqualR(res, expect_result)

    def test_guest_put_bulletin(self):
        data = {
            "token": self.token,
        }
        data = {
            "token": self.token,
            "title": self.title,
            "content": "Modify @ " + str(datetime.datetime.now()) + self.content,
        }
        res =requests.put( '%s%s/'%(self.url, 3), data=data)
        res.connection.close()
        expect_result = {
            "status_code": 403,
            "body": {
                "msg": "Permission Denied",
            }
        }
        self.assertEqualR(res, expect_result)

    def test_guest_delete_bulletin(self):
        data = {
            "token": self.token,
        }
        res = requests.delete( '%s%s/'%(self.url, 3), data=data)
        res.connection.close()
        expect_result = {
            "status_code": 403,
            "body": {
                "msg": "Permission Denied",
            }
        }
        self.assertEqualR(res, expect_result)
