from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Profile

# Create your views here.
def home(request):
    return render(request, 'home.html', {})

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

        return render(request, "profile.html", {"profile": profile})
    else:
        messages.success(request, ("You must be logged in to view this page..."))
        return redirect('home')
