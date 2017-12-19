#!/usr/bin/env python3

"""
    To-do
        separate login and direcoty from the code with yaml file
        rename file with date and time for img-xxxx.pdf

"""

__version__ = "0.1"

import os
import sys
import shutil
import yaml
import logging
from optparse import OptionParser
from datetime import datetime
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def get_home_dir(home_dir):
    ''' if default hoem directory is exist and writable use it
    otherwise, fallback to somewhere
    '''
    if os.access(home_dir, os.W_OK) is True:
        _dir = home_dir
    else:
        _dir = '/tmp'

    logging.info("Use %s as home directory" %_dir)

    return _dir

class MyHandler(FTPHandler):

    doc_dir = ""    # by default, do not move the received file

    def on_connect(self):
        logging.info("%s:%s connected" % (self.remote_ip, self.remote_port))

    def on_disconnect(self):
        # do something when client disconnects
        pass

    def on_login(self, username):
        # do something when user login
        pass

    def on_logout(self, username):
        # do something when user logs out
        pass

    def on_file_sent(self, file):
        # do something when a file has been sent
        pass

    def on_file_received(self, file):
        # do something when a file has been received
        filepath = os.path.dirname(file)
        filename = os.path.basename(file)

        tmp = file.split('/')
        dir_name = tmp[len(tmp)-2]    # only the last directory name itself

        file_extension = os.path.splitext(filename)[1]

        tmp = file.split('/')


        logging.info("Receive %s" %file)

        # 1. move the file to somewhere with renaming
        dt = datetime.now()
        new_filename = "%s%s" %(dt.strftime("%Y%m%d_%H%M%S_%f"), file_extension)

        if self.doc_dir != "":
            try:
                shutil.move(file, "%s/%s" %(self.doc_dir, new_filename))
                logging.info("Move to %s/%s" %(self.doc_dir, new_filename))
            except FileNotFoundError:
                logging.error("Fail to move file %s/%s" %(self.doc_dir, new_filename))
                pass

            # 2. if the directory starts with 'img-' and it is empty, delete it
            if dir_name.find("img-") == 0 and os.listdir(filepath) == []:
                os.rmdir(filepath)

        pass

    def on_incomplete_file_sent(self, file):
        # do something when a file is partially sent
        pass

    def on_incomplete_file_received(self, file):
        # remove partially uploaded files
        import os
        os.remove(file)

def main():
    usage   = "Usage: %prog [options]"
    version = "%s" % __version__

    option_parser = OptionParser(usage=usage, version=version)
    option_parser.set_defaults(
        cfg_name="data.yaml"
    )

    option_parser.add_option("-c", "--cfg",
                             action="store", dest="cfg_name",
                             help="YAML filename"
    )

    (options, args) = option_parser.parse_args()

    if not os.path.isfile(options.cfg_name):
        print("Error! Configuration file %s is not exit..." %options.cfg_name)
        sys.exit(0)

    stream = open(options.cfg_name, 'r')
    cfg = yaml.load(stream)
    ftp_param = cfg['server']

    home_dir = get_home_dir(ftp_param['incoming_dir'])

    print("home dir : %s" %home_dir)

    authorizer = DummyAuthorizer()
    authorizer.add_user(ftp_param['username'], ftp_param['password'], home_dir, perm="elradfmw")

    #authorizer.add_anonymous("/home/nobody")

    handler = MyHandler # FTPHandler is the default handler
    handler.authorizer = authorizer
    handler.doc_dir = cfg['post-processing']['doc_dir']

    log_filename = '%s/pyftpd.log' %ftp_param['log_dir']
    print("log dir  : %s" %log_filename)
    logging.basicConfig(filename=log_filename, level=logging.INFO)

    server = FTPServer((ftp_param['ip_address'], ftp_param['port_number']), handler)
    server.serve_forever()

if __name__ == "__main__":
    main()
