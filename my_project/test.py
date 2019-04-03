#!/usr/bin/env python
# -*- coding:utf-8 -*-

from aip import AipImageSearch

# a = 'ab'+'bc'
# print(a)
# a = {"a":123}
# print(a["a"])
# print("a" in a.keys())
""" 你的APPID AK SK """
APP_ID = '15900910'
API_KEY = 'w9GDvddBuCn86NwxSTfFiocG'
SECRET_KEY = 'W8GgfxwpMpFjDlrFV4mLT1i1Y6pu4Lx1'

client = AipImageSearch(APP_ID, API_KEY, SECRET_KEY)
print(client.productDeleteBySign("1160357892,4224460940"))
#
# """  读取图片 """
# def get_file_content(filePath):
#     with open(filePath, 'rb') as fp:
#         return fp.read()
#
# image = get_file_content('sample.jpg')
#
# f = open('sample_1.jpg', 'wb')
# f.write(image)
# f.close()

# """ 调用相同图检索-入库，图片参数为本地图片 """
# client.similarAdd(image);
#
# """ 如果有可选参数 """
# options = {}
# options["brief"] = "{\"name\":\"周杰伦\", \"id\":\"666\"}"
# options["tags"] = "100,11"
#
# """ 带参数调用相同图检索-入库，图片参数为本地图片 """
# print(client.similarAdd(image, options))

# url = "http//www.x.com/sample.jpg"
#
# """ 调用相同图检索-入库，图片参数为远程url图片 """
# client.similarAdd(url);
#
# """ 如果有可选参数 """
# options = {}
# options["brief"] = "{\"name\":\"美图\", \"id\":\"666\"}"
# options["tags"] = "100,11"
#
# url = 'https://ss3.baidu.com/-fo3dSag_xI4khGko9WTAnF6hhy/image/h%3D300/sign=7dac85b2825494ee982209191df4e0e1/c2cec3fdfc03924558fae5028994a4c27d1e256b.jpg'
#
# """ 带参数调用相同图检索-入库，图片参数为远程图片 """
# print(client.similarAddUrl(url, options))

# """ 调用相似图检索—检索, 图片参数为本地图片 """
# client.similarSearch(image);

# """ 如果有可选参数 """
# options = {}
# options["tags"] = "100,11"
# options["tag_logic"] = "0"
# options["pn"] = "100"
# options["rn"] = "250"

# """ 带参数调用相似图检索—检索, 图片参数为本地图片 """
# print(client.similarSearch(image))


# """ 调用删除相似图，传入参数为图片 """
# print(client.similarDeleteByImage(image))