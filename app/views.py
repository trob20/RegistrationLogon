from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):
    return render(request, "index.html")


def create(request):
    if(request.method=="POST"): 
        errors = User.objects.validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")

        password = request.POST["password"]
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        print(pw_hash)
        
        user = User.objects.create(
            first_name=request.POST["first_name"],
            last_name=request.POST["last_name"],
            birthdate=request.POST["birthdate"],
            email=request.POST["email"],
            password=pw_hash
        )
        request.session["userId"] = user.id
        
        context = {
            'first_name': user.first_name
        }
        return render(request, "success.html", context)

        return redirect ("/")

    return redirect ("/")


def login(request):
    if(request.method=="POST"): 
        email = request.POST["email"]
        password = request.POST["password"]

        userSearch = User.objects.filter(email=email)
        if not userSearch:
            messages.error(request, "Invalid credentials")
            return redirect ("/")

        user = userSearch[0]

        if bcrypt.checkpw(password.encode(), user.password.encode()):
            request.session["userId"] = user.id
            request.session["first_name"] = user.first_name
            return redirect("/success")
        else:
            messages.error(request, "Invalid credentials")
            return redirect ("/")
    return redirect ("/")

def success(request):
    sessionTest = request.session.get('userId', 'no userId')
    if sessionTest == 'no userId': 
        return redirect ("/")
    context = {
        'first_name': request.session['first_name'],
    }
    return render(request, "success.html", context)

def logout(request):
    if(request.method=="POST"): 
        del request.session["userId"]
        del request.session["first_name"]
    return redirect ("/")
