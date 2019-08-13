#coding=utf-8
from django.http import JsonResponse
from django.shortcuts import render, redirect
from user_manage import login_decorator
from cart_manage.models import CartInfo

@login_decorator.login
def cart(request):
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid)
    # print(gid)
    context = {'title': '购物车', 'page_name': 1, 'uid': uid, 'carts': carts}
    return render(request, 'cart_manage/cart.html', context)

@login_decorator.login
def add(request, gid, count):
    uid = request.session['user_id']
    gid = int(gid)
    carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)
    if len(carts) >= 1:  # 查询对应的只能有一条数据
        cart = carts[0]
        cart.count = cart.count + int(count)
    else:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = count
    cart.save()

    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=request.session['user_id']).count()  # count()方法计算购物车中物品数量
        return JsonResponse({'count': count})
    else:
        return redirect('/cart/')

@login_decorator.login
def edit(request, cart_id, count):  # 根据传入的商品ID和数量修改数据库中的值
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        count1 = cart.count = int(count)
        cart.save()
        data={'ok': 0}
    except Exception as e:
        data = {'ok': count1}
    return JsonResponse(data)

@login_decorator.login
def delete(request, cart_id):
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        cart.delete()
        data = {'ok': 1}
    except Exception as e:
        data = {'ok': 0}
    return JsonResponse(data)
