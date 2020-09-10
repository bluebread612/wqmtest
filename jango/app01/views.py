from django.http import HttpResponse
from django.shortcuts import render
from . import test10
from .test10 import search_action


def index(request):
    return render(request, 'index.html')


def stack(request):
    return render(request, 'stack-example.html')


def login(request):
    # print(request.method)
    if request.method == "GET":
        return render(request, "login.html")
    else:
        # print(request.POST)
        action_type = request.POST.get("type")
        number = request.POST.get("numb")
        # print(number)
        # print(action_type)
        # 下面数据库操作
        json_data = search_action(number, action_type, 3)
        print(json_data)
        print(len(json_data))
        if len(json_data) == 2:
            return render(request, "fail.html")  # 这里可以替换成弹窗提示，或者更精致的页面
        else:
            return HttpResponse("OK")   # 这里需要替换为返回json数据到前端

