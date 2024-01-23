from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms 
from django.contrib.auth.models import User

from .models import Profile, Tea
from .forms import TeaForm, SignUpForm, ProfilePicForm

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
    
def followers(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'followers.html', {"profiles": profiles})
        else:
            messages.success(request, ("Not your profile list..."))
            return redirect('home')
    else:
        messages.success(request, ("You must be logged in to view this page..."))
        return redirect('home')
    
def follows(request, pk):
    if request.user.is_authenticated:
        if request.user.id == pk:
            profiles = Profile.objects.get(user_id=pk)
            return render(request, 'follows.html', {"profiles": profiles})
        else:
            messages.success(request, ("Not your profile list..."))
            return redirect('home')
    else:
        messages.success(request, ("You must be logged in to view this page..."))
        return redirect('home')
    
def follow(request, pk):
    if request.user.is_authenticated:
        #  get profile to follow
        profile = Profile.objects.get(user_id=pk)
        # follow user
        request.user.profile.follows.add(profile)
        # save updated profile
        request.user.profile.save()
        # return message
        messages.success(request, (f"You have successfully followed {profile.user.username}"))
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, ("You must be logged in to view this page..."))
        return redirect('home')

def unfollow(request, pk):
    if request.user.is_authenticated:
        #  get profile to unfollow
        profile = Profile.objects.get(user_id=pk)
        # unfollow user
        request.user.profile.follows.remove(profile)
        # save updated profile
        request.user.profile.save()
        # return message
        messages.success(request, (f"You have successfully unfollowed {profile.user.username}"))
        return redirect(request.META.get("HTTP_REFERER"))
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
        current_user = User.objects.get(id=request.user.id)
        profile_user = Profile.objects.get(user__id=request.user.id)

        # get forms
        user_form = SignUpForm(request.POST or None, request.FILES or None, instance=current_user)
        profile_form = ProfilePicForm(request.POST or None, request.FILES or None, instance=profile_user)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            # django logs you out after update, re login
            login(request, current_user)
            messages.success(request, ("Your profile has been updated!"))
            return redirect('home')
        return render(request, "update_user.html", {'user_form': user_form, 'profile_form': profile_form })
    else:
        messages.success(request, ("You must be logged in to view that page"))
        return redirect('home')

def tea_like(request, pk):
    if request.user.is_authenticated:
        tea = get_object_or_404(Tea, id=pk)
        if tea.likes.filter(id=request.user.id):
            tea.likes.remove(request.user)
        else:
            tea.likes.add(request.user)
        
        return redirect(request.META.get("HTTP_REFERER"))

    else:
        messages.success(request, ("You must be logged in to view that page"))
        return redirect('home')
    
def tea_show(request, pk):
    tea = get_object_or_404(Tea, id=pk)

    if tea:
        return render(request, "show_tea.html", {"tea": tea})
    else:
        messages.success(request, ("Post does not exist"))
        return redirect('home')
    
def delete_tea(request, pk):
    if request.user.is_authenticated:
        tea = get_object_or_404(Tea, id=pk)
    else:
        messages.success(request, ("Please log in to continue"))
        return redirect(request.META.get("HTTP_REFERER"))
    