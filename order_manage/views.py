from datetime import datetime
from decimal import Decimal

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
from cart_manage.models import CartInfo
from order_manage.models import OrderInfo, OrderDetailInfo
from user_manage import login_decorator
from user_manage.models import UserInfo


@login_decorator.login
def order(request):
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid)
    user = UserInfo.objects.filter(id=uid)[0]
    # carts = request.GET.get('cart_id')
    context = {'title': '提交订单', 'page_name': 1, 'carts': carts, 'user': user}
    return render(request, 'order_manage/place_order.html', context)

@transaction.atomic()
@login_decorator.login
def order_handle(request):
    tran_id = transaction.savepoint()
    cart_ids = request.POST.getlist('cart_ids[]')
    print(cart_ids)
    try:
        order = OrderInfo()
        now = datetime.now()
        uid = request.session['user_id']
        print(uid)
        order.oid = '%s%d' % (now.strftime('%Y%m%d%H%M%S'), uid)
        order.user_id = uid
        order.odate = now
        order.ototal = Decimal(request.POST['total'].replace('元', ''))
        order.save()

        # cart_ids1 = [int(item) for item in cart_ids]
        for id1 in cart_ids:
            detail = OrderDetailInfo()
            detail.order = order

            cart = CartInfo.objects.get(id=id1)

            goods = cart.goods
            if goods.gkucun >= cart.count:
                # 更新库存
                goods.gkucun = cart.goods.gkucun-cart.count
                goods.save()
                # 保存订单详细信息
                detail.goods_id = goods.id
                detail.price = goods.gprice
                detail.count = cart.count
                detail.save()
                # 删除购物车
                cart.delete()
            else:
                transaction.savepoint_rollback(tran_id)
                return JsonResponse({'data': 2})  # 创建订单失败
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print(e)
        transaction.savepoint_rollback(tran_id)

    return JsonResponse({'data': 1}) # 创建订单成功