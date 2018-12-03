from django import forms
from django.contrib.auth.models import User



# 登录表单
class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5,widget=forms.PasswordInput)


# 注册表单
class RegisterForm(forms.Form):
	email = forms.EmailField(required=True)
	password = forms.CharField(required=True, min_length=5)



class RsgistrationForm(forms.ModelForm):
	password = forms.CharField(label="Password",widget=forms.PasswordInput)
	password2 = forms.CharField(label="Password", widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ("username", "email")

	"""
	以clean_+"属性名称"创建的函数，在执行.is_valid()的时候就会自动执行
	这里的clean_password2就是为了检验两次输入的密码是否正确，我以前写是在view函数中
	取出来判断的，这样写感觉舒服一点。。
	"""
	def clean_password2(self):
		cd = self.cleaned_data
		if cd["password"] != cd["password2"]:
			raise forms.ValidationError("passwords do not match !")
		return cd["password2"]