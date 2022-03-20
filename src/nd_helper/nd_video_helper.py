# coding: utf-8
import os, sys
from math import floor

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
from moviepy.editor import *


# detect调用docker
class NDVideoHelper:
    def __init__(self, conf, req, reInit=False):
        self._ip = conf["services"]["nd"]["ip"]
        self._port = conf["services"]["nd"]["port"]
        self._nd_req = req
        self._init_ok = True

    def One_Predict(self):
        # 返回结果
        detect_result = []

        sampling_density = 2

        video_path = self._nd_req.file_urls[0].replace('file://', '')
        clip = VideoFileClip(video_path)
        duration = int(clip.duration)

        safe = list()
        unsafe = list()

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

            # img_list = list()

            for i in range(duration):
                if i % sampling_density == 0:
                    # screenshot video by time
                    frame = clip.get_frame(i)

                    # convert screenshpot to PIL format and resize
                    img = tf.keras.preprocessing.image.array_to_img(frame)

                    newsize = (299, 299)
                    img = img.resize(newsize)
                    img_array = keras.preprocessing.image.img_to_array(img)
                    img_array /= 255
                    img_array = tf.expand_dims(img_array, 0)  # Create a batch

                    url = 'http://localhost:8501/v1/models/yellow_pic:predict'
                    data = img_array.numpy()
                    # img_list.append(data.tolist())
                    # img_list.append(img_array)
                    # data = np.random.random((1, 299, 299, 3))

                    # params = {'inputs': data.tolist()}

                    # img_list = np.concatenate([x for x in img_list])  # 传多张

                    # params = {'inputs': img_list}
                    params = {'inputs': data.tolist()}
                    t = time.time()

                    requests.adapters.DEFAULT_RETRIES = 5
                    s = requests.session()
                    s.keep_alive = False
                    res = s.post(url, json=params)
                    result = res.json()
                    s.close()

                    predictions = np.array(result['outputs'])
                    ndlogger.warning("predictions: {}".format(result))
                    y_pred = np.argmax(predictions, axis=1)
                    ndlogger.warning("y_pred: {}".format(y_pred))

                    if y_pred == 0:
                        safe.append(i)
                    else:
                        unsafe.append(i)

            safe_roportion = round(len(safe) / floor(clip.duration / sampling_density), 2)
            detect_result = [safe_roportion]
            if safe_roportion < 0.98:
                ndlogger.warning("NSFW!!!NSFW!!!NSFW!!!NSFW!!!NSFW!!!NSFW!!!")


        except Thrift.TException as ex:
            ndlogger.info("{}".format(ex.message))

        return detect_result
