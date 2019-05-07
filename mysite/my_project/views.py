from django.shortcuts import render
from django.shortcuts import HttpResponse
from my_project.service.SamePic import SamePic
from my_project.service.SimilarityPic import SimilarityPic
from my_project.service.GoodsPic import GoodsPic
from my_project.service.Auxiliary import get_file_content
import json
import os

# Create your views here.

user_list = [
    {"user":"jack", "pwd":"abc"},
    {"user":"tom", "pwd":"ABC"}
]

# 相同图类别字典
samePicCategoryDict = {
    "白种人男性":"1", "白种人女性":"2", "黄种人男性":"3", "黄种人女性":"4", "黑种人男性":"5", "黑种人女性":"6", "澳大利亚人种男性":"7", "澳大利亚人种女性":"8", "哺乳动物":"9",
    "两栖动物":"10", "昆虫":"11", "鱼类":"12", "鸟类":"13", "床上用品":"14", "厨卫用品":"15", "家用电器":"16", "家具":"17", "日常用品":"18",
    "饮料":"19", "食物":"20", "机动车":"21", "非机动车":"22", "飞机":"23", "船":"24", "航天器":"25", "自然风光":"26", "城市风光":"27",
    "旅游名胜":"28", "other":"29"
}
# 相似图类别字典
similarPicCategoryDict = {
    "白种人男性":"1", "白种人女性":"2", "黄种人男性":"3", "黄种人女性":"4", "黑种人男性":"5", "黑种人女性":"6", "澳大利亚人种男性":"7", "澳大利亚人种女性":"8", "哺乳动物":"9",
    "两栖动物":"10", "昆虫":"11", "鱼类":"12", "鸟类":"13", "床上用品":"14", "厨卫用品":"15", "家用电器":"16", "家具":"17", "日常用品":"18",
    "饮料":"19", "食物":"20", "机动车":"21", "非机动车":"22", "飞机":"23", "船":"24", "航天器":"25", "自然风光":"26", "城市风光":"27",
    "旅游名胜":"28", "other":"30"
}
# 商品图类别字典
productPicCategoryDict = {
    "女装":"1", "女鞋":"2", "男装":"3", "男鞋":"4", "内衣":"5", "母婴":"6", "手机":"7", "数码":"8", "家电":"9",
    "美妆":"10", "箱包":"11", "运动":"12", "户外":"13", "家装":"14", "家纺":"15", "居家百货":"16", "鲜花宠物":"17", "配饰":"18",
    "食品":"19", "生鲜":"20", "汽车摩托":"21", "医药":"22", "图书":"23", "通信":"24", "洗护":"25", "乐器":"26", "other":"27"
}

def index(request):
    # request.POST
    # request.GET
    # return HttpResponse('Hello world!')
    if request.method == "POST":
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        print(username, password)
        temp = {"user":username, "pwd":password}
        user_list.append(temp)
    return render(request, "index.html",{"data":user_list})

def index_same(request):
    return render(request, "admin-same.html")

def index_similar(request):
    return render(request, "admin-similar.html")

def index_product(request):
    return render(request, "admin-product.html")

def index_same_url(request):
    return render(request, "admin-same-url.html")

def index_similar_url(request):
    return render(request, "admin-similar-url.html")

def index_product_url(request):
    return render(request, "admin-product-url.html")

# 相同图入库
def same_put_in(request):
    if request.method == "POST":
        # 获取表单传过来的图片
        image = request.FILES.get("image")
        # 获取表单传过来的图片类型
        category = request.POST.get("category", "other")
        if samePicCategoryDict.get(category):
            category_id = samePicCategoryDict[category]
        else:
            category_id = samePicCategoryDict["other"]
        filePath = '/assets/img/same/'+image.name
        # 将图片保存到img目录下面
        filePath1 = 'assets/img/same/'+image.name
        f = open(filePath1,'wb')
        f.write(image.file.getvalue())
        f.close()
        # 定义一个相同图对象
        sp = SamePic()
        sp.image = get_file_content(filePath1)
        # 文件名
        (filename, extension) = os.path.splitext(image.name)
        # 给图片增加描述
        sp.options["brief"] = "{\"name\":\""+filename+"\", \"url\":\""+filePath+"\"}"
        # 给图片增加类型
        sp.options["tags"] = category_id
        # 有图片描述的本地图片入库
        data = sp.putIn(1)
        # 判断是否是返回错误信息
        if 'error_msg' in data.keys():
            return render(request, "admin-same.html", {"error_msg": data['error_msg'], "sign": 0})
        else:
            return render(request, 'admin-same.html', {"sign": 1})

