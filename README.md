# dailyfresh
天天生鲜：小型电商购物网站，基于Python3.4和Django1.8

项目尽量使用Django内部提供的API，后台管理为Django自带的管理系统django-admin。

功能简介：
商品浏览：商品的图片，售价，种类，简介以及库存等信息。
登录注册：用户的登录与注册。
用户中心：支持用户个人信息，收货地址等信息的更新，商品加入购物车，订单生成。
商品下单：在支付接口和企业资质的支持下可完成商品的下单功能，按照原子事务处理，下单异常则终止此次下单过程。
后台管理：支持后台管理功能，商品及用户信息的增加，更新与删除，可自定制样式与功能，日志，以及权限的管理和分配。
