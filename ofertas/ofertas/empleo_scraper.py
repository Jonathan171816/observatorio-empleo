# empleo/scraper/empleo_scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote_plus
import time

from empleo.models import OfertaLaboral
from datetime import date


def scrape_empleo_dot_com(query: str):
    """
    Ejecuta un scraping en ElEmpleo.com buscando el término dado,
    y guarda cada oferta en la base de datos.
    """
    print(f"Iniciando scraping de ElEmpleo.com con query «{query}»…")

    # Configurar el navegador en modo headless
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    # Construir URL de búsqueda
    base_url = "https://www.elempleo.com/co/ofertas-empleo"
    search_url = f"{base_url}?q={quote_plus(query)}"
    driver.get(search_url)

    # Espera estática (puedes mejorar con WebDriverWait)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, "lxml")
    driver.quit()

    ofertas = soup.find_all("article", class_="oferta")
    print(f"Se encontraron {len(ofertas)} ofertas para «{query}»")

    for oferta in ofertas:
        try:
            titulo = oferta.find("a", class_="js-o-link").text.strip()
            empresa = oferta.find("span", class_="info-empresa").text.strip()
            ciudad = oferta.find("span", class_="info-ciudad").text.strip()
            fecha = date.today()  # Por simplicidad
            url_relativa = oferta.find("a", class_="js-o-link")["href"]
            url_completa = urljoin(base_url, url_relativa)

            OfertaLaboral.objects.create(
                cargo=titulo,
                empresa=empresa,
                ciudad=ciudad,
                salario="No disponible",
                tipo_contrato="No especificado",
                fecha_publicacion=fecha,
                fuente="ElEmpleo.com",
                url=url_completa,
                termino_busqueda=query
            )

            print(f"Guardada oferta: {titulo} - {empresa}")
        except Exception as e:
            print("Error procesando una oferta:", e)

    print("Scraping de ElEmpleo.com finalizado.")
