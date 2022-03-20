# coding: utf-8

import sys, os, logging
cur_path = os.getcwd()
sys.path.append(cur_path+"/../")

ndlogger = logging.getLogger('search_plan')
ndlogger.setLevel(logging.DEBUG)
# 写入到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s-%(filename)s-%(lineno)d:    %(message)s')
ch.setFormatter(formatter)
ndlogger.addHandler(ch)

import datetime

import yaml

conf_file_path = '../conf/nd.yaml'
with open(conf_file_path) as nd_conf_file:
    if nd_conf_file:
        nd_conf = yaml.load(nd_conf_file.read())
        #splogger.info("Conf:")
        #splogger.info(sp_conf["services"]["qp"])
    else:
        ndlogger.fatal("Load conf {} error!".format(conf_file_path))
        sys.exit(-1)
