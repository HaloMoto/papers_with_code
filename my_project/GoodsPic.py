#!/usr/bin/env python
# -*- coding:utf-8 -*-

from Pic import Pic
from Auxiliary import get_file_content
from aip import AipImageSearch

class GoodsPic(Pic):
    """ 你的APPID AK SK """
    APP_ID = '15900910'
    API_KEY = 'w9GDvddBuCn86NwxSTfFiocG'
    SECRET_KEY = 'W8GgfxwpMpFjDlrFV4mLT1i1Y6pu4Lx1'

    def __init__(self, filePath):
        self.image = get_file_content(filePath)
        self.client = AipImageSearch(GoodsPic.APP_ID, GoodsPic.API_KEY, GoodsPic.SECRET_KEY)
        self.options = {}
        self.url = None
        self.contSign = None

    # 商品入库
    def putIn(self, sign):
        # 调用商品检索—入库, 图片参数为本地图片
        if sign == 0:
            self.client.productAdd(self.image)
        # 带参数调用商品检索—入库, 图片参数为本地图片
        elif sign == 1:
            self.client.productAdd(self.image, self.options)
        # 调用商品检索—入库, 图片参数为远程url图片
        elif sign == 2:
            self.client.productAddUrl(self.url)
        # 带参数调用商品检索—入库, 图片参数为远程url图片
        elif sign == 3:
            self.client.productAddUrl(self.url, self.options)
        else:
            print("请输入正确的sign")

    # 商品检索
    def check(self, sign):
        # 调用商品检索—检索, 图片参数为本地图片
        if sign == 0:
            self.client.productSearch(self.image);
        # 带参数调用商品检索—检索, 图片参数为本地图片
        elif sign == 1:
            self.client.productSearch(self.image, self.options);
        # 调用商品检索—检索, 图片参数为远程url图片
        elif sign == 2:
            self.client.productSearchUrl(self.url)
        # 带参数调用商品检索—检索, 图片参数为远程url图片
        elif sign == 3:
            self.client.productSearchUrl(self.url, self.options)
        else:
            print("请输入正确的sign")

    # 商品更新
    def renew(self, sign):
        # 调用商品检索—更新, 图片参数为本地图片
        if sign == 0:
            self.client.productUpdate(self.image)
        # 带参数调用商品检索—更新, 图片参数为本地图片
        elif sign == 1:
            self.client.productUpdate(self.image, self.options)
        # 调用商品检索—更新, 图片参数为远程url图片
        elif sign == 2:
            self.client.productUpdateUrl(self.url)
        # 带参数调用商品检索—更新, 图片参数为远程url图片
        elif sign == 3:
            self.client.productUpdateUrl(self.url, self.options)
        else:
            print("请输入正确的sign")

    # 商品删除
    def delete(self,sign):
        # 调用删除商品，传入参数为图片
        if sign == 0:
            self.client.productDeleteByImage(self.image)
        # 调用删除商品，图片参数为远程url图片
        elif sign == 1:
            self.client.productDeleteByUrl(self.url)
        # 调用删除商品，传入参数为图片签名
        elif sign == 2:
            self.client.productDeleteBySign(self.contSign)
        else:
            print("请输入正确的sign")