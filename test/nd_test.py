# coding: utf-8
"""
nd_test.py
"""
import os, sys

from src.idls.nd_idl.nsfw_detection.ttypes import Request
from src.util.util import ndlogger

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
import base64
import requests
from PIL import Image
from io import BytesIO
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
    enum RequestType {
        NSFW_DETECT,
        DETECT_DEBUG
    }
    
    enum FileType {
        VIDEO,
        IMAGE,
        AUDIO,
        TEXT
    }
    
    struct Request {
        1: required RequestType         req_type;
        2: required FileType            file_type;
        3: required list<string>        file_urls;
        4: optional map<string, string> detect_params;
    }
    '''

    file_urls = []
    file_urls.append('http://bpic.588ku.com/element_origin_min_pic/19/03/15/75076c485081d15ed9c224ad3e4ce4a1.jpg')
    file_urls.append('https://cdn.pornpics.com/pics/2017-01-10/253759_12big.jpg')

    detect_params = {}
    detect_params['debug'] = "1"

    '''

    response = requests.get(file_urls[0])
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

    # 构造得到请求体xxx
    # req = {'inputs': data.tolist()}
    # req = data.tolist()
    '''

    req = Request(0, 1, file_urls, detect_params)

    # 执行request
    result = client.doNsfwDetect(req)

    ndlogger.info("Sp return")
    ndlogger.info(result)

    transport.close()

except Thrift.TException as ex:
    print("%s" % (ex.message))