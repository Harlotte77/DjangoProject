from django.shortcuts import render, redirect, HttpResponse
from io import BytesIO
from userManage import models
from userManage.utils.form import LoginForm
from userManage.utils.code import check_code


def login(request):
    """登录"""
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    form = LoginForm(data=request.POST)
    if form.is_valid():
        # 此使的form.clean_data中有三个键值对：{“username”:..., "password":..., "code":...}（form.py中的LoginForm）
        # 由于clean_data要放到数据库中进行校验，而数据库中没有“code”字段，因此会报错
        # 解决方法就是使用pop()函数，在拿到“code”值的同时，也要把“code”字段删除
        # 这样再去数据库中校验就不会报错
        user_input_code = form.cleaned_data.pop("code")
        # 在session中拿到“code”的值
        # 但是“code”的值可能为空，因为设置了60秒超时，超过60秒之后，“code”的值就会为空
        code = request.session.get("image_code", "")
        if user_input_code.upper() != code.upper():
            # 验证码校验失败（错误）
            form.add_error("code", "验证码错误")
            return render(request, 'login.html', {"form": form})

        admin_obj = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_obj:
            form.add_error("password", "用户名或密码错误")
            return render(request, 'login.html', {'form': form})
        # 用户名和密码正确
        # 网站生成随即字符串，写入到用户浏览器的cookie中，再写入到session中
        request.session["info"] = {'id': admin_obj.id, 'username': admin_obj.username}
        # 用户登录成功后，可以重新设置验证码过期的时间
        # 下面的方式表示七天免登录
        request.session.set_expiry(60 * 60 * 24 * 7)

        return redirect('/admin/list')
    return render(request, 'login.html', {'form': form})


def logout(request):
    """退出登录"""
    # 清除当前用户的session
    request.session.clear()
    return redirect('/login/')


def image_code(request):
    """生成动态图片验证码"""
    image, code_string = check_code()

    # 将图片验证码上的文字内容写入到session中
    # 以便后续获取，并校验用户输入的验证码是否和图片上的一致
    request.session["image_code"] = code_string
    # 设置60秒超时，超过60秒图片验证码就会过期
    request.session.set_expiry(60)

    stream = BytesIO()
    image.save(stream, 'png')
    return HttpResponse(stream.getvalue())