# 相同图检索
def same_check(request):
    # 判断请求方法为post
    if request.method == "POST":
        # 获取表单传过来的图片
        image = request.FILES.get("image")
        # 获取表单传过来的图片类型
        category = request.POST.get("category", None)
        if samePicCategoryDict.get(category):
            category_id = samePicCategoryDict[category]
        else:
            category_id = samePicCategoryDict["other"]
        if category:
            # 定义一个相同图对象
            print(category,category_id)
            sp = SamePic()
            sp.image = image.file.getvalue()
            # 设置可选参数
            sp.options["tags"] = category_id
            sp.options["tag_logic"] = "0"
            sp.options["pn"] = "0"
            sp.options["rn"] = "1000"
            # 本地图片检索
            data = sp.check(1)
            # 将字符串转为字典
            for image in data['result']:
                print(image['brief'])
                image['brief'] = json.loads(image['brief'])
            # 判断是否是返回错误信息
            if 'error_msg' in data.keys():
                return render(request, "admin-same.html", {"error_msg": data['error_msg'], "sign": 0})
            else:
                return render(request, "admin-gallery.html", {"data": data})
        else:
            # 定义一个相同图对象
            sp = SamePic()
            sp.image = image.file.getvalue()
            # 本地图片检索
            data = sp.check(0)
            # 将字符串转为字典
            for image in data['result']:
                print("hello",image['brief'])
                image['brief'] = json.loads(image['brief'])
            # 判断是否是返回错误信息
            if 'error_msg' in data.keys():
                return render(request, "admin-same.html", {"error_msg": data['error_msg'], "sign": 0})
            else:
                return render(request, "admin-gallery.html", {"data": data})

# 相同图更新
def same_update(request):
    # 判断请求方法为post
    if request.method == "POST":
        # 获取表单传过来的图片
        image = request.FILES.get("image")
        # 获取表单传过来的图片类型
        category = request.POST.get("category",None)
        if samePicCategoryDict.get(category):
            category_id = samePicCategoryDict[category]
        else:
            category_id = samePicCategoryDict["other"]
        if category:
            # 定义一个相同图对象
            sp = SamePic()
            sp.image = image.file.getvalue()
            # 可选参数
            # sp.options["brief"]  = "{\"name\":\"周杰伦\", \"id\":\"666\"}"
            sp.options["tags"] = category_id
            # 本地图片更新
            data = sp.update(1)
            # 判断是否是返回错误信息
            if 'error_msg' in data.keys():
                return render(request, "admin-same.html", {"error_msg": data['error_msg'], "sign": 0})
            else:
                return render(request, 'admin-same.html', {"sign": 1})
        else:
            # 定义一个相同图对象
            sp = SamePic()
            sp.image = image.file.getvalue()
            # 本地图片更新
            data = sp.update(0)
            # 判断是否是返回错误信息
            if 'error_msg' in data.keys():
                return render(request, "admin-same.html", {"error_msg": data['error_msg'], "sign": 0})
            else:
                return render(request, 'admin-same.html', {"sign": 1})

# 相同图删除
def same_delete(request):
    # 判断请求方法为post
    if request.method == "POST":
        # 获取表单传过来的图片
        image = request.FILES.get("image")
        # 定义一个相同图对象
        sp = SamePic()
        sp.image = image.file.getvalue()
        # 本地图片更新
        data = sp.delete(0)
        # 判断是否是返回错误信息
        if 'error_msg' in data.keys():
            return render(request, "admin-same.html", {"error_msg": data['error_msg'], "sign": 0})
        else:
            return render(request, 'admin-same.html', {"sign": 1})

