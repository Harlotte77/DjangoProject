from django import forms
from django.core.exceptions import ValidationError
from userManage.utils.bootstrap import BootStrapModelForm, BootStrapForm
from userManage import models
from userManage.utils.encrypt import md5


class UserModelForm(BootStrapModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'age', 'gender', 'salary', 'create_time', 'user_depart']
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '姓名'}),
        #     'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密码'}),
        #     'age': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '年龄'}),
        #     'gender': forms.Select(attrs={'class': 'form-control', 'placeholder': '性别'}),
        #     'salary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '薪资'}),
        #     'create_time': forms.DateInput(attrs={'class': 'form-control', 'placeholder': '入职时间'}),
        #     'user_depart': forms.Select(attrs={'class': 'form-control', 'placeholder': '所在部门'}),
        # }


class PretyModelForm(BootStrapModelForm):
    # 验证手机号格式的方式1:
    # 使用正则表达式
    # mobile = forms.CharField(
    #     label='手机号',
    #     validators=[RegexValidator(r'^1【3-9】\d{9}$', '手机号必须是11位数字')]
    # )

    class Meta:
        model = models.PrettyNum
        fields = "__all__"  # 所有字段
        # fields = ['mobile', 'price', 'level', 'status']    # 自定义字段
        # exclude = ["level"]  # 排除哪个字段（排除‘level’字段）

    # 验证手机号格式的方式2:
    # 使用钩子函数
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        # 检查手机号是否已存在
        # 存在返回True, 不存在返回False
        obj = models.PrettyNum.objects.filter(mobile=txt_mobile).exists()
        if obj:
            raise ValidationError("手机号已存在")

        if len(txt_mobile) != 11:
            # 验证不通过
            raise ValidationError("手机号格式错误")
        # 验证通过
        # 验证通过返回txt_mobile，那么form.save()保存到数据库中的就是txt_mobile的值
        # 返回什么就保存什么
        return txt_mobile


class PrettyEditModelForm(BootStrapModelForm):
    """
    编辑靓号
    只允许修改价格、级别和状态
    不允许修改手机号， 手机号会显示在界面上，但是是锁定的（disabled=True）
    """
    mobile = forms.CharField(disabled=True, label="手机号")

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']


class AdminModelForm(BootStrapModelForm):
    # render_value=True的作用是不清空输入框
    # 如果密码验证不通过也不会清空界面上的输入框
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = "__all__"
        widgets = {
            'password': forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)

    # 钩子函数，验证两次输入的密码是否一致
    def clean_confirm_password(self):
        confirm = self.cleaned_data.get('confirm_password')
        password = self.cleaned_data.get('password')
        if password != md5(confirm):
            raise ValidationError('两次密码输入不一致')
        else:
            # 如果密码验证通过，则返回confirm，那么form.save()保存到数据库中的就是confirm的值
            # 返回什么就保存什么
            return confirm


class AdminEditModelForm(BootStrapModelForm):
    class Meta:
        model = models.Admin
        # 只允许编辑用户名，不能编辑密码
        # 编辑(重置)密码部分在AdminResetModelForm中
        fields = ['username']


class AdminResetModelForm(BootStrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput(render_value=True)
    )

    class Meta:
        model = models.Admin
        fields = ['password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True)
        }

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        md5_pwd = md5(pwd)
        # 校验新输入的密码是否与旧密码一致
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd)
        if exists:
            raise ValidationError("不能与当前密码一致")
        return md5_pwd

    # 钩子函数，验证两次输入的密码是否一致
    def clean_confirm_password(self):
        confirm = self.cleaned_data.get('confirm_password')
        password = self.cleaned_data.get('password')
        if password != md5(confirm):
            raise ValidationError('两次密码输入不一致')
        else:
            # 如果密码验证通过，则返回confirm，那么form.save()保存到数据库中的就是confirm的值
            # 返回什么就保存什么
            return confirm


class LoginForm(BootStrapForm):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '用户名'}),
        required=True
    )

    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密码'}, render_value=True),
        required=True
    )

    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput(),
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        md5_pwd = md5(pwd)
        return md5_pwd


class TaskModelForm(BootStrapModelForm):
    class Meta:
        model = models.Task
        fields = "__all__"


class OrderModelForm(BootStrapModelForm):
    class Meta:
        model = models.Order
        exclude = ['order_id', 'admin']


class UploadForm(BootStrapForm):
    bootstrap_exclude_fields = ['file']
    name = forms.CharField(label="姓名")
    age = forms.IntegerField(label="年龄")
    file = forms.FileField(label="文件")


class UploadModalForm(BootStrapModelForm):
    bootstrap_exclude_fields = ["file"]
    class Meta:
        model = models.UploadInfo_ModalForm
        fields = "__all__"
