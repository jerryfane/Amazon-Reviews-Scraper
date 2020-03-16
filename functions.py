import sys
import linecache
import time
from datetime import datetime
import pytz

def get_proxy_list(filename):
    with open(filename) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]

    proxy_list = content
    return proxy_list

def get_Chrome_proxy(optionsChrome, proxy):
    print('Proxy:', proxy)
    optionsChrome.add_argument('--proxy-server=socks4://' + proxy)
    return optionsChrome

def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    data = 'EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj)
    print(data)
    return str(data)
