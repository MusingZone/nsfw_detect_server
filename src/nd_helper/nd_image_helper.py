# coding: utf-8
import os, sys

cur_path = os.getcwd()
sys.path.append(cur_path + "/../")

from utils.util import *
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TCompactProtocol

from nd_idl.nsfw_detection import NsfwDetectService
from nd_idl.nsfw_detection.ttypes import *

import numpy as np
import time
import tensorflow as tf
tf.enable_eager_execution()
from tensorflow import keras
import base64
import requests
from PIL import Image
from io import BytesIO
from tensorflow.keras.preprocessing.image import load_img


# detect调用docker
class NDImageHelper:
    def __init__(self, conf, req, reInit=False):
        self._ip = conf["services"]["nd"]["ip"]
        self._port = conf["services"]["nd"]["port"]
        self._nd_req = req
        self._init_ok = True

    def One_Predict(self):
        # 返回结果
        detect_result = []
        try:
            '''RPC
            qptransport = TSocket.TSocket(self._ip, self._port)
            qptransport = TTransport.TBufferedTransport(qptransport)
            qpprotocol = TCompactProtocol.TCompactProtocol(qptransport)
            qpHelper = NsfwDetectService.Client(qpprotocol)
            qptransport.open()

            ndlogger.debug("Sp access qp");

            # RPC
            ndReq = Request(0, self._nd_req.file_type, self._nd_req.file_urls, self._nd_req.detect_params)

            # 调用NsfwDetectService中的doNsfwDetect方法，发送实际request体
            nd_result = qpHelper.doNsfwDetect(ndReq)
            ndlogger.debug("qp return")
            # splogger.debug(qpRslt)

            qptransport.close()
            '''

            # Restful API
            img_path = self._nd_req.file_urls[0].replace('file://', '')
            img = load_img(img_path)
            newsize = (299, 299)
            img = img.resize(newsize)
            img_array = keras.preprocessing.image.img_to_array(img)
            img_array /= 255
            img_array = tf.expand_dims(img_array, 0)  # Create a batch

            url = 'http://localhost:8501/v1/models/yellow_pic:predict'
            data = img_array.numpy()
            # data = np.random.random((1, 299, 299, 3))

            params = {'inputs': data.tolist()}
            # params = {'inputs': data}
            t = time.time()
            res = requests.post(url, json=params)
            result = res.json()
            predictions = np.array(result['outputs'])
            ndlogger.warning("predictions: {}".format(predictions))
            y_pred = np.argmax(predictions, axis=1)
            ndlogger.warning("y_pred: {}".format(y_pred))

            detect_result = [item for sublist in predictions for item in sublist]


        except Thrift.TException as ex:
            ndlogger.info("{}".format(ex.message))

        return detect_result
