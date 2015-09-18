from req import Service
from map import *

class TestdataSerivce:
    def __init__(self, db, rs, ftp):
        super().__init__(self, db, rs, ftp)
        TestdataSerivce.inst = self