# 相似图入库
def similar_put_in(request):
    if request.method == "POST":
        # 获取表单传过来的图片
        image = request.FILES.get("image")
        # 获取表单传过来的图片类型
        category = request.POST.get("category", None)
        if similarPicCategoryDict.get(category):
            category_id = similarPicCategoryDict[category]
        else:
            category_id = similarPicCategoryDict["other"]
        filePath = '/assets/img/similar/'+image.name
        # 将图片保存到img目录下面
        filePath1 = 'assets/img/similar/'+image.name
        f = open(filePath1,'wb')
        f.write(image.file.getvalue())
        f.close()
        # 定义一个相似图对象
        sp = SimilarityPic()
        sp.image = get_file_content(filePath1)
        # 文件名
        (filename, extension) = os.path.splitext(image.name)
        # 给图片增加描述
        sp.options["brief"] = "{\"name\":\""+filename+"\", \"url\":\""+filePath+"\"}"
        # 给图片增加类型
        sp.options["tags"] = category_id
        # 有图片描述的本地图片入库
        data = sp.putIn(1)
        # 判断是否是返回错误信息
        if 'error_msg' in data.keys():
            return render(request, "admin-similar.html", {"error_msg": data['error_msg'], "sign": 0})
        else:
            return render(request, 'admin-similar.html', {"sign": 1})

# 相似图检索
def similar_check(request):
    # 判断请求方法为post
    if request.method == "POST":
        # 获取表单传过来的图片
        image = request.FILES.get("image")
        # 获取表单传过来的图片类型
        category = request.POST.get("category", None)
        if similarPicCategoryDict.get(category):
            category_id = similarPicCategoryDict[category]
        else:
            category_id = similarPicCategoryDict["other"]
        if category:
            # 定义一个相似图对象
            sp = SimilarityPic()
            sp.image = image.file.getvalue()
            # 设置可选参数
            sp.options["tags"] = category_id
            sp.options["tag_logic"] = "0"
            sp.options["pn"] = "0"
            sp.options["rn"] = "1000"
            # 本地图片检索
            data = sp.check(1)
            # 将字符串转为字典
            for image in data['result']:
                print(image['brief'])
                image['brief'] = json.loads(image['brief'])
            # 判断是否是返回错误信息
            if 'error_msg' in data.keys():
                return render(request, "admin-similar.html", {"error_msg": data['error_msg'], "sign": 0})
            else:
                return render(request, "admin-gallery.html", {"data": data})
        else:
            # 定义一个相似图对象
            sp = SimilarityPic()
            sp.image = image.file.getvalue()
            # 本地图片检索
            data = sp.check(0)
            # 将字符串转为字典
            for image in data['result']:
                print("hello", image['brief'])
                image['brief'] = json.loads(image['brief'])
            # 判断是否是返回错误信息
            if 'error_msg' in data.keys():
                return render(request, "admin-similar.html", {"error_msg": data['error_msg'], "sign": 0})
            else:
                return render(request, "admin-gallery.html", {"data": data})

# 相似图更新
def similar_update(request):
    # 判断请求方法为post
    if request.method == "POST":
        # 获取表单传过来的图片
        image = request.FILES.get("image")
        # 获取表单传过来的图片类型
        category = request.POST.get("category", None)
        if similarPicCategoryDict.get(category):
            category_id = similarPicCategoryDict[category]
        else:
            category_id = similarPicCategoryDict["other"]
        if category:
            # 定义一个相似图对象
            sp = SimilarityPic()
            sp.image = image.file.getvalue()
            # 可选参数
            # sp.options["brief"] = "{\"name\":\"周杰伦\", \"id\":\"666\"}"
            sp.options["tags"] = category_id
            # 本地图片更新
            data = sp.update(1)
            # 判断是否是返回错误信息
            if 'error_msg' in data.keys():
                return render(request, "admin-similar.html", {"error_msg": data['error_msg'], "sign": 0})
            else:
                return render(request, 'admin-similar.html', {"sign": 1})
        else:
            # 定义一个相似图对象
            sp = SimilarityPic()
            sp.image = image.file.getvalue()
            # 本地图片更新
            data = sp.update(0)
            # 判断是否是返回错误信息
            if 'error_msg' in data.keys():
                return render(request, "admin-similar.html", {"error_msg": data['error_msg'], "sign": 0})
            else:
                return render(request, 'admin-similar.html', {"sign": 1})

