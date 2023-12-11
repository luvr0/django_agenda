from django.contrib.auth.forms import AuthenticationForm
from contact.views import RegisterForm, RegisterUpdate
from django.shortcuts import render, redirect
from django.contrib import auth


def register(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('contact:login')


    return render(
        request,
        'contact/register.html',
        {
            'form': form
        }
    )

def user_update(request):
    form = RegisterUpdate(instance=request.user)
    
    if request.method != 'POST':
        return render(
            request,
            'contact/register.html',
            {
                'form': form
            }
        )
    
    form = RegisterUpdate(data=request.POST, instance=request.user)

    if not form.is_valid():
        return render(
            request,
            'contact/register.html',
            {
                'form': form
            }
        )
    
    form.save()
    return redirect('contact:user_update')

def user_login(request):
    form = AuthenticationForm(request)

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth.login(request, user)
            return redirect('contact:index')


    return render(
        request,
        'contact/login.html',
        {
            'form': form
        }
    )

def user_logout(request):
    auth.logout(request)
    return redirect('contact:login')