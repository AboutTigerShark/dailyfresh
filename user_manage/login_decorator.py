from django.http import HttpResponseRedirect

# 用于需要登录才能访问的页面的装饰器
def login(func):
    def login_dec(request, *args, **kwargs):
        if 'user_id' in request.session:  # 不支持request.session.has_key()方法
            return func(request, *args, **kwargs)
        else:
            red = HttpResponseRedirect('/user/login/')
            red.set_cookie('url', request.get_full_path())  # 保存完整路径,登录完可跳转回原页面
            return red
    return login_dec