# 相似图删除
def similar_delete(request):
    # 判断请求方法为post
    if request.method == "POST":
        # 获取表单传过来的图片
        image = request.FILES.get("image")
        # 定义一个相似图对象
        sp = SimilarityPic()
        sp.image = image.file.getvalue()
        # 本地图片更新
        data = sp.delete(0)
        # 判断是否是返回错误信息
        if 'error_msg' in data.keys():
            return render(request, "admin-similar.html", {"error_msg": data['error_msg'], "sign": 0})
        else:
            return render(request, 'admin-similar.html', {"sign": 1})

# 商品图入库
def product_put_in(request):
    if request.method == "POST":
        # 获取表单传过来的图片
        image = request.FILES.get("image")
        # 获取表达传过来的图片类型
        category = request.POST.get("category", None)
        if productPicCategoryDict.get(category):
            category_id = productPicCategoryDict[category]
        else:
            category_id = productPicCategoryDict["other"]
        filePath = '/assets/img/product/'+image.name
        # 将图片保存到img目录下面
        filePath1 = 'assets/img/product/'+image.name
        f = open(filePath1,'wb')
        f.write(image.file.getvalue())
        f.close()
        # 定义一个商品图对象
        gp = GoodsPic()
        gp.image = get_file_content(filePath1)
        # 文件名
        (filename, extension) = os.path.splitext(image.name)
        # 给图片增加描述
        gp.options["brief"] = "{\"name\":\""+filename+"\", \"url\":\""+filePath+"\"}"
        # 给图片增加类型
        gp.options["class_id1"] = int(category_id)
        # 有图片描述的本地图片入库
        data = gp.putIn(1)
        print(data)
        # 判断是否是返回错误信息
        if 'error_msg' in data.keys():
            return render(request, "admin-product.html", {"error_msg":data['error_msg'], "sign":0})
        else:
            return render(request, 'admin-product.html', {"sign":1})

# 商品图检索
def product_check(request):
    # 判断请求方法为post
    if request.method == "POST":
        # 获取表单传过来的图片
        image = request.FILES.get("image")
        # 获取表单传过来的图片类型
        category = request.POST.get("category", None)
        if productPicCategoryDict.get(category):
            category_id = productPicCategoryDict[category]
        else:
            category_id = productPicCategoryDict["other"]
        if category:
            # 定义一个商品图对象
            gp = GoodsPic()
            gp.image = image.file.getvalue()
            # 设置可选参数
            gp.options["class_id1"] = int(category_id)
            gp.options["pn"] = "0"
            gp.options["rn"] = "1000"
            # 本地图片检索
            data = gp.check(1)
            # 将字符串转为字典
            for image in data['result']:
                print(image['brief'])
                image['brief'] = json.loads(image['brief'])
            # 判断是否是返回错误信息
            if 'error_msg' in data.keys():
                return render(request, "admin-product.html", {"error_msg": data['error_msg'], "sign": 0})
            else:
                return render(request, "admin-gallery.html", {"data": data})
        else:
            # 定义一个商品图对象
            gp = GoodsPic()
            gp.image = image.file.getvalue()
            # 本地图片检索
            data = gp.check(0)
            # 将字符串转为字典
            for image in data['result']:
                print("hello", image['brief'])
                image['brief'] = json.loads(image['brief'])

            # 判断是否是返回错误信息
            if 'error_msg' in data.keys():
                return render(request, "admin-product.html", {"error_msg": data['error_msg'], "sign": 0})
            else:
                return render(request, "admin-gallery.html", {"data": data})

