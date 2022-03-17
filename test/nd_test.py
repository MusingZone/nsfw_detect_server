# coding: utf-8
"""
nd_test.py
"""
import os, sys
cur_path = os.getcwd()
sys.path.append(cur_path+"/../src")

from util.util import *

from idls.nd_idl.nsfw_detection import NsfwDetectService
from idls.nd_idl.nsfw_detection.ttypes import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TCompactProtocol

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.image import load_img


try:
    transport = TSocket.TSocket('42.192.54.30', 8501)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TCompactProtocol.TCompactProtocol(transport)

    # client实例化
    client = NsfwDetectService.Client(protocol)

    transport.open()
    ndlogger.info("Sp access");
    '''
    enum RequestType
    {
        IMAGE_SEARCH,
        SEARCH_DEBUG
    }
    struct Request
    {
        1: required RequestType type;
        2: required i32         comp_id;
        3: required i32         craft_id;
        4: required set < i32 > styles;
        5: required list < string > img_urls;
        6: optional map < string, string > srch_params;
    }
    '''
    styles = set([1,2])
    file_urls = []
    file_urls.append('D:/Workspace/鉴黄/image_search_app/test1.jpg')
    file_urls.append('D:/Workspace/鉴黄/image_search_app/test2.jpg')

    imgs = load_img('test.jpg')
    newsize = (299, 299)
    img = img.resize(newsize)
    img_array = keras.preprocessing.image.img_to_array(img)
    img_array /= 255
    img_array = tf.expand_dims(img_array, 0)  # Create a batch
    data = img_array.numpy()

    params = {}
    params['debug'] = "1"

    # 构造得到请求体
    req = Request(0, 1, file_urls, params)
    print("req: ", req)

    # 执行request
    result = client.doNsfwDetect(req)

    ndlogger.info("Sp return")
    ndlogger.info(result)

    transport.close()

except Thrift.TException as ex:
    print("%s" % (ex.message))