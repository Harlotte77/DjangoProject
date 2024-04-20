"""
URL configuration for DjangoProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from django.conf import settings
from userManage.views import user, department, prettynum, admin, account, task, order, chart, upload

urlpatterns = [
    # path('admin/', admin.site.urls),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

    # 部门管理
    path('depart/list/', department.depart_list),
    path('depart/add/', department.depart_add),
    path('depart/delete/', department.depart_delete),
    # 批量上传
    path('depart/multi/', department.depart_multi),
    # 'depart/<int:id>/edit/':
    # 这是一个 URL 路径模式，其中包含了一个动态参数 <int:id>，
    # 表示匹配一个整数类型的参数，并将其传递给视图函数。
    # 当访问类似 /depart/1/edit/ 这样的路径时，
    # Django 将调用 depart_edit 视图函数来处理该请求，并将路径中的整数参数传递给视图函数。
    path('depart/<int:id>/edit/', department.depart_edit),

    #################################
    # 员工管理
    path('user/list/', user.user_list),
    path('user/add/', user.user_add),
    path('user/add/ModelForm/', user.user_add_ModelForm),
    path('user/<int:user_id>/edit/', user.user_edit),
    path('user/<int:user_id>/delete/', user.user_delete),

    #################################
    # 靓号管理
    path('prettynum/list/', prettynum.prettynum_list),
    path('prettynum/add/', prettynum.prettynum_add),
    path('prettynum/<int:pretty_id>/edit/', prettynum.prettynum_edit),
    path('prettynum/<int:pretty_id>/delete/', prettynum.prettynum_delete),

    #################################
    # 管理员管理
    path('admin/list/', admin.admin_list),
    path('admin/add/ModelForm/', admin.admin_add_ModelForm),
    path('admin/<int:admin_id>/edit/', admin.admin_edit),
    path('admin/<int:admin_id>/delete/', admin.admin_delete),
    path('admin/<int:admin_id>/reset/', admin.admin_reset),

    #################################
    # 登录和登出
    path('login/', account.login),
    path('logout/', account.logout),

    #################################
    # 验证码
    path('image/code/', account.image_code),

    #################################
    # 任务管理
    # 基于Ajax
    path('task/list/', task.task_list),
    path('task/add/', task.task_add),

    #################################
    # 订单管理
    # 基于Ajax
    path('order/list/', order.order_list),
    path('order/add/', order.order_add),
    path('order/delete/', order.order_delete),
    path('order/detail/', order.order_detail),
    path('order/edit/', order.order_edit),

    #################################
    # 数据统计
    path('data/statistics/', chart.data_statistics),
    path('data/bar/', chart.data_bar),

    #################################
    # 文件上传
    path('upload/form/', upload.upload_form),
    path('upload/modalform/', upload.upload_modalform),
    path('upload/list/', upload.upload_list),
    path('upload/add/', upload.upload_add),

]
