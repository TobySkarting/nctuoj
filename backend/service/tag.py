from req import Service
from map import *
from service.base import BaseService

class TagService(BaseService):
    def __init__(self, db, rs, ftp):
        super().__init__(db, rs, ftp)

        TagService.inst = self

    def get_tag_list(self):
        pass

    def get_tag(self, data={}):
        pass

    def post_tag(self, data={}):
        pass

    def delete_tag(self, data={}):
        pass

