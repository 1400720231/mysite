from django.shortcuts import render, HttpResponseRedirect, reverse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
# Create your views here.

# 登录视图
def user_login(request):
    if request.method == 'GET':
        login_form = LoginForm()
        context = {"form": login_form}
        return render(request, "login.html",context=context)
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
                else:
                    return render(request, "login.html")
        else:
            return render(request, "login.html", {'form': form})

# 登出视图
def user_logout(request):
    logout(request)  # 登出
    # 登出后重定向到index页面
    return HttpResponseRedirect(reverse('blog:blog_title'))


def user_register(request):
    pass