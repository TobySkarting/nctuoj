from req import Service
from service.base import BaseService
from map import *

class TestdataSerivce(BaseService):
    def __init__(self, db, rs, ftp):
        super().__init__(db, rs, ftp)
        TestdataSerivce.inst = self

    def get_testddata_list(self):
        pass

    def get_testddata(self, data={}):
        pass

    def post_testdata(self, data={}):
        pass

    def delete_testdata(self, data={}):
        pass

