from django.shortcuts import render, get_object_or_404, redirect
from .models import Oferta
from django.urls import reverse
from django.contrib import messages
# Importamos el scraper correcto desde la carpeta ofertas/scraper
from .computrabajo import scrape_computrabajo

def scrape_ofertas(request):
    query = request.GET.get('q', '').strip()
    if not query:
        messages.error(request, "Debes ingresar un término de búsqueda.")
        return redirect(reverse('ofertas:list'))

    # Llamamos al scraper pasándole la query
    scrape_computrabajo(query)

    messages.success(request, f"Se ha iniciado el scraping para «{query}».")
    return redirect(reverse('ofertas:list'))

def index(request):
    ubicacion = request.GET.get('ubicacion', '').strip()
    salario = request.GET.get('salario', '').strip()
    ofertas = Oferta.objects.all()

    if ubicacion:
        ofertas = ofertas.filter(ubicacion__icontains=ubicacion)
    if salario:
        ofertas = ofertas.filter(salario__icontains=salario)

    return render(request, 'ofertas/base.html', {'ofertas': ofertas})

def lista_ofertas(request):
    ofertas = Oferta.objects.all()
    return render(request, 'ofertas/oferta_list.html', {'ofertas': ofertas})

def detalle_oferta(request, pk):
    oferta = get_object_or_404(Oferta, pk=pk)
    return render(request, 'ofertas/oferta_detail.html', {'oferta': oferta})
