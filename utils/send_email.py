# coding:utf-8
# author:mini_panda
import random
from account.models import EmailVerifyRecord
from django.core.mail import send_mail
from mysite.settings import EMAIL_FROM


# 随机字符串函数
def random_str(random_length=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    for i in range(random_length):  # 循环8次
        str += chars[random.randint(0, length)]  #随机字符串拼接８次
    return str


# 把随机字符串和对应的邮箱保存在数据库，并发送邮件
def send_email(email):
    email_record = EmailVerifyRecord()
    
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.save()  
    email_titile = '小熊的网站密码重置链接'
    email_body = '请点击下面的链接激活你的账号：http:127.0.0.1:8000/account/reset/{0}'.format(code)
    send_status = send_mail(subject=email_titile, message=email_body, from_email=EMAIL_FROM, recipient_list=[email])
    if send_status:
        pass
