from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class UserType:
    # TODO BUG 数字不一致。。
    Customer = 1
    Manager = 2
    Chef = 3
    Waiter = 4

    UserTypeChoices = (
        (0, '顾客'),
        (1, '管理员'),
        (2, '厨师'),
        (3, '服务员'),
    )

    @staticmethod
    def user_type(type_id):
        return (
            '顾客',
            '管理员',
            '厨师',
            '服务员'
        )[type_id]


# Create your models here.


class User(AbstractUser):
    """
    用户类
    """
    phone_number = models.CharField(max_length=11, verbose_name="用户手机号码", unique=True, null=True)

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="用户创建时间")

    user_type = models.IntegerField(default=UserType.Customer, choices=UserType.UserTypeChoices, verbose_name="用户类型")

    def __str__(self):
        description = "{}".format(self.username)
        return description

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class CodeType:
    register = 0
    login = 1
    resetpwd = 2

    CodeTypeChoice = (
        (0, '注册'),
        (1, '登录'),
        (2, '修改密码'),
    )

    @staticmethod
    def code_type(type_id):
        return (
            '注册',
            '登录',
            '修改密码'
        )[type_id]

class VerifyCode(models.Model):
    """
    短信验证码
    """
    code = models.CharField(max_length=10, verbose_name="验证码")
    phone_number = models.CharField(max_length=11, verbose_name="电话")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    purpose = models.IntegerField(default=CodeType.register, choices=CodeType.CodeTypeChoice, verbose_name='验证码的用途')

    class Meta:
        verbose_name = "短信验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
