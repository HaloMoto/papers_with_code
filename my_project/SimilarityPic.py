#!/usr/bin/env python
# -*- coding:utf-8 -*-

from Pic import Pic
from Auxiliary import get_file_content
from aip import AipImageSearch

class SimilarityPic(Pic):
    """ 你的APPID AK SK """
    APP_ID = '15900910'
    API_KEY = 'w9GDvddBuCn86NwxSTfFiocG'
    SECRET_KEY = 'W8GgfxwpMpFjDlrFV4mLT1i1Y6pu4Lx1'

    def __init__(self, filePath):
        self.image = get_file_content(filePath)
        self.client = AipImageSearch(SimilarityPic.APP_ID, SimilarityPic.API_KEY, SimilarityPic.SECRET_KEY)
        self.options = {}
        self.url = None
        self.contSign = None

    # 相似图入库
    def putIn(self, sign):
        # 调用相似图检索—入库, 图片参数为本地图片
        if sign == 0:
            self.client.similarAdd(self.image)
        # 带参数调用相似图检索—入库, 图片参数为本地图片
        elif sign == 1:
            self.client.similarAdd(self.image, self.options)
        # 调用相似图检索—入库, 图片参数为远程url图片
        elif sign == 2:
            self.client.similarAddUrl(self.url)
        # 带参数调用相似图检索—入库, 图片参数为远程url图片
        elif sign == 3:
            self.client.similarAddUrl(self.url, self.options)
        else:
            print("请输入正确的sign")

    # 相似图检索
    def check(self, sign):
        # 调用相似图检索—检索, 图片参数为本地图片
        if sign == 0:
            self.client.similarSearch(self.image);
        # 带参数调用相似图检索—检索, 图片参数为本地图片
        elif sign == 1:
            self.client.similarSearch(self.image, self.options);
        # 调用相似图检索—检索, 图片参数为远程url图片
        elif sign == 2:
            self.client.similarSearchUrl(self.url)
        # 带参数调用相似图检索—检索, 图片参数为远程url图片
        elif sign == 3:
            self.client.similarSearchUrl(self.url, self.options)
        else:
            print("请输入正确的sign")

    # 相似图更新
    def renew(self, sign):
        # 调用相似图检索—更新, 图片参数为本地图片
        if sign == 0:
            self.client.similarUpdate(self.image)
        # 带参数调用相似图检索—更新, 图片参数为本地图片
        elif sign == 1:
            self.client.similarUpdate(self.image, self.options)
        # 调用相似图检索—更新, 图片参数为远程url图片
        elif sign == 2:
            self.client.similarUpdateUrl(self.url)
        # 带参数调用相似图检索—更新, 图片参数为远程url图片
        elif sign == 3:
            self.client.similarUpdateUrl(self.url, self.options)
        else:
            print("请输入正确的sign")

    # 相似图删除
    def delete(self,sign):
        # 调用删除相似图，传入参数为图片
        if sign == 0:
            self.client.similarDeleteByImage(self.image)
        # 调用删除相似图，图片参数为远程url图片
        elif sign == 1:
            self.client.similarDeleteByUrl(self.url)
        # 调用删除相似图，传入参数为图片签名
        elif sign == 2:
            self.client.similarDeleteBySign(self.contSign)
        else:
            print("请输入正确的sign")