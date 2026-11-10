from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm  

# Create your views here.
def index(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST) # Form with the details of the form
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'index.html', {'form': form})

def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username') 
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def profile(request):
    return render(request, 'profile.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def booking(request):
    return render(request, 'booking.html')