# 商品图更新
def product_update(request):
    # 判断请求方法为post
    if request.method == "POST":
        # 获取表单传过来的图片
        image = request.FILES.get("image")
        # 获取表单传过来的图片类型
        category = request.POST.get("category", None)
        if productPicCategoryDict.get(category):
            category_id = productPicCategoryDict[category]
        else:
            category_id = productPicCategoryDict["other"]
        if category:
            # 定义一个商品图对象
            gp = GoodsPic()
            gp.image = image.file.getvalue()
            # 可选参数
            gp.options["brief"] = "{\"name\":\"周杰伦\", \"id\":\"666\"}"
            gp.options["class_id1"] = int(category_id)
            # 本地图片更新
            data = gp.update(1)
            # 判断是否是返回错误信息
            if 'error_msg' in data.keys():
                return render(request, "admin-product.html", {"error_msg": data['error_msg'], "sign": 0})
            else:
                return render(request, 'admin-product.html', {"sign": 1})
        else:
            # 定义一个相同图对象
            gp = GoodsPic()
            gp.image = image.file.getvalue()
            # 本地图片更新
            data = gp.update(0)

            # 判断是否是返回错误信息
            if 'error_msg' in data.keys():
                return render(request, "admin-product.html", {"error_msg": data['error_msg'], "sign": 0})
            else:
                return render(request, 'admin-product.html', {"sign": 1})

# 商品图删除
def product_delete(request):
    # 判断请求方法为post
    if request.method == "POST":
        # 获取表单传过来的图片
        image = request.FILES.get("image")
        # 定义一个相同图对象
        gp = GoodsPic()
        gp.image = image.file.getvalue()
        # 本地图片更新
        data = gp.delete(0)

        # 判断是否是返回错误信息
        if 'error_msg' in data.keys():
            return render(request, "admin-product.html", {"error_msg": data['error_msg'], "sign": 0})
        else:
            return render(request, 'admin-product.html', {"sign": 1})

# 相同图入库
def same_put_in_url(request):
    if request.method == "POST":
        # 获取表单传过来的网络地址
        image_url = request.POST.get("URL")
        # 获取表单传过来的图片类型
        category = request.POST.get("category", None)
        if samePicCategoryDict.get(category):
            category_id = samePicCategoryDict[category]
        else:
            category_id = samePicCategoryDict["other"]
        # 获取图片名称
        image_name = request.POST.get("name", None)
        # 定义一个相同图对象
        sp = SamePic()
        sp.url = image_url
        # 给图片增加描述
        sp.options["brief"] = "{\"name\":\""+image_name+"\", \"url\":\""+image_url+"\"}"
        # 给图片增加类型
        sp.options["tags"] = category_id
        # 有图片描述的本地图片入库
        data = sp.putIn(3)
        # 判断是否是返回错误信息
        if 'error_msg' in data.keys():
            return render(request, "admin-same-url.html", {"error_msg": data['error_msg'], "sign": 0})
        else:
            return render(request, 'admin-same-url.html', {"sign": 1})

# 相同图检索
def same_check_url(request):
    # 判断请求方法为post
    if request.method == "POST":
        # 获取表单传过来的网络地址
        image_url = request.POST.get("URL")
        # 获取表单传过来的图片类型
        category = request.POST.get("category", None)
        if samePicCategoryDict.get(category):
            category_id = samePicCategoryDict[category]
        else:
            category_id = samePicCategoryDict["other"]
        if category:
            # 定义一个相同图对象
            sp = SamePic()
            sp.url = image_url
            # 设置可选参数
            sp.options["tags"] = category_id
            sp.options["tag_logic"] = "0"
            sp.options["pn"] = "0"
            sp.options["rn"] = "1000"
            # 本地图片检索
            data = sp.check(3)
            # 将字符串转为字典
            for image in data['result']:
                print(image['brief'])
                image['brief'] = json.loads(image['brief'])
            # 判断是否是返回错误信息
            if 'error_msg' in data.keys():
                return render(request, "admin-same.html", {"error_msg": data['error_msg'], "sign": 0})
            else:
                return render(request, "admin-gallery.html", {"data": data})
        else:
            # 定义一个相同图对象
            sp = SamePic()
            sp.url = image_url
            # 本地图片检索
            data = sp.check(2)
            # 将字符串转为字典
            for image in data['result']:
                print("hello",image['brief'])
                image['brief'] = json.loads(image['brief'])
            # 判断是否是返回错误信息
            if 'error_msg' in data.keys():
                return render(request, "admin-same.html", {"error_msg": data['error_msg'], "sign": 0})
            else:
                return render(request, "admin-gallery.html", {"data": data})

