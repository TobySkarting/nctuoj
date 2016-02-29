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
    urls = '%s/api/groups/1/bulletins/'%(config.base_url)
    another_url = '%s/api/groups/2/bulletins/'%(config.base_url)
    another_urls = '%s/api/groups/2/bulletins/'%(config.base_url)
    admin_token = common.get_user_info({'account': config.user_admin_account, 'passwd': config.user_admin_password})['token']
    title = "Title test @ " + str(datetime.datetime.now())
    content = "Content tes @ " + str(datetime.datetime.now())

    def test_admin_get_bulletins(self):
        data = {
            "token": self.admin_token,
        }
        res = requests.get(self.urls, data=data)
        res.connection.close()
        self.assertEqual(res.status_code, 200)

    def test_admin_post_bulletin(self):
        # missing title
        data = {
            "token": self.admin_token,
            "content": self.content,
        }
        expect_result = {
            "status_code": 400,
            "body": {
                "msg": 'value of title: "None" should not be empty value',
            }
        }
        res = requests.post(self.urls, data=data)
        res.connection.close()
        self.assertEqualR(res, expect_result)

        # missing content
        data = {
            "token": self.admin_token,
            "title": self.title,
        }
        res = requests.post(self.urls, data=data)
        res.connection.close()
        expect_result = {
            "status_code": 400,
            "body": {
                "msg": 'value of content: "None" should not be empty value',
            }
        }
        self.assertEqualR(res, expect_result)

        # success post
        data = {
            "token": self.admin_token,
            "title": self.title,
            "content": self.content,
        }
        res = requests.post(self.urls, data=data)
        res.connection.close()
        self.assertEqual(res.status_code, 200)

    def test_admin_put_bulletin(self):
        data = {
            "token": self.admin_token,
        }
        res = requests.get(self.urls, data=data)
        res.connection.close()
        res = json.loads(res.text)['msg'][0]
        data = {
            "token": self.admin_token,
            "title": res['title'],
            "content": "Modify @ " + str(datetime.datetime.now()) + res['content'],
        }
        res =requests.put( '%s%s/'%(self.url, res['id']), data=data)
        res.connection.close()
        expect_result = {
            "status_code": 200,
            "body": {
                "msg": "",
            }
        }
        self.assertEqualR(res, expect_result)

    def test_admin_delete_bulletin(self):
        pass
    def test_admin_post_another_bulletin(self):
        pass
    def test_admin_put_another_bulletin(self):
        pass
    def test_admin_delete_another_bulletin(self):
        pass
