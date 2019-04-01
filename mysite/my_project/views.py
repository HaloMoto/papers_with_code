from django.shortcuts import render
from django.shortcuts import HttpResponse
from my_project.service.SamePic import SamePic

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

# 相同图入库
def same_put_in(request):
    if request.method == "POST":
        # 获取表单传过来的图片
        image = request.FILES.get("image")
        # 获取表达传过来的图片类型
        category = request.POST.get("category", None)
        filePath = '/assets/img/'+image.name
        # 将图片保存到img目录下面
        filePath1 = 'assets/img/'+image.name
        f = open(filePath1,'wb')
        f.write(image.file.getvalue())
        f.close()
        # 定义一个相似图对象
        sp = SamePic(filePath1)
        # 给图片增加描述
        sp.options["brief"] = "{\"name\":\""+image.name+"\", \"url\":\""+filePath+"\"}"
        # 给图片增加类型
        sp.options["tags"] = "100,11"
        # 有图片描述的本地图片入库
        print(sp.putIn(1))
        return render(request, "admin-same.html")

# 相同图检索
def same_check(request):
    pass

# 相同图更新
def same_update(request):
    pass

# 相同图删除
def same_delete(request):
    pass

# 相似图入库
def similar_put_in(request):
    pass

# 相似图检索
def similar_check(request):
    pass

# 相似图更新
def similar_update(request):
    pass

# 相似图删除
def similar_delete(request):
    pass

# 商品图入库
def product_put_in(request):
    pass

# 商品图检索
def product_check(request):
    pass

# 商品图更新
def product_update(request):
    pass

# 商品图删除
def product_delete(request):
    pass