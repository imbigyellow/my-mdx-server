# -*- coding: utf-8 -*-
import threading
import re
import os
import sys

from wsgiref.simple_server import make_server
from file_util import *
from mdx_util import *
from mdict_query import IndexBuilder

"""
browser URL:
http://localhost:8000/test
"""

content_type_map = {
    'html': 'text/html; charset=utf-8',
    'js': 'application/x-javascript',
    'ico': 'image/x-icon',
    'css': 'text/css',
    'jpg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'mp3': 'audio/mpeg',
    'mp4': 'audio/mp4',
    'wav': 'audio/wav',
    'spx': 'audio/ogg',
    'ogg': 'audio/ogg',
    'eot': 'font/opentype',
    'svg': 'text/xml',
    'ttf': 'application/x-font-ttf',
    'woff': 'application/x-font-woff',
    'woff2': 'application/font-woff2',
}

resource_path = os.path.join(os.path.abspath("."), 'mdx')
print("resource path: " + resource_path)
builder = None

def get_url_map():
    result = {}
    files = []
    file_util_get_files(resource_path, files)
    for p in files:
        if file_util_get_ext(p) in content_type_map:
            p = p.replace('\\', '/')
            result[re.match('.*?/mdx(/.*)', p).groups()[0]] = p
    return result

def application(environ, start_response):
    path_info = environ['PATH_INFO'].encode('iso8859-1').decode('utf-8')
    print(path_info)
    m = re.match('/(.*)', path_info)
    word = ''
    if m is not None:
        word = m.groups()[0]

    url_map = get_url_map()

    if path_info in url_map:
        url_file = url_map[path_info]
        content_type = content_type_map.get(file_util_get_ext(url_file), 'text/html; charset=utf-8')
        start_response('200 OK', [('Content-Type', content_type)])
        return [file_util_read_byte(url_file)]
    elif file_util_get_ext(path_info) in content_type_map:
        content_type = content_type_map.get(file_util_get_ext(path_info), 'text/html; charset=utf-8')
        start_response('200 OK', [('Content-Type', content_type)])
        return get_definition_mdd(path_info, builder)
    else:
        start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
        return get_definition_mdx(path_info[1:], builder)

def loop():
    httpd = make_server('', 8000, application)
    print("Serving HTTP on port 8000...")
    httpd.serve_forever()

if __name__ == '__main__':
    # 直接用默认路径，不用tk选文件
    filename = os.path.join(os.path.abspath("./data"), "longman6.mdx")
    if not os.path.exists(filename):
        print("Dictionary file not found:", filename)
        sys.exit(1)

    builder = IndexBuilder(filename)
    t = threading.Thread(target=loop)
    t.start()
