from django.core import paginator
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

from cart_manage.models import CartInfo
from goods_manage.models import TypeInfo, GoodsInfo

def index(request):
    # 这里只查询前两种分类的最新和最热门的4条数据.另外几种分类原理相同
    typelist = TypeInfo.objects.all()
    print(type(typelist[0]))
    t1_id = typelist[0].goodsinfo_set.order_by('-id')[0:4]
    t1_click = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]
    t2_id = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    t2_click = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
    context = {'guest_cart': 1, 'title': '首页',
               't1_id': t1_id, 't1_click': t1_click,
               't2_id': t2_id, 't2_click': t2_click,
               }
    return render(request, 'goods_manage/index.html', context)

def detail(request, id):
    goods = GoodsInfo.objects.filter(pk=int(id))[0]
    goods.gclick += 1
    goods.save()
    # print(type(goods.id)) # goods.id是int
    # print(goods)
    new = goods.gtype.goodsinfo_set.order_by('-id')[0:2]  # GoodsInfo.objects.filter(pk=int(id))[0].gtype = TypeInfo.objects.all()[0]
    # print(new)
    if 'user_id' in request.session:   # 如果没有登录购物车商品数为0
        count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
    else:
        count = 0
    context = {'guest_cart': 1, 'goods': goods, 'new': new, 'count': count}
    res = render(request, 'goods_manage/detail.html', context)


    goods_ids = request.COOKIES.get('goods_id', '')
    goods_id = '%d' % goods.id
    if goods_ids != '':
        goods_ids1 = goods_ids.split(',')  # 拆分成一个列表
        if goods_ids1.count(goods_id) >= 1:  # 判断列表中元素数量,重复的移除
            goods_ids1.remove(goods_id)
        else:
            goods_ids1.insert(0, goods_id)
        if len(goods_ids1) > 5:  # 只保存5个数据，删除第6个
            del goods_ids1[5]
        goods_ids = ','.join(goods_ids1)  # 重新拼接成字符串
    else:
        goods_ids = goods_id  # 如果goods_ids为空就直接添加
    res.set_cookie('goods_id', goods_ids)  # 将goods_ids添加到cookie中
    return res


def list(request, typeid, ordertype, pageindex):

    typeinfo = TypeInfo.objects.get(pk=int(typeid))
    new = typeinfo.goodsinfo_set.order_by('-id')[0:2] # 最新的两个
    if ordertype == '1': # 1表示最新
        goodslist = GoodsInfo.objects.filter(gtype_id=int(typeid)).order_by('-id')
    elif ordertype == '2': # 2表示价格
        goodslist = GoodsInfo.objects.filter(gtype_id=int(typeid)).order_by('-gprice')
    elif ordertype == '3':  # 3表示人气(点击量)
        goodslist = GoodsInfo.objects.filter(gtype_id=int(typeid)).order_by('-gclick')
    paginator = Paginator(goodslist, 4)
    page = paginator.page(int(pageindex))
    context = {'guest_cart': 1, 'paginator': paginator, 'page': page, 'new': new,
               'ordertype': ordertype, 'typeinfo': typeinfo,
               }
    return render(request, 'goods_manage/list.html', context)