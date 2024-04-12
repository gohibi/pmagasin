from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from .forms import UserForm
from .models import User
# Create your views here.

def register(request):
    if request.method == "POST":
        form = UserForm(request.POST or None)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username} , votre compte a été creé avec succès !')
            return redirect('authusers:connexion')
    else:
        form = UserForm()   
    context ={
        'form': form
    }
    return render(request,'users/register.html',context)

def connexion(request):
    if request.method == "POST":
        email =request.POST.get('email')
        password =request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user =authenticate(request,email=email,password=password)

            if user is not None:
                login(request,user)
                messages.success(request,f"Vous etes connectés")
                return redirect("core:index")
            else:
                messages.warning(request,f"Ce compte n'existe pas ! Creer un compte")
        except:
            messages.warning(request,f"cet {email} n'existe pas dans notre base")
    return render(request,'users/connexion.html')

def deconnexion(request):
    logout(request)
    messages.success(request,f"Vous etes deconnectés avec succes!")
    return redirect('core:index')

    