from req import Service
from utils.form import form_validation
import hashlib
import time
import os
import config

class UploadService:
    def __init__(self, db, rs):
        self.db = db
        self.rs = rs
        UploadService.inst = self

    def gen_hash_filename(self, filename):
        hashed = hashlib.md5((filename+str(time.time())).encode()).hexdigest()
        filename = filename.split('.')
        ext = filename[-1] if len(filename) > 1 else ''
        ext = ext.lower()
        if ext == '': return (hashed, ext)
        else: return (hashed + '.' + ext, ext)

    def post_upload(self, data={}):
        required_args = [{
            'name': '+upload_file'
        }, {
            'name': '+group_id',
            'type': int,
        }]
        err = form_validation(data, required_args)
        if err: return (err, None)
        upload_file = data['upload_file']
        hashed_filename, ext = self.gen_hash_filename(upload_file['filename'])
        if ext not in config.ALLOW_EXT: return ((400, 'Extension not allowed'), None)
        folder = config.DATAROOT + '/data/resources/' + str(data['group_id']) + '/' 
        filepath = folder + hashed_filename
        try: os.makedirs(folder)
        except: pass
        with open(filepath, 'wb+') as f:
            f.write(upload_file['body'])
        return (None, hashed_filename)

