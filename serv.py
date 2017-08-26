#!/usr/bin/env python
"""
Usage::
    ./serv.py [<port>]

Send a GET request::
    curl http://localhost:port

Send a HEAD request::
    curl -I http://localhost:port

Send a POST request::
    curl -d "user=bar&ip=baz" http://localhost:port

"""


import cgi, cgitb, mimetypes, os, urlparse, json

from sys import version as python_version
from cgi import parse_header, parse_multipart
from mimetypes import guess_type
from io import open


if python_version.startswith('3'):
    from urllib.parse import parse_qs
    from http.server import BaseHTTPRequestHandler
else:
    from urlparse import parse_qs
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer


import SocketServer

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    # Modified version of this
    # https://stackoverflow.com/a/44599922
    def append_to_json(self, _dict,path):
        ## b added otherwise else f.seek(-1, 2) wouldn't work
        with open(path, 'ab+') as f:
            f.seek(0,2)              #Go to the end of file
            if f.tell() == 0 :       #Check if file is empty
                # write unicode added
                f.write(unicode(json.dumps([_dict], ensure_ascii=False)))  #If empty, write an array
            else:
                f.seek(-1,2)
                f.truncate()           #Remove the last character, open the array
                f.write(",\n")         #Write the separator
                json.dump(_dict,f)     #Dump the dictionary
                f.write(']')           #Close the array
                
    # From this post 
    # https://stackoverflow.com/a/21398402
    def do_GET(self):
        try:
            if self.path in ("", "/"):
                filepath = "html/index.html"
            else:
                filepath = self.path.lstrip("/")

            f = open(os.path.join('.', filepath), "rb")

        except IOError:
            self.send_error(404,'File Not Found: %s ' % filepath)

        else:
            self.send_response(200)

            #this part handles the mimetypes for you.
            mimetype, _ = mimetypes.guess_type(filepath)
            self.send_header('Content-type', mimetype)
            self.end_headers()
            for s in f:
                self.wfile.write(s)

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        # Reading header of the page and post variables
        # https://stackoverflow.com/a/13330449
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if ctype == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers.getheader('content-length'))
            postvars = urlparse.parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}

        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        # print(postvars) # Debuggining print
        
        # Creating file info.txt
        try:
            fileName = "./data/info.txt"
            myFile = os.path.isfile(fileName)
            ### Can be changed to what ever you want
            entry = {'user': postvars.get("user", "noUser")[0], 'ip': postvars.get("ip","noIP")[0]}
            if not myFile:
                raise # Exception will be raised
        except:
            # doesn't exist
            self.append_to_json(entry, fileName)

        else:
            # exists
            self.append_to_json(entry, fileName)


def run(server_class=HTTPServer, handler_class=S, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd... http://localhost:' + str(port)
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
