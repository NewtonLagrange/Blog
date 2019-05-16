from hashlib import sha1

from django.shortcuts import render, redirect, reverse
from blog.views import render_page
from blog import models
# from .forms import UserForm
# from .models import User


# Create your views here.
def index(request):
    papers = models.Paper.objects.all()
    return render_page(request=request, papers=papers)


def login(request):
    """ 登陆 """
    if request.method == 'GET':
        return render(request, 'Index/login.html', )

    elif request.method == 'POST':
        username = request.POST.get('username')
        pwd = request.POST.get('pwd').encode('utf8')
        s = sha1()
        s.update(pwd)
        pwd = s.hexdigest()

        names = models.User.objects.values('name')
        print(names)
        for name in names:

            if username in name['name']:
                db_pwd = models.User.objects.get(name=username).pwd

                if pwd == db_pwd:
                    request.session['username'] = username
                    return redirect(reverse('Index:index'))

        else:
            return redirect(reverse('Index:login'), {'failed': True})


def register(request):
    """ 注册 """
    if request.method == 'GET':
        return render(request, 'Index/register.html')

    elif request.method == 'POST':
        # TODO username要唯一, 加判断
        username = request.POST.get('username')
        pwd = request.POST.get('pwd').encode('utf8')
        # 加密密码
        s = sha1()
        s.update(pwd)
        pwd = s.hexdigest()
        user = models.User()
        user.name = username
        user.pwd = pwd
        user.save()
        return redirect(reverse('Index:login'))


def logout(request):
    """ 退出 """
    request.session.pop('username')
    return redirect(reverse('Index:index'))


def test(request):
    """ 测试 """
    pass