# 相同图更新
def same_update_url(request):
    # 判断请求方法为post
    if request.method == "POST":
        # 获取表单传过来的URL
        image_url = request.POST.get("URL")
        # 获取表单传过来的图片类型
        category = request.POST.get("category",None)
        if samePicCategoryDict.get(category):
            category_id = samePicCategoryDict[category]
        else:
            category_id = samePicCategoryDict["other"]
        if category:
            # 定义一个相同图对象
            sp = SamePic()
            sp.url = image_url
            # 可选参数
            # sp.options["brief"]  = "{\"name\":\"周杰伦\", \"id\":\"666\"}"
            sp.options["tags"] = category_id
            # 本地图片更新
            data = sp.update(3)
            # 判断是否是返回错误信息
            if 'error_msg' in data.keys():
                return render(request, "admin-same.html", {"error_msg": data['error_msg'], "sign": 0})
            else:
                return render(request, 'admin-same.html', {"sign": 1})
        else:
            # 定义一个相同图对象
            sp = SamePic()
            sp.url = image_url
            # 本地图片更新
            data = sp.update(2)
            # 判断是否是返回错误信息
            if 'error_msg' in data.keys():
                return render(request, "admin-same.html", {"error_msg": data['error_msg'], "sign": 0})
            else:
                return render(request, 'admin-same.html', {"sign": 1})

# 相同图删除
def same_delete_url(request):
    # 判断请求方法为post
    if request.method == "POST":
        # 获取表单传过来的URL
        image_url = request.POST.get("URL")
        # 定义一个相同图对象
        sp = SamePic()
        sp.url = image_url
        # 本地图片更新
        data = sp.delete(1)
        # 判断是否是返回错误信息
        if 'error_msg' in data.keys():
            return render(request, "admin-same.html", {"error_msg": data['error_msg'], "sign": 0})
        else:
            return render(request, 'admin-same.html', {"sign": 1})

# 相似图入库
def similar_put_in_url(request):
    if request.method == "POST":
        # 获取表单传过来的网络地址
        image_url = request.POST.get("URL")
        # 获取表单传过来的图片类型
        category = request.POST.get("category", None)
        if similarPicCategoryDict.get(category):
            category_id = similarPicCategoryDict[category]
        else:
            category_id = similarPicCategoryDict["other"]
        # 获取图片名称
        image_name = request.POST.get("name", None)
        # 定义一个相似图对象
        sp = SimilarityPic()
        sp.url = image_url
        # 给图片增加描述
        sp.options["brief"] = "{\"name\":\""+image_name+"\", \"url\":\""+image_url+"\"}"
        # 给图片增加类型
        sp.options["tags"] = category_id
        # 有图片描述的本地图片入库
        data = sp.putIn(3)
        # 判断是否是返回错误信息
        if 'error_msg' in data.keys():
            return render(request, "admin-similar-url.html", {"error_msg": data['error_msg'], "sign": 0})
        else:
            return render(request, 'admin-similar-url.html', {"sign": 1})

