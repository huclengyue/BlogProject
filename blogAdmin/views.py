import random

from django.contrib.auth.models import User
from django.shortcuts import render


# Create your views here.

def admin_index(request):
    return render(request, 'admin/index.html')


def admin_login(request):
    if request.POST:
        username = request.get('username')
        password = request.get('password')
        user = User.objects.filter(username=username, password=password)
        if user is None:
            return '''
                    {"msg":"不存在该用户","code":-1,"success":false}
                '''
        else:
            return '''
                    {"msg":"OK","code":200,"success":True}
                '''
    else:
        context = {'random': random.randint(1, 5)}
        return render(request, 'admin/login.html', context=context)
