from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm, RsgistrationForm,UserProfileForm,ModifyPwdForm
from .forms import EmailForm
from .models import EmailVerifyRecord
from django.contrib.auth.hashers import make_password
# 发送邮件重置密码
from utils.send_email import send_email
from datetime import datetime

# Create your views here.

# 登录视图
def user_login(request):
    if request.method == 'GET':
        login_form = LoginForm()
        context = {"form": login_form}
        return render(request, "account/login.html",context=context)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:  # 是否激活，激活才让登录
                    login(request, user)
                    # 如果这里用render的话 意思就是把此时view中的数据render到index.html页面，
                    # 会导致看不到其他view在index.html render的数据，所以我们直接重定向过去就可以了，不用render传信息
                    return HttpResponseRedirect(reverse('blog:blog_title'))
                    # return HttpResponse("账户未激活，请激活或再重新登录")
                else:
                    return HttpResponse("账户未激活，请激活或再重新登录")
        
        return HttpResponse("账户密码错误，重新登录")


# 登出视图
def user_logout(request):
    logout(request)  # 登出
    # 登出后重定向到index页面
    return HttpResponseRedirect(reverse('blog:blog_title'))

"""
注册视图函数一
def register(request):
    if request.method == "POST":
        user_form = RsgistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            return HttpResponse("successful")
        else:
            return HttpResponse("sorry, 填入的信息有误，请重新输入再次注册")
    else:
        user_form = RsgistrationForm()
        return render(request, "account/register.html", {"form":user_form})

"""
"""
注册视图函数二 增加了userprofile model后的重写注册视图函数一
"""
def register(request):
    if request.method == "POST":
        user_form = RsgistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        if user_form.is_valid() * userprofile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            return HttpResponse("successful")
        else:
            return HttpResponse("sorry , you can not register !")
    else:
        user_form = RsgistrationForm()
        userprofile_form = UserProfileForm()
        return render(request, "account/register.html",{"form":user_form,"profile":userprofile_form})


# 修改或者重置密码
def modify_password(request):
    modify_form = ModifyPwdForm(request.POST)
    if request.method == "POST":
        user = request.user
        
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1')
            pwd2 = request.POST.get('password2')
            if pwd1 != pwd2:
                return render(request, 'account/modify_password.html', {'mes': '密码不一致','modify_form': modify_form})
            else:
                # 注意这里的make_password函数，吧明文编码成hash的密文
                user.password = make_password(pwd2)
                user.save()
                return HttpResponseRedirect(reverse('account:user_login'))
    else:
        return render(request, 'account/modify_password.html', {'mes': '','modify_form': modify_form})

# 发送密码

def send_reset_password(request):
    if request.method == "GET":
        form = EmailForm()
        context = {"form":form}
        return render(request, 'account/send_email.html',context=context)
        
    else:
        email = request.POST.get("email", '')
        if email:

            send_email(email)
            return HttpResponse("验证码已经发送，查收")
        else:
            return HttpResponse("请输入正确的邮箱")

# 重置密码
def password_reset(request,code):
    form = ModifyPwdForm()
    context = {}
    code = EmailVerifyRecord.objects.filter(code=code)
    if code:
        send_time = code[0].send_time
        time_now = datetime.now()
        delta_time  = time_now - send_time
        # 验证码5分钟过期
        if delta_time.seconds < 60*5:
            context = {"form":form}
    if request.method == "GET":
        if context:
        # return render(request, "account/reset_password.html",context=context)
            return render(request, "account/reset_password.html", context=context)
        else:
            return HttpResponse("验证码时间过期，请重新获取验证码")

    if request.method == 'POST':
        path = request.path[15:]
        code = path[:-1]
        code = EmailVerifyRecord.objects.filter(code=code)
        email = code[0].email
        if form.is_valid():
            pwd1 = request.POST.get('password1')
            pwd2 = request.POST.get('password2')
            if pwd1 != pwd2:
                return render(request, 'account/reset_password.html', {'mes': '密码不一致','form':  form})
            else:
                user = User.objects.filter(email=email)
                # 注意这里的make_password函数，吧明文编码成hash的密文
                user.password = make_password(pwd2)
                user.save()
                return HttpResponseRedirect(reverse('account:user_login'))

def page_not_found(request):
    """
    全局404处理函数, 404 表示NOT FOUND，访问不存在的地址的时候的状态
    """
    from django.shortcuts import render_to_response
    response = render_to_response('404.html')
    response.status_code = 404
    return response


def page_error(request):
    """
    全局500处理函数， 500表示error，一般是view函数错误的时候
    """
    from django.shortcuts import render_to_response
    response = render_to_response('500.html')
    response.status_code = 500
    return response