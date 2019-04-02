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
        category = request.POST.get("category", None)
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
        sp.options["tags"] = "100,11"
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
        if category:
            # 定义一个相同图对象
            sp = SamePic()
            sp.image = image.file.getvalue()
            # 设置可选参数
            sp.options["tags"] = "100,11"
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
        if category:
            # 定义一个相同图对象
            sp = SamePic()
            sp.image = image.file.getvalue()
            # 可选参数
            sp.options["brief"]  = "{\"name\":\"周杰伦\", \"id\":\"666\"}"
            sp.options["tags"] = "100,11"
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
        sp.options["tags"] = "100,11"
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
        if category:
            # 定义一个相似图对象
            sp = SimilarityPic()
            sp.image = image.file.getvalue()
            # 设置可选参数
            sp.options["tags"] = "100,11"
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
        if category:
            # 定义一个相似图对象
            sp = SimilarityPic()
            sp.image = image.file.getvalue()
            # 可选参数
            sp.options["brief"] = "{\"name\":\"周杰伦\", \"id\":\"666\"}"
            sp.options["tags"] = "100,11"
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
        gp.options["class_id1"] = 1
        gp.options["class_id2"] = 1
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
        if category:
            # 定义一个商品图对象
            gp = GoodsPic()
            gp.image = image.file.getvalue()
            # 设置可选参数
            gp.options["class_id1"] = 1
            gp.options["class_id2"] = 1
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
        if category:
            # 定义一个商品图对象
            gp = GoodsPic()
            gp.image = image.file.getvalue()
            # 可选参数
            gp.options["brief"] = "{\"name\":\"周杰伦\", \"id\":\"666\"}"
            gp.options["class_id1"] = 1
            gp.options["class_id2"] = 1
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
        # 获取图片名称
        image_name = request.POST.get("name", None)
        # 定义一个相同图对象
        sp = SamePic()
        sp.url = image_url
        # 给图片增加描述
        sp.options["brief"] = "{\"name\":\""+image_name+"\", \"url\":\""+image_url+"\"}"
        # 给图片增加类型
        sp.options["tags"] = "100,11"
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
        image = request.POST.get("URL")
        # 获取表单传过来的图片类型
        category = request.POST.get("category", None)
        if category:
            # 定义一个相同图对象
            sp = SamePic()
            sp.image = image.file.getvalue()
            # 设置可选参数
            sp.options["tags"] = "100,11"
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
def same_update_url(request):
    # 判断请求方法为post
    if request.method == "POST":
        # 获取表单传过来的图片
        image = request.FILES.get("image")
        # 获取表单传过来的图片类型
        category = request.POST.get("category",None)
        if category:
            # 定义一个相同图对象
            sp = SamePic()
            sp.image = image.file.getvalue()
            # 可选参数
            sp.options["brief"]  = "{\"name\":\"周杰伦\", \"id\":\"666\"}"
            sp.options["tags"] = "100,11"
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
def same_delete_url(request):
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
def similar_put_in_url(request):
    if request.method == "POST":
        # 获取表单传过来的图片
        image = request.FILES.get("image")
        # 获取表单传过来的图片类型
        category = request.POST.get("category", None)
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
        sp.options["tags"] = "100,11"
        # 有图片描述的本地图片入库
        data = sp.putIn(1)
        # 判断是否是返回错误信息
        if 'error_msg' in data.keys():
            return render(request, "admin-similar.html", {"error_msg": data['error_msg'], "sign": 0})
        else:
            return render(request, 'admin-similar.html', {"sign": 1})

# 相似图检索
def similar_check_url(request):
    # 判断请求方法为post
    if request.method == "POST":
        # 获取表单传过来的图片
        image = request.FILES.get("image")
        # 获取表单传过来的图片类型
        category = request.POST.get("category", None)
        if category:
            # 定义一个相似图对象
            sp = SimilarityPic()
            sp.image = image.file.getvalue()
            # 设置可选参数
            sp.options["tags"] = "100,11"
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
def similar_update_url(request):
    # 判断请求方法为post
    if request.method == "POST":
        # 获取表单传过来的图片
        image = request.FILES.get("image")
        # 获取表单传过来的图片类型
        category = request.POST.get("category", None)
        if category:
            # 定义一个相似图对象
            sp = SimilarityPic()
            sp.image = image.file.getvalue()
            # 可选参数
            sp.options["brief"] = "{\"name\":\"周杰伦\", \"id\":\"666\"}"
            sp.options["tags"] = "100,11"
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
def similar_delete_url(request):
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
def product_put_in_url(request):
    if request.method == "POST":
        # 获取表单传过来的图片
        image = request.FILES.get("image")
        # 获取表达传过来的图片类型
        category = request.POST.get("category", None)
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
        gp.options["class_id1"] = 1
        gp.options["class_id2"] = 1
        # 有图片描述的本地图片入库
        data = gp.putIn(1)
        print(data)
        # 判断是否是返回错误信息
        if 'error_msg' in data.keys():
            return render(request, "admin-product.html", {"error_msg":data['error_msg'], "sign":0})
        else:
            return render(request, 'admin-product.html', {"sign":1})

# 商品图检索
def product_check_url(request):
    # 判断请求方法为post
    if request.method == "POST":
        # 获取表单传过来的图片
        image = request.FILES.get("image")
        # 获取表单传过来的图片类型
        category = request.POST.get("category", None)
        if category:
            # 定义一个商品图对象
            gp = GoodsPic()
            gp.image = image.file.getvalue()
            # 设置可选参数
            gp.options["class_id1"] = 1
            gp.options["class_id2"] = 1
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
def product_update_url(request):
    # 判断请求方法为post
    if request.method == "POST":
        # 获取表单传过来的图片
        image = request.FILES.get("image")
        # 获取表单传过来的图片类型
        category = request.POST.get("category", None)
        if category:
            # 定义一个商品图对象
            gp = GoodsPic()
            gp.image = image.file.getvalue()
            # 可选参数
            gp.options["brief"] = "{\"name\":\"周杰伦\", \"id\":\"666\"}"
            gp.options["class_id1"] = 1
            gp.options["class_id2"] = 1
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
def product_delete_url(request):
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