# 相似图检索
def similar_check_url(request):
    # 判断请求方法为post
    if request.method == "POST":
        # 获取表单传过来的网络地址
        image_url = request.POST.get("URL")
        # 获取表单传过来的图片类型
        category = request.POST.get("category", None)
        if similarPicCategoryDict.get(category):
            category_id = similarPicCategoryDict[category]
        else:
            category_id = similarPicCategoryDict["other"]
        if category:
            # 定义一个相似图对象
            sp = SimilarityPic()
            sp.url = image_url
            # 设置可选参数
            sp.options["tags"] = category_id
            sp.options["tag_logic"] = "0"
            sp.options["pn"] = "0"
            sp.options["rn"] = "1000"
            # 本地图片检索
            data = sp.check(3)
            # 将字符串转为字典
            for image in data['result']:
                print(image['brief'])
                image['brief'] = json.loads(image['brief'])
            # 判断是否是返回错误信息
            if 'error_msg' in data.keys():
                return render(request, "admin-similar-url.html", {"error_msg": data['error_msg'], "sign": 0})
            else:
                return render(request, "admin-gallery.html", {"data": data})
        else:
            # 定义一个相似图对象
            sp = SimilarityPic()
            sp.url = image_url
            # 本地图片检索
            data = sp.check(2)
            # 将字符串转为字典
            for image in data['result']:
                print("hello", image['brief'])
                image['brief'] = json.loads(image['brief'])
            # 判断是否是返回错误信息
            if 'error_msg' in data.keys():
                return render(request, "admin-similar-url.html", {"error_msg": data['error_msg'], "sign": 0})
            else:
                return render(request, "admin-gallery.html", {"data": data})

# 相似图更新
def similar_update_url(request):
    # 判断请求方法为post
    if request.method == "POST":
        # 获取表单传过来的URL
        image_url = request.POST.get("URL")
        # 获取表单传过来的图片类型
        category = request.POST.get("category", None)
        if similarPicCategoryDict.get(category):
            category_id = similarPicCategoryDict[category]
        else:
            category_id = similarPicCategoryDict["other"]
        if category:
            # 定义一个相似图对象
            sp = SimilarityPic()
            sp.url = image_url
            # 可选参数
            # sp.options["brief"] = "{\"name\":\"周杰伦\", \"id\":\"666\"}"
            sp.options["tags"] = category_id
            # 本地图片更新
            data = sp.update(3)
            # 判断是否是返回错误信息
            if 'error_msg' in data.keys():
                return render(request, "admin-similar-url.html", {"error_msg": data['error_msg'], "sign": 0})
            else:
                return render(request, 'admin-similar-url.html', {"sign": 1})
        else:
            # 定义一个相似图对象
            sp = SimilarityPic()
            sp.url = image_url
            # 本地图片更新
            data = sp.update(2)
            # 判断是否是返回错误信息
            if 'error_msg' in data.keys():
                return render(request, "admin-similar-url.html", {"error_msg": data['error_msg'], "sign": 0})
            else:
                return render(request, 'admin-similar-url.html', {"sign": 1})

# 相似图删除
def similar_delete_url(request):
    # 判断请求方法为post
    if request.method == "POST":
        # 获取表单传过来的URL
        image_url = request.POST.get("URL")
        # 定义一个相似图对象
        sp = SimilarityPic()
        sp.url = image_url
        # 本地图片更新
        data = sp.delete(1)
        # 判断是否是返回错误信息
        if 'error_msg' in data.keys():
            return render(request, "admin-similar-url.html", {"error_msg": data['error_msg'], "sign": 0})
        else:
            return render(request, 'admin-similar-url.html', {"sign": 1})

# 商品图入库
def product_put_in_url(request):
    if request.method == "POST":
        # 获取表单传过来的网络地址
        image_url = request.POST.get("URL")
        # 获取表单传过来的图片类型
        category = request.POST.get("category", None)
        if productPicCategoryDict.get(category):
            category_id = productPicCategoryDict[category]
        else:
            category_id = productPicCategoryDict["other"]
        # 获取图片名称
        image_name = request.POST.get("name", None)
        # 定义一个商品图对象
        gp = GoodsPic()
        gp.url = image_url
        # 给图片增加描述
        gp.options["brief"] = "{\"name\":\""+image_name+"\", \"url\":\""+image_url+"\"}"
        # 给图片增加类型
        gp.options["class_id1"] = int(category_id)
        # 有图片描述的本地图片入库
        data = gp.putIn(3)
        # 判断是否是返回错误信息
        if 'error_msg' in data.keys():
            return render(request, "admin-product-url.html", {"error_msg": data['error_msg'], "sign": 0})
        else:
            return render(request, 'admin-product-url.html', {"sign": 1})

