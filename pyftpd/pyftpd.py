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
import logging
import argparse
from datetime import datetime
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import yaml

def get_dir(dir_name):
    ''' If the default directory exists and it is writable, use it.
    Otherwise, use default directory /tmp
    '''
    if dir_name == None:
        return ""

    if dir_name[0:4] == "ENV:":
        env_string = dir_name.split(':')[1]
        try:
            dir_name = os.environ[env_string]
        except KeyError:
            dir_name = '.'
    
    if os.access(dir_name, os.W_OK) is True:
        _dir = dir_name
    else:
        _dir = '.'

    return _dir

class MyHandler(FTPHandler):
    """
    handler for ftp events
    """

    target_dir = None    # by default, do not move the received file

    def on_connect(self):
        logging.info("%s:%s connected", self.remote_ip, self.remote_port)

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

        logging.info("Receive %s", file)

        if self.target_dir != None:
            # 1. move file to somewhere with renaming
            cur_date = datetime.now()
            new_filename = "%s%s" %(cur_date.strftime("%Y%m%d_%H%M%S_%f"), file_extension)

        if self.target_dir != "" and filename.find("img-") == 0:
            try:
                shutil.move(file, "%s/%s" %(self.target_dir, new_filename))
                logging.info("Move to %s/%s", self.target_dir, new_filename)
            except FileNotFoundError:
                logging.error("Fail to move %s/%s", self.target_dir, new_filename)

            # 2. if the directory name starts with 'img-' and it is empty, delete it
            if dir_name.find("img-") == 0 and os.listdir(filepath) == []:
                os.rmdir(filepath)

    def on_incomplete_file_sent(self, file):
        # do something when a file is partially sent
        pass

    def on_incomplete_file_received(self, file):
        # remove partially uploaded files
        os.remove(file)


def open_logfile(log_dir):
    log_filename = '%s/pyftpd.log' %get_dir(log_dir)
    print("log dir  : %s" %log_filename)
    logging.basicConfig(filename=log_filename, level=logging.INFO)

    # print to console also
    stderrLogger=logging.StreamHandler()
    stderrLogger.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
    logging.getLogger().addHandler(stderrLogger)

def main():
    """
    main
    """

    parser = argparse.ArgumentParser("Simple ftp server")
    parser.add_argument('-c', action='store', dest='cfg_name', default="/etc/pyftpd.yaml", help="YAML filename")
    options = parser.parse_args()

    if not os.path.isfile(options.cfg_name):
        print("Error! Configuration file %s is not exit..." %options.cfg_name)
        sys.exit(0)

    stream = open(options.cfg_name, 'r')
    cfg = yaml.load(stream)
    ftp_cfg = cfg['server']
    
    open_logfile(ftp_cfg['log_dir'])
    logging.info("log dir  : %s" %ftp_cfg['log_dir'])

    home_dir = get_dir(ftp_cfg['incoming_dir'])
    logging.info("home dir : %s" %home_dir)

    authorizer = DummyAuthorizer()
    authorizer.add_user(ftp_cfg['username'], ftp_cfg['password'], home_dir, perm="elradfmw")

    #authorizer.add_anonymous("/home/nobody")

    handler = MyHandler # FTPHandler is the default handler
    handler.authorizer = authorizer
    handler.target_dir = get_dir(cfg['post-processing']['target_dir'])

    # enable for docker case
    handler.permit_foreign_addresses = True

    try:
        listening_port = os.environ["PYFTPD_PORT"]
        listening_port = eval(listening_port)
    except KeyError:
        listening_port = ftp_cfg['port_number']

    logging.info("Listening port : %d" %listening_port)
    print("Listening port : %d" %listening_port)

    try:
        passive_ports = os.environ["PYFTPD_PASSIVE_PORT"]
        print("Passive port   : %s" %passive_ports)
        p_ports = passive_ports.split('-')  
        if len(p_ports) == 2:
            handler.passive_ports = range(eval(p_ports[0]), eval(p_ports[1]))

        logging.info("Passive mode : %s" %passive_port)
    except:
        logging.info("Active mode")
        pass

    server = FTPServer((ftp_cfg['ip_address'], listening_port), handler)
    server.serve_forever()

if __name__ == "__main__":
    main()
