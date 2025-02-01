
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect




@login_required(login_url='accounts/login/')  # Redirect to login page if not authenticated
def index(request):
    return render(request, 'pages/index.html')

@login_required
def login_view(request):
    # Replace with your actual login logic or template
    if request.user.is_authenticated:
        return redirect('index')  # Redirect to index if already authenticated
    return render(request, 'pages/login.html')





