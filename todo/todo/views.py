from django . shortcuts import render, redirect
from django.contrib.auth.models import User
from todo import models
from todo.models import TODOO
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        fnm = request.POST.get('fnm')
        emailid = request.POST.get('email')
        pwd = request.POST.get('pwd')
        my_user = User.objects.create_user(fnm, emailid, pwd)
        my_user.save()
        return redirect('/loginn')
    return render(request, 'signup.html')


def loginn(request):
    if request.method =='POST':
        fnm = request.POST.get('fnm')
        pwd = request.POST.get('pwd')
        userr = authenticate(request, username=fnm, password=pwd)
        if userr is not None:
            login(request, userr)
            return redirect('/todopage')
        else:
            return redirect('loginn')

    return render(request, 'loginn.html')



@login_required(login_url='/loginn')
def todo(request):
    if request.method =='POST':
        title = request.POST.get('title')
        obj = models.TODOO(title = title, user = request.user)
        obj.save()
        user = request.user
        res = models.TODOO.objects.filter(user= request.user).order_by('-date')
        return redirect('/todopage', {'res':res})

    res = models.TODOO.objects.filter(user = request.user).order_by('-date')
    return render(request, 'todo.html', {'res':res})



@login_required(login_url='/loginn')
def edit_todo(request, srno):
    if request.method == 'POST':
        title = request.POST.get('title')
        print(title)
        obj = models.TODOO.objects.get(srno=srno)
        obj.title = title
        obj.save()
        return redirect('/todopage')

    obj = models.TODOO.objects.get(srno=srno)
    return render(request, 'edit_todo.html', {'obj': obj})



@login_required(login_url='/loginn')
def delete_todo(request, srno):
    obj = models.TODOO.objects.get(srno=srno)
    obj.delete()
    return redirect('/todopage')


def signout(request):
    logout(request)
    return redirect('/loginn')