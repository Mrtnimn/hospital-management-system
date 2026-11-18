from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm  
from django.core.checks import messages
from patients.forms import PatientForm
from patients.models import Patient, Payment
from patients.serializers import PatientSerializer 
from rest_framework import viewsets
from rest_framework.permissions import AllowAny 
from django_daraja.mpesa.core import MpesaClient

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

def delete_patient(request, patient_id):
    if request.method == 'POST':
        patient = get_object_or_404(Patient, id=patient_id)
        patient.delete()
    
    return redirect('dashboard')
    
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_class = [AllowAny]
    
def make_payment(request):
    if request.method == 'POST':
        patient_name = request.POST.get('patient_name')
        phone_number = request.POST.get('phone_number')
        amount = int(request.POST.get('amount'))
        
        # Create a new payment object
        payment = Payment.objects.create(
            patient_name = patient_name,
            phone_number = phone_number,
            amount = amount
        )
        
        cl = MpesaClient()
        account_reference = "Hospital Payment"
        transaction_desc = "Payment for hospital services"
        callback_url = "https://darajambili.herokuapp.com/express-payment"
        response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
        payment.transaction_id = response['CheckoutResponseID']
        payment.save()
        messages.success(request, f"STK Push sent. Please complete the payment on your phone.")
        
        return redirect('dashboard')
    
    return render(request, 'make_payment.html')