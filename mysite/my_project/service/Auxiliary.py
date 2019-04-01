#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 读取图片
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()