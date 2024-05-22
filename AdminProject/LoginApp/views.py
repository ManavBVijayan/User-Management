from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.views.decorators.cache import cache_control
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    if 'username' in request.session:
        username = request.user.username
        return render(request, "home.html",{'username': username})
    return redirect('signin')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signin(request):
    if 'username' in request.session:
        return redirect('home')
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            request.session['username']=username
            auth.login(request,user)
            return redirect('home')
        else:
            messages.error(request,'invalid credentials')
            return redirect('/')
    return render(request,'signin.html')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def signup(request):
    # if request.user.is_authenticated:
    #     return redirect('home')
    if 'username' in request.session:
        return redirect('home')
    if request.method =="POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['password']
        cpassword = request.POST['cpassword']
        if pass1 == cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username taken')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'email already taken')
                return redirect('signup')
            else:
                myuser = User.objects.create_user(username=username,first_name=fname, last_name=lname,password=pass1, email=email)
                myuser.save()
                return redirect('signin')

        else:
            messages.info(request, 'password not matching')
            return redirect('signup')
    return render(request, 'signup.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout(request):
    if 'username' in request.session:
        request.session.flush()
    # auth.logout(request)
    return redirect('/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True, max_age=0)
def adminpanel(request):
    if request.user.is_superuser:
        if request.GET.get('search') is not None:
            search = request.GET.get('search')
            users = User.objects.filter(username__contains=search)
        else:
            users = User.objects.all()
        context = {
            'users': users
        }
        return render(request, 'adminpanel.html', context)
    else:
        return redirect('home')

@cache_control(no_cache=True, must_revalidate=True, no_store=True, max_age=0)
def updateuser(request, user_id):
    if request.user.is_superuser:
        user = User.objects.get(id=user_id)
        if request.method == 'POST':
            username = request.POST['username']
            email = request.POST['email']
            name = request.POST['name']
            password = request.POST['pass1']

            user.username = username
            user.first_name = name
            user.email = email
            user.set_password = password

            user.save()


            return redirect('adminpanel')

        return render(request, 'edit.html', {'user': user})
    else:
        return redirect('home')


@cache_control(no_cache=True, must_revalidate=True, no_store=True, max_age=0)
def delete_user(request, user_id):
    if request.user.is_superuser:
        user = User.objects.get(id=user_id)
        user.delete()
        return redirect('adminpanel')
    else:
        return redirect('home')


@cache_control(no_cache=True, must_revalidate=True, no_store=True, max_age=0)
def createuser(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            username = request.POST['username']
            name = request.POST['fname']
            lname = request.POST['lname']
            email = request.POST['email']
            password = request.POST['password']
            cpassword = request.POST['cpassword']
            if password == cpassword:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username taken')
                    return redirect('createuser')
                elif User.objects.filter(email=email).exists():
                    messages.error(request, 'email already taken')
                    return redirect('createuser')
                else:
                    myuser = User.objects.create_user(username=username, first_name=name, last_name=lname,
                                                      password=password, email=email)
                    myuser.first_name = name
                    myuser.save()
                    return redirect('adminpanel')
            else:
                messages.info(request, 'password not matching')
                return redirect('createuser')
        return render(request, 'createuser.html')
    else:
        return redirect('home')