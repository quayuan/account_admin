from django.db import models
from django.contrib.auth.models import AbstractUser
from maxcn.utils.models import BaseModel


# Create your models here.
class User(AbstractUser, BaseModel):
    # 继承后，默认的属性、方法都有
    # 扩展新属性
    server_type = models.CharField(max_length=10, unique=False)

    class Meta:
        # 表名
        db_table = 'tb_users'

    def __str__(self):
        return self.username
