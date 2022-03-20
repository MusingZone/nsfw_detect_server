# coding: utf-8

"""
file  : nd_server
desc  : 
author:
date  :
"""

#Thrift modules
from nd_idl.nsfw_detection import NsfwDetectService

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TCompactProtocol
from thrift.server import TServer

# my custom utility
from utils.util import *
from nd_handler.nd_handler import NsfwDetectServiceHandler


handler     = NsfwDetectServiceHandler()
processor   = NsfwDetectService.Processor(handler)
nd_ip       = nd_conf["services"]["nd"]["ip"]
nd_port     = nd_conf["services"]["nd"]["port"]
transport   = TSocket.TServerSocket(nd_ip, nd_port)
tfactory    = TTransport.TBufferedTransportFactory()
pfactory    = TCompactProtocol.TCompactProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

ndlogger.info("Starting NSFW Detect in ip \"{}\" and port {}".format(nd_ip, nd_port))

server.serve()

ndlogger.info("Done")

