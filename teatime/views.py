from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms 

from .models import Profile, Tea
from .forms import TeaForm, SignUpForm

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        form = TeaForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                tea = form.save(commit=False)
                tea.user = request.user
                tea.save()
                messages.success(request, ("Your Tea has been posted!"))
                return redirect('home')

        teas = Tea.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"teas": teas, "form": form})
    else:
        teas = Tea.objects.all().order_by("-created_at")
        return render(request, 'home.html', {"teas": teas})


def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user)
        return render(request, 'profile_list.html', {"profiles": profiles})
    else:
        messages.success(request, ("You must be logged in to view this page..."))
        return redirect('home')
    
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        teas = Tea.objects.filter(user_id=pk).order_by("-created_at")

        # POST form logic
        if request.method == "POST":
            # get current user
            current_user_profile = request.user.profile
            # get form data
            action = request.POST['follow']
            #  logic to decide follow or unfollow
            if action == "unfollow":
                current_user_profile.follows.remove(profile)
            elif action == "follow":
                current_user_profile.follows.add(profile)
            # save profile
            current_user_profile.save()

        return render(request, "profile.html", {"profile": profile, "teas": teas})
    else:
        messages.success(request, ("You must be logged in to view this page..."))
        return redirect('home')

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in!"))
            return redirect('home')
        else:
            messages.success(request, ("There was an error logging in. Please try again."))
            return redirect('login')
    else:
        return render(request, "login.html", {})
    
def logout_user(request):
    logout(request)
    messages.success(request, ("You have been logged out."))
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            # first_name = form.cleaned_data['first_name']
            # last_name = form.cleaned_data['last_name']
            # email = form.cleaned_data['email']

            # log in user
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have successfully registered!"))
            return redirect('home')
    
    return render(request, "register.html", {'form': form})

def update_user(request):
    if request.user.is_authenticated:
        return render(request, "update_user.html", {})
    else:
        messages.success(request, ("You must be logged in to view that page"))
        return redirect('home')
