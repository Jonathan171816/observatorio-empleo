# empleo/scraper/empleo_scraper.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time

from empleo.models import OfertaLaboral
from datetime import date


def scrape_empleo_dot_com():
    print("Iniciando scraping de ElEmpleo.com...")

    # Configurar el navegador (modo headless)
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(options=options)

    base_url = "https://www.elempleo.com/co/ofertas-empleo"
    driver.get(base_url)
    time.sleep(5)  # espera que cargue la página completa (mejorable con wait dinámico)

    soup = BeautifulSoup(driver.page_source, "lxml")
    driver.quit()

    ofertas = soup.find_all("article", class_="oferta")

    print(f"Se encontraron {len(ofertas)} ofertas")

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
                url=url_completa
            )

            print(f"Guardada oferta: {titulo} - {empresa}")
        except Exception as e:
            print("Error procesando una oferta:", e)

    print("Scraping de ElEmpleo.com finalizado.")
