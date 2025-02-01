
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from .models import UserProfile, CourseRule, Course


@login_required
def profile(request):
    return render(request, 'pages/profile.html')

@login_required(login_url='accounts/login/')  # Redirect to login page if not authenticated
def index(request):
    return render(request, 'pages/index.html')

@login_required
def login_view(request):
    # Replace with your actual login logic or template
    if request.user.is_authenticated:
        return redirect('index')  # Redirect to index if already authenticated
    return render(request, 'pages/login.html')

@login_required
def registercourse(request):
    return render(request, 'pages/registercourse.html')

@login_required
def register_course(request):

    return render(request, 'pages/register_course.html')




