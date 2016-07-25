import logging
import inspect
import datetime

def log(msg):
    (frame, filename, line_number, function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[1]
    print("[%s] [%s,%s,%s] %s"%(str(datetime.datetime.now())[:-7], filename, line_number, function_name, msg))

