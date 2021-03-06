#!/usr/bin/env python
# -*- coding:utf-8 -*-

from Pic import Pic
from Auxiliary import get_file_content
from aip import AipImageSearch

class SamePic(Pic):
    """ 你的APPID AK SK """
    APP_ID = '15900910'
    API_KEY = 'w9GDvddBuCn86NwxSTfFiocG'
    SECRET_KEY = 'W8GgfxwpMpFjDlrFV4mLT1i1Y6pu4Lx1'

    def __init__(self, filePath):
        self.image = get_file_content(filePath)
        self.client = AipImageSearch(SamePic.APP_ID, SamePic.API_KEY, SamePic.SECRET_KEY)
        self.options = {}
        self.url = None
        self.contSign = None

    # 相同图入库
    def putIn(self, sign):
        # 调用相同图检索—入库, 图片参数为本地图片
        if sign == 0:
            self.client.sameHqAdd(self.image)
        # 带参数调用相同图检索—入库, 图片参数为本地图片
        elif sign == 1:
            self.client.sameHqAdd(self.image, self.options)
        # 调用相同图检索—入库, 图片参数为远程url图片
        elif sign == 2:
            self.client.sameHqAddUrl(self.url)
        # 带参数调用相同图检索—入库, 图片参数为远程url图片
        elif sign == 3:
            self.client.sameHqAddUrl(self.url, self.options)
        else:
            print("请输入正确的sign")

    # 相同图检索
    def check(self, sign):
        # 调用相同图检索—检索, 图片参数为本地图片
        if sign == 0:
            self.client.sameHqSearch(self.image);
        # 带参数调用相同图检索—检索, 图片参数为本地图片
        elif sign == 1:
            self.client.sameHqSearch(self.image, self.options);
        # 调用相同图检索—检索, 图片参数为远程url图片
        elif sign == 2:
            self.client.sameHqSearchUrl(self.url)
        # 带参数调用相同图检索—检索, 图片参数为远程url图片
        elif sign == 3:
            self.client.sameHqSearchUrl(self.url, self.options)
        else:
            print("请输入正确的sign")

    # 相同图更新
    def renew(self, sign):
        # 调用相同图检索—更新, 图片参数为本地图片
        if sign == 0:
            self.client.sameHqUpdate(self.image)
        # 带参数调用相同图检索—更新, 图片参数为本地图片
        elif sign == 1:
            self.client.sameHqUpdate(self.image, self.options)
        # 调用相同图检索—更新, 图片参数为远程url图片
        elif sign == 2:
            self.client.sameHqUpdateUrl(self.url)
        # 带参数调用相同图检索—更新, 图片参数为远程url图片
        elif sign == 3:
            self.client.sameHqUpdateUrl(self.url, self.options)
        else:
            print("请输入正确的sign")

    # 相同图删除
    def delete(self,sign):
        # 调用删除相同图，传入参数为图片
        if sign == 0:
            self.client.sameHqDeleteByImage(self.image)
        # 调用删除相同图，图片参数为远程url图片
        elif sign == 1:
            self.client.sameHqDeleteByUrl(self.url)
        # 调用删除相同图，传入参数为图片签名
        elif sign == 2:
            self.client.sameHqDeleteBySign(self.contSign)
        else:
            print("请输入正确的sign")