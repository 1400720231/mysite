from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RsgistrationForm,UserProfileForm
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
        else:
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