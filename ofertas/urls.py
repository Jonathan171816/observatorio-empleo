from django.urls import path
from . import views

app_name = 'ofertas'

urlpatterns = [
    path('', views.lista_ofertas, name='list'),
    path('<int:pk>/', views.detalle_oferta, name='detail'),
    path('scrape/', views.scrape_ofertas, name='scrape'),
]