# 商品图检索
def product_check_url(request):
    # 判断请求方法为post
    if request.method == "POST":
        # 获取表单传过来的网络地址
        image_url = request.POST.get("URL")
        # 获取表单传过来的图片类型
        category = request.POST.get("category", None)
        if productPicCategoryDict.get(category):
            category_id = productPicCategoryDict[category]
        else:
            category_id = productPicCategoryDict["other"]
        if category:
            # 定义一个商品图对象
            gp = GoodsPic()
            gp.url = image_url
            # 设置可选参数
            gp.options["class_id1"] = int(category_id)
            gp.options["pn"] = "0"
            gp.options["rn"] = "1000"
            # 本地图片检索
            data = gp.check(3)
            # 将字符串转为字典
            for image in data['result']:
                print(image['brief'])
                image['brief'] = json.loads(image['brief'])
            # 判断是否是返回错误信息
            if 'error_msg' in data.keys():
                return render(request, "admin-product-url.html", {"error_msg": data['error_msg'], "sign": 0})
            else:
                return render(request, "admin-gallery.html", {"data": data})
        else:
            # 定义一个商品图对象
            gp = GoodsPic()
            gp.url = image_url
            # 本地图片检索
            data = gp.check(2)
            # 将字符串转为字典
            for image in data['result']:
                print("hello", image['brief'])
                image['brief'] = json.loads(image['brief'])
            # 判断是否是返回错误信息
            if 'error_msg' in data.keys():
                return render(request, "admin-product-url.html", {"error_msg": data['error_msg'], "sign": 0})
            else:
                return render(request, "admin-gallery.html", {"data": data})

# 商品图更新
def product_update_url(request):
    # 判断请求方法为post
    if request.method == "POST":
        # 获取表单传过来的URL
        image_url = request.POST.get("URL")
        # 获取表单传过来的图片类型
        category = request.POST.get("category", None)
        if productPicCategoryDict.get(category):
            category_id = productPicCategoryDict[category]
        else:
            category_id = productPicCategoryDict["other"]
        if category:
            # 定义一个商品图对象
            gp = GoodsPic()
            gp.url = image_url
            # 可选参数
            gp.options["brief"] = "{\"name\":\"周杰伦\", \"id\":\"666\"}"
            gp.options["class_id1"] = int(category_id)
            # 本地图片更新
            data = gp.update(3)
            # 判断是否是返回错误信息
            if 'error_msg' in data.keys():
                return render(request, "admin-product-url.html", {"error_msg": data['error_msg'], "sign": 0})
            else:
                return render(request, 'admin-product-url.html', {"sign": 1})
        else:
            # 定义一个商品图对象
            gp = GoodsPic()
            gp.url = image_url
            # 本地图片更新
            data = gp.update(2)
            # 判断是否是返回错误信息
            if 'error_msg' in data.keys():
                return render(request, "admin-product-url.html", {"error_msg": data['error_msg'], "sign": 0})
            else:
                return render(request, 'admin-product-url.html', {"sign": 1})

# 商品图删除
def product_delete_url(request):
    # 判断请求方法为post
    if request.method == "POST":
        # 获取表单传过来的URL
        image_url = request.POST.get("URL")
        # 定义一个商品图对象
        gp = GoodsPic()
        gp.url = image_url
        # 本地图片更新
        data = gp.delete(1)
        # 判断是否是返回错误信息
        if 'error_msg' in data.keys():
            return render(request, "admin-product-url.html", {"error_msg": data['error_msg'], "sign": 0})
        else:
            return render(request, 'admin-product-url.html', {"sign": 1})