from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 排除那些不需要登录就能访问的页面
        if request.path_info in ["/login/", "/image/code/"]:
            return
        # 读取当前访问的用户的session信息
        # 如果能读到，则说明已经登录过，可以继续后续的步骤
        info_dict = request.session.get("info")
        if info_dict:
            return

        # 如果没有登录过，则重新定向到登录页面
        return redirect('/login/')
