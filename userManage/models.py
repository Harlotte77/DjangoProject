from django.db import models


# Create your models here.

class Admin(models.Model):
    """管理员"""
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)

    def __str__(self):
        return self.username


class Department(models.Model):
    """部门表"""
    department_title = models.CharField(verbose_name='部门名字', max_length=32)

    def __str__(self):
        return self.department_title


class UserInfo(models.Model):
    """员工表"""
    name = models.CharField(verbose_name='姓名', max_length=16)
    password = models.CharField(verbose_name='密码', max_length=64)
    age = models.IntegerField(verbose_name='年龄')
    salary = models.DecimalField(verbose_name='薪资', max_digits=10, decimal_places=2, default=0)
    create_time = models.DateField(verbose_name='入职时间')

    # 定义一个外键字段 user_depart，用于关联到 Department 模型的 id 字段，
    # 当关联的部门对象被删除时，与之关联的用户对象也会被删除。
    user_depart = models.ForeignKey(verbose_name='所在部门', to='Department', to_field='id', on_delete=models.CASCADE)

    # 定义一个外键字段 user_depart，用于关联到 Department 模型的 id 字段，
    # 允许存储空值，可以在表单中为空，当关联的部门对象被删除时，
    # 与之关联的用户对象的 user_depart 字段会被设置为 NULL
    # user_depart = models.ForeignKey(to='Department', to_field='id', null=True, blank=True, on_delete=models.SET_NULL)

    # 第一个元素是存储在数据库中的值，第二个元素是在界面上显示的文本。
    gender_choice = (
        (1, '男'),
        (2, '女'),
    )
    # 定义一个小整数字段 gender，用于存储员工的性别信息，只能选择预定义的男或女选项
    gender = models.SmallIntegerField(verbose_name='性别', choices=gender_choice)


class PrettyNum(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name="手机号", max_length=11)
    price = models.DecimalField(verbose_name="月租", max_digits=10, decimal_places=2)
    level_choices = (
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)
    status_choices = (
        (1, '未占用'),
        (2, '已占用'),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)


class Task(models.Model):
    """任务表"""
    title = models.CharField(verbose_name="标题", max_length=64)
    detail = models.TextField(verbose_name="任务详细信息")
    level_choice = (
        (1, '紧急'),
        (2, '重要'),
        (3, '次要'),
    )

    level = models.SmallIntegerField(verbose_name="任务级别", choices=level_choice, default=2)
    user = models.ForeignKey(verbose_name="任务负责人", to="Admin", on_delete=models.CASCADE, to_field="id")


class Order(models.Model):
    """订单表"""
    order_id = models.CharField(verbose_name="订单号", max_length=64)
    order_name = models.CharField(verbose_name="订单名称", max_length=32)
    price = models.DecimalField(verbose_name="价格", max_digits=10, decimal_places=2)
    status_choice = (
        (0, "待支付"),
        (1, "已支付"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choice)
    admin = models.ForeignKey(verbose_name="管理员", to="Admin", on_delete=models.CASCADE)


class UploadInfo_Form(models.Model):
    """用户上传的信息表(基于Form)"""
    name = models.CharField(verbose_name="姓名", max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    file = models.CharField(verbose_name="上传的文件", max_length=128)


class UploadInfo_ModalForm(models.Model):
    """用户上传的信息表(基于ModalForm)"""
    name = models.CharField(verbose_name="姓名", max_length=32)
    age = models.IntegerField(verbose_name="年龄")
    # 本质上数据库也是CharField，但是可以自动保存数据
    file = models.FileField(verbose_name="上传的文件", max_length=128)