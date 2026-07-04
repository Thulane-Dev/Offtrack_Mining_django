
from django.urls import path
from .import views

urlpatterns = [
    path('products/', views.ProductsView, name='products'),
    path('filter-category/', views.category_filter, name='filter-category'),
    path('service/<uuid:product_uuid>/<slug:product_slug>/',
         views.ProductDetailsView, name='service'),
    path('quote/<uuid:product_uuid>/<slug:product_slug>/',
         views.RequestQuoteView, name='quote'),
    path('service-quote/<int:service_id>/<slug:service_name>/',
         views.RequestServiceQuoteView, name='service-quote'),
    path(
        "submit-quote/<uuid:uuid>/<slug:slug>/submit/",
        views.submit_quote,
        name="submit_quote"
    ),
    path(
        "submit-service-quote/<int:service_id>/<slug:service_name>/",
        views.submit_service_quote,
        name="submit_service_quote"
    ),
    path('thank-you/', views.SubmitRedirectPage, name='thank-you'),
]
