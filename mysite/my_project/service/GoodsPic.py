#!/usr/bin/env python
# -*- coding:utf-8 -*-

from my_project.service.Pic import Pic
from my_project.service.Auxiliary import get_file_content
from aip import AipImageSearch

class GoodsPic(Pic):
    """ 你的APPID AK SK """
    APP_ID = '15900910'
    API_KEY = 'w9GDvddBuCn86NwxSTfFiocG'
    SECRET_KEY = 'W8GgfxwpMpFjDlrFV4mLT1i1Y6pu4Lx1'

    def __init__(self):
        self.image = None
        self.client = AipImageSearch(GoodsPic.APP_ID, GoodsPic.API_KEY, GoodsPic.SECRET_KEY)
        self.options = {}
        self.url = None
        self.contSign = None

    # 商品入库
    def putIn(self, sign):
        # 调用商品检索—入库, 图片参数为本地图片
        if sign == 0:
            return self.client.productAdd(self.image)
        # 带参数调用商品检索—入库, 图片参数为本地图片
        elif sign == 1:
            return self.client.productAdd(self.image, self.options)
        # 调用商品检索—入库, 图片参数为远程url图片
        elif sign == 2:
            return self.client.productAddUrl(self.url)
        # 带参数调用商品检索—入库, 图片参数为远程url图片
        elif sign == 3:
            return self.client.productAddUrl(self.url, self.options)
        else:
            print("请输入正确的sign")

    # 商品检索
    def check(self, sign):
        # 调用商品检索—检索, 图片参数为本地图片
        if sign == 0:
            return self.client.productSearch(self.image);
        # 带参数调用商品检索—检索, 图片参数为本地图片
        elif sign == 1:
            return self.client.productSearch(self.image, self.options);
        # 调用商品检索—检索, 图片参数为远程url图片
        elif sign == 2:
            return self.client.productSearchUrl(self.url)
        # 带参数调用商品检索—检索, 图片参数为远程url图片
        elif sign == 3:
            return self.client.productSearchUrl(self.url, self.options)
        else:
            print("请输入正确的sign")

    # 商品更新
    def update(self, sign):
        # 调用商品检索—更新, 图片参数为本地图片
        if sign == 0:
            return self.client.productUpdate(self.image)
        # 带参数调用商品检索—更新, 图片参数为本地图片
        elif sign == 1:
            return self.client.productUpdate(self.image, self.options)
        # 调用商品检索—更新, 图片参数为远程url图片
        elif sign == 2:
            return self.client.productUpdateUrl(self.url)
        # 带参数调用商品检索—更新, 图片参数为远程url图片
        elif sign == 3:
            return self.client.productUpdateUrl(self.url, self.options)
        else:
            print("请输入正确的sign")

    # 商品删除
    def delete(self,sign):
        # 调用删除商品，传入参数为图片
        if sign == 0:
            return self.client.productDeleteByImage(self.image)
        # 调用删除商品，图片参数为远程url图片
        elif sign == 1:
            return self.client.productDeleteByUrl(self.url)
        # 调用删除商品，传入参数为图片签名
        elif sign == 2:
            return self.client.productDeleteBySign(self.contSign)
        else:
            print("请输入正确的sign")