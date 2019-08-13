#coding = utf-8
from django.core.paginator import Paginator
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from hashlib import sha1

from goods_manage.models import GoodsInfo
from order_manage.models import OrderInfo, OrderDetailInfo
from user_manage import login_decorator
from user_manage.models import UserInfo


def uname_exits(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})


def register(request):
    return render(request, 'user_manage/register.html')

def register_handle(request):
    post = request.POST
    uname = post['user_name']
    upwd = post['pwd']
    upwd2 = post['cpwd']
    uemail = post['email']
    if upwd2 != upwd:
        return redirect('/user/register/')
    sha = sha1()
    sha.update(upwd.encode('utf8'))
    upwd3 = sha.hexdigest()
    userinfo = UserInfo()
    userinfo.uname = uname
    userinfo.upwd = upwd3
    userinfo.uemail = uemail
    userinfo.save()
    return redirect('/user/login/')

def login(request):
    uname = request.COOKIES.get('uname', '')   # 从cookie中取用户名，取不到置为空
    context = {'title': '登录', 'error_name': 0, 'error_pwd': 0, 'uname': uname}
    return render(request, 'user_manage/login.html', context)

def login_handle(request):
    post = request.POST
    uname = post['username']
    upwd = post['pwd']
    remember_name = post.get('remmamber_name', 0)
    user = UserInfo.objects.filter(uname=uname)
    if(len(user) == 1):
        sha = sha1()
        sha.update(upwd.encode('utf8'))
        if(sha.hexdigest() == user[0].upwd):
            url = request.COOKIES.get('url', '/goods/index/')  # 登录成功跳转到先前的url
            red = HttpResponseRedirect(url)  # HttpResponseRedirect继承于HttpResponse.
            if(remember_name != 0):
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', uname, max_age=-1)
            request.session['user_id'] = user[0].id
            request.session['user_name'] = uname
            return red
        else:
            context = {'title': '登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd}
            return render(request, 'user_manage/login.html', context)


    else:
        context = {'title': '登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
        return render(request, 'user_manage/login.html', context)

def logout(request):
    request.session.flush()
    return redirect('/goods/index/')

@login_decorator.login
def info(request):
    goods_ids = request.COOKIES.get('goods_id', '')
    goods_ids1 = goods_ids.split(',')
    goods_list = []
    for goods_id in goods_ids1:
        try:  # 这里加个异常判断不然goods_id为空的话就会抛异常,空字符串不能转为int
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))
        except ValueError:
            pass
    uname = request.session.get('user_name', 'zhangsan')
    uemail = UserInfo.objects.get(pk=request.session['user_id']).uemail
    context = {'uname': uname, 'uemail': uemail, 'page_name': 1, 'goods_list': goods_list}
    return render(request, 'user_manage/user_center_info.html', context)

@login_decorator.login
def order(request):
    context = {'page_name': 1}
    return render(request, 'user_manage/user_center_order.html', context)

@login_decorator.login
def site(request):
    user = UserInfo.objects.filter(pk=request.session['user_id'])[0]  # 返回的是一个queryset集合，集合没有save()方法，取第一个元素即可.
    if request.method == 'POST':  # 区分超链接和POST请求，如果是超链接请求，不执行if块
        post = request.POST
        user.ureceive = post.get('receiver')
        user.uadress = post.get('address')
        user.uzipcode = post.get('zipcode')
        user.uphonenumber = post.get('phonenumber')
        user.save()
    context = {'title': '用户中心', 'user': user, 'page_name': 1}
    return render(request, 'user_manage/user_center_site.html', context)

@login_decorator.login
def user_center_order(request, pageindex):
    uid = request.session.get('user_id')
    orderinfos = OrderInfo.objects.filter(user_id=uid).order_by('oIsPay', '-oid')

    # print(type(orderinfos))
    paginator = Paginator(orderinfos, 2)
    page = paginator.page(int(pageindex))

    context = {'orderinfos': orderinfos, 'paginator': paginator, 'page': page}
    return render(request, 'user_manage/user_center_order.html', context)



