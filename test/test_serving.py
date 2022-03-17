import os
import numpy as np
import time
import tensorflow as tf
from tensorflow import keras
import base64
import requests
from PIL import Image
from io import BytesIO
from tensorflow.keras.preprocessing.image import load_img
import json

# 正常图
response = requests.get("http://bpic.588ku.com/element_origin_min_pic/19/03/15/75076c485081d15ed9c224ad3e4ce4a1.jpg")
# # 涉黄图
# response = requests.get("https://cdn.pornpics.com/pics/2017-01-10/253759_12big.jpg")

# 内存中打开图片
image = Image.open(BytesIO(response.content))

# 图片的base64编码
ls_f = base64.b64encode(BytesIO(response.content).read())

# base64编码解码
imgdata = base64.b64decode(ls_f)

# 图片文件保存
file = open('test.jpg','wb')
file.write(imgdata)
file.close()

# img = tf.keras.preprocessing.image.array_to_img(frame)
# img = imgdata
img = load_img('test.jpg')
newsize = (299, 299)
img = img.resize(newsize)
img_array = keras.preprocessing.image.img_to_array(img)
img_array /= 255
img_array = tf.expand_dims(img_array, 0) # Create a batch

# r = requests.post(url="http://42.192.54.30:8501/v1/models/yellow_pic_model:predict", data=json.dumps(img_array))
# print(r.json())


url = 'http://42.192.54.30:8501/v1/models/yellow_pic_model:predict'
data = img_array.numpy()
# data = np.random.random((1, 299, 299, 3))


params = {'inputs': data.tolist()}
# params = {'inputs': data}
t = time.time()
res = requests.post(url, json=params)
print(time.time() - t)
print(res)
result = res.json()
predictions = np.array(result['outputs'])
y_pred = np.argmax(predictions, axis=1)
print(y_pred)
if y_pred == 0:
	print("THIS IS SAFE.")
else:
	print("THIS IS NSFW ⚠⚠⚠.")
print(result)
