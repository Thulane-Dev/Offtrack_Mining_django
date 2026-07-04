
from django.urls import path
from .import views

urlpatterns = [
    path('', views.IndexView, name='index'),
    path('about/', views.AboutView, name='about'),
    path('marketplace/', views.MarketplaceView, name='marketplace'),
    path('services/', views.ServicesView, name='services'),
    path('contract/', views.ContractView, name='contract'),
    path("contract-enquiry/", views.Submit_Contact_Enquiry, name="contract-enquiry"),
    path('menu/', views.MenuView, name='menu'),
]
