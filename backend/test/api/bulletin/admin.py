#!/usr/bin/env python3
import sys
import requests
import json
import unittest
import datetime
from util import TestCase
import config
import common

class TestApiBulletinAdmin(TestCase):
    url = '%s/api/groups/1/bulletins/'%(config.base_url)
    token = common.get_user_info({'account': config.user_admin_account, 'passwd': config.user_admin_password})['token']
    title = "Title test @ " + str(datetime.datetime.now())
    content = "Content test @ " + str(datetime.datetime.now())

    def test_get(self):
        data = {
            "token": self.token,
        }
        res = requests.get("%s%s/"%(self.url,1), data=data)
        res.connection.close()
        self.assertEqual(res.status_code, 200)

        ### outbound
        data = {
            "token": self.token,
        }
        res = requests.get("%s%s/"%(self.url,2), data=data)
        res.connection.close()

    def test_gets(self):
        data = {
            "token": self.token,
        }
        res = requests.get(self.url, data=data)
        res.connection.close()
        self.assertEqual(res.status_code, 200)

    def test_edit(self):
        # missing title
        data = {
            "token": self.token,
            "content": self.content,
        }
        expect_result = {
            "status_code": 400,
            "body": {
                "msg": 'title not in form',
            }
        }
        res = requests.post(self.url, data=data)
        res.connection.close()
        self.assertEqualR(res, expect_result)

        # missing content
        data = {
            "token": self.token,
            "title": self.title,
        }
        res = requests.post(self.url, data=data)
        res.connection.close()
        expect_result = {
            "status_code": 400,
            "body": {
                "msg": 'content not in form',
            }
        }
        self.assertEqualR(res, expect_result)

        # success post
        data = {
            "token": self.token,
            "title": self.title,
            "content": self.content,
        }
        res = requests.post(self.url, data=data)
        res.connection.close()
        self.assertEqual(res.status_code, 200)
        id = json.loads(res.text)['msg']['id']

        ### put
        data = {
            "token": self.token,
            "title": self.title,
            "content": "Modify @ " + str(datetime.datetime.now()) + self.content,
        }
        res =requests.put( '%s%s/'%(self.url, id), data=data)
        res.connection.close()
        expect_result = {
            "status_code": 200,
            "body": {
                "msg": "",
            }
        }
        self.assertEqualR(res, expect_result)

        ### delete
        data = {
            "token": self.token,
        }
        res = requests.delete( '%s%s/'%(self.url, id), data=data)
        res.connection.close()
        expect_result = {
            "status_code": 200,
            "body": {
                "msg": "",
            }
        }
        self.assertEqualR(res, expect_result)
