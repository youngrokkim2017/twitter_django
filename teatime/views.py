from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Profile, Tea
from .forms import TeaForm

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
