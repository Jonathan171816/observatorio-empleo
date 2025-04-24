from django.contrib import admin
from django.urls import path,  include
from ofertas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('ofertas/', include('ofertas.urls')),
]
