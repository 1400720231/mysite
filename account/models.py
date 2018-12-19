from django.db import models
from django.contrib.auth.models import User



# 账号密码重置的model
class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20, verbose_name='验证码')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    send_time = models.DateTimeField(verbose_name="发送时间", auto_now_add=True)  # 自动生时间戳

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}{1}'.format(self.code, self.email)

class UserProfile(models.Model):    
    user = models.OneToOneField(User, unique=True)   
    birth = models.DateField(blank=True, null=True)
    phone = models.CharField(max_length=20, null=True)
    
    def __str__(self):
        return 'user {}'.format(self.user.username)


class UserInfo(models.Model):
    user = models.OneToOneField(User, unique=True)
    school = models.CharField(max_length=97, blank=True)
    company = models.CharField(max_length=97, blank=True)
    profession = models.CharField(max_length=27, blank=True)
    address = models.CharField(max_length=177, blank=True)
    aboutme = models.TextField(blank=True)  
    photo = models.ImageField(blank=True)

    def __str__(self):
        return "user:{}".format(self.user.username)


