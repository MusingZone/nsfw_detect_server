# coding: utf-8
import os, sys

cur_path = os.getcwd()
sys.path.append(cur_path + "/../")

from util.util import *
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TCompactProtocol

from idls.nd_idl.nsfw_detection import NsfwDetectService
from idls.nd_idl.nsfw_detection.ttypes import *

import numpy as np
import time
import tensorflow as tf
from tensorflow import keras
import base64
import requests
from PIL import Image
from io import BytesIO
from tensorflow.keras.preprocessing.image import load_img


# detect调用docker
class NDHelper:
    def __init__(self, conf, req, reInit=False):
        self._ip = conf["services"]["qp"]["ip"]
        self._port = conf["services"]["qp"]["port"]
        self._nd_req = req
        self._init_ok = True

    def QP_Access(self):
        # 返回结果
        nd_result = SearchResult
        try:
            qptransport = TSocket.TSocket(self._ip, self._port)
            qptransport = TTransport.TBufferedTransport(qptransport)
            qpprotocol = TCompactProtocol.TCompactProtocol(qptransport)
            qpHelper = NsfwDetectService.Client(qpprotocol)
            qptransport.open()

            ndlogger.debug("Sp access qp");

            # RPC
            ndReq = Request(0, self._nd_req.file_type, self._nd_req.file_urls, self._nd_req.detect_params)

            '''Restful API
            response = requests.get(self._nd_req.file_urls[0])
            # 内存中打开图片
            image = Image.open(BytesIO(response.content))
            # 图片的base64编码
            ls_f = base64.b64encode(BytesIO(response.content).read())
            # base64编码解码
            imgdata = base64.b64decode(ls_f)
            # 图片文件保存
            file = open('test.jpg', 'wb')
            file.write(imgdata)
            file.close()
            img = load_img('test.jpg')
            newsize = (299, 299)
            img = img.resize(newsize)
            img_array = keras.preprocessing.image.img_to_array(img)
            img_array /= 255
            img_array = tf.expand_dims(img_array, 0)  # Create a batch
            data = img_array.numpy()

            ndReq = {'inputs': data.tolist()}
            '''

            # 调用NsfwDetectService中的doNsfwDetect方法，发送实际request体
            nd_result = qpHelper.doNsfwDetect(ndReq)
            ndlogger.debug("qp return")
            # splogger.debug(qpRslt)

            qptransport.close()

        except Thrift.TException as ex:
            ndlogger.info("{}".format(ex.message))

        return nd_result
