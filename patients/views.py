from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm  
from django.views.decorators.http import require_POST
from patients.forms import PatientForm
from patients.models import Patient

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
    patients = Patient.objects.all()
    return render(request, 'dashboard.html', {'patients': patients})

def booking(request):
    return render(request, 'booking.html')

def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PatientForm()
        
    return render(request, 'add_patient.html', {'form': form})

def update_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    if request.method == 'POST':
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PatientForm(instance=patient)

    return render(request, 'add_patient.html', {'form': form})

@require_POST
def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    patient.delete()
    return redirect('dashboard')
    