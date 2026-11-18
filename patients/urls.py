"""
URL configuration for hospital project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from patients import views
# from django.contrib.auth.views import LogoutView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('patients', views.PatientViewSet, basename = 'patient')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name = 'index'),
    path('login/', views.userlogin, name = 'login'),
    path('profile/', views.profile, name = 'profile'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('booking/', views.booking, name = 'booking'),
    path('addpatient/', views.add_patient, name = 'addpatient'),
    path('updatepatient/<patient_id>/edit', views.update_patient, name='updatepatient'),
    path('deletepatient/<patient_id>/edit', views.delete_patient, name='deletepatient'),
    path('', include(router.urls)),
    path('makepayment/', views.make_payment, name = 'makepayment')
]
