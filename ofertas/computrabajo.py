from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

def obtener_ofertas():
    opciones = Options()
    opciones.add_argument("--headless")
    driver = webdriver.Chrome(options=opciones)

    url = 'https://co.computrabajo.com/trabajo-de-analista-de-datos'
    driver.get(url)
    time.sleep(3)

    ofertas = []

    while True:
        elementos = driver.find_elements(By.CLASS_NAME, 'js-o-link')
        for elem in elementos:
            titulo = elem.text
            enlace = elem.get_attribute('href')
            # Aquí puedes agregar más lógica para obtener empresa, ubicación, salario y descripción

            ofertas.append({'titulo': titulo, 'enlace': enlace})

        try:
            siguiente_pagina = driver.find_element(By.CLASS_NAME, 'pagination-next')
            siguiente_pagina.click()
            time.sleep(3)
        except:
            break

    driver.quit()

    return ofertas

def guardar_ofertas():
    ofertas = obtener_ofertas()
    df = pd.DataFrame(ofertas)
    df.to_csv('ofertas.csv', index=False)

if __name__ == '__main__':
    guardar_ofertas()