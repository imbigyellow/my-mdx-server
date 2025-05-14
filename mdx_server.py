# -*- coding: utf-8 -*-
# version: python 3.5+

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

try:
    base_path = os.path.dirname(sys.executable)
except Exception:
    base_path = os.path.abspath(".")

resource_path = os.path.join(base_path, 'mdx')
print("Resource path:", resource_path)

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
    print("Request path:", path_info)
    m = re.match('/(.*)', path_info)
    word = m.groups()[0] if m else ''

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
    mdx_file = 'data/longman6.mdx'
    if not os.path.exists(mdx_file):
        print(f"Cannot find mdx file: {mdx_file}")
        sys.exit(1)

    builder = IndexBuilder(mdx_file)

    t = threading.Thread(target=loop)
    t.start()
