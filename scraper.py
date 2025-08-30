from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from unidecode import unidecode
import lxml as lxml
import html as html
import time
import pandas as pd
import numpy as np 
import re
import datetime

#medir cuanto tarda el script
start = time.time()

#Link a la pagina web
link = 'https://diaonline.supermercadosdia.com.ar/'
link_sin_barra = 'https://diaonline.supermercadosdia.com.ar'

# Inicializa el driver de Selenium (asegúrate de tener el driver correspondiente instalado)
driver = webdriver.Chrome()  # Puedes cambiar a otro navegador y/o ruta del driver si lo necesitas
driver.maximize_window()

#Abre la página web en el navegador controlado por Selenium
driver.get(link)

#Hacemos click en el boton de categorias
button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'diaio-custom-mega-menu-0-x-custom-mega-menu-trigger__button')))
button.click()

# Obtiene el HTML después de cargar todos los elementos
html_home = driver.page_source

# # Cierra el navegador controlado por Selenium
# driver.quit()

#Se busca dentro del HTML las categorias donde hacer hover
sp_home = BeautifulSoup(html_home, 'lxml')
sp_categorias = sp_home.find("div",{"class":"diaio-custom-mega-menu-0-x-category-list__container"}).find_all("a")
categorias = []
for cat in sp_categorias:
    # href = cat.get("href")
    categorias.append(cat.get("href"))
categorias 

# Abre la página web en el navegador controlado por Selenium
driver.get(categorias[0])
html_categoria = driver.page_source

#Se obtiene la lista de categorias internas 
sp_categoria_interna = BeautifulSoup(html_categoria, 'lxml')
categorias_internas = sp_categoria_interna.find("div", {"class":"diaio-search-result-0-x-filter__container diaio-search-result-0-x-filter__container--plp bb b--muted-4 diaio-search-result-0-x-filter__container--category-2"})
lista_checkboxes = categorias_internas.find("div", {"class":"diaio-search-result-0-x-filterTemplateOverflow diaio-search-result-0-x-filterTemplateOverflow--plp pb5 overflow-y-auto"}).find_all("input", {"type":"checkbox"})

# #Apretar boton pop-up
# button_popup = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "vtex-modal__close-icon")))
# button_popup.click()

#Lista de categorias dentro de la pagina
id_chechbox = []
for l in lista_checkboxes:
    id_chechbox.append(l.get("id"))
id_chechbox


#Obtencion del HTML que contiene todos los productos de una categoria
productos_obtenidos_html = {}

for i in id_chechbox:
    checkbox_button = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, i)))
    checkbox_button.click()
    time.sleep(5) 

last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Desplazarse un poco hacia abajo
    driver.execute_script("window.scrollBy(0, 1500);")
    time.sleep(2)  # Esperar para cargar más contenido

    # Obtener la nueva altura de la página
    new_height = driver.execute_script("return document.body.scrollHeight")

    # Intentar hacer clic en el botón "Mostrar más"
    try:
        see_more_button = driver.find_element(By.XPATH, "//button[.//div[text()='Mostrar más']]")
        if see_more_button.is_displayed():
            # Desplazar el botón a la vista
            driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", see_more_button)
            time.sleep(1)
            # Verificar si está habilitado y hacer clic
            if see_more_button.is_enabled():
                see_more_button.click()
                time.sleep(2)  # Esperar después del clic
    except Exception as e:
        # Capturar el error pero seguir el bucle
        pass

    # Salir del bucle si no hay más contenido
    if new_height == last_height:
        break
    
    
    # Actualizar la altura de la página para la siguiente iteración
    last_height = new_height

# Regresar al inicio de la página

time.sleep(5)
html_productos = driver.page_source
driver.quit()


soup_3 = BeautifulSoup(html_productos, 'lxml')
productos_categoria = soup_3.find('div', {"id":"gallery-layout-container"}).find_all("div", {"class":"diaio-search-result-0-x-galleryItem"})

total_items = []  # Lista para acumular todos los productos

for litem_listado in range(len(productos_categoria)):
    imagen = productos_categoria[litem_listado].find('img')
    link_imagen = imagen['src'] if imagen else None

    # Extracción link a la web del producto en el supermercado
    web_producto = productos_categoria[litem_listado].find('a')
    url_producto = link_sin_barra + web_producto['href'] if web_producto else None

    # Datos del producto
    informacion_producto_wrapped = []
    productos = productos_categoria[litem_listado].find('div', 'vtex-flex-layout-0-x-flexCol').find_all('div', 'vtex-flex-layout-0-x-flexColChild')
        
    for div in productos:
        targets = div.find_all("div", attrs={"aria-label": True})
        for t in targets:
            informacion_producto_wrapped.append(t.get_text(strip=True))

    informacion_producto_wrapped.append(link_imagen)
    informacion_producto_wrapped.append(url_producto)

    # Ajustar longitud para que coincida exactamente con las 11 columnas
    lista_columnas = [
        'descuento_1','descuento_2','campo_vacio_1','producto',
        'campo_vacio_2', 'campo_vacio_3',
        'precio_sin_descuento', 'precio', 
        'precio_por_k','link', 'imagen'
    ]
    if len(informacion_producto_wrapped) > len(lista_columnas):
        informacion_producto_wrapped = informacion_producto_wrapped[:len(lista_columnas)]
    elif len(informacion_producto_wrapped) < len(lista_columnas):
        informacion_producto_wrapped += [None] * (len(lista_columnas) - len(informacion_producto_wrapped))

    total_items.append(informacion_producto_wrapped)

dataframe_productos = pd.DataFrame(total_items, columns=lista_columnas)
dataframe_productos["fecha_scrapeo"] = datetime.date.today()
csv_name = 'Almacen.csv'
dataframe_productos.to_csv(f'Productos Obtenidos/{csv_name}', index=False)

end = time.time() 
print(f"Tiempo transcurrido: {end - start:.2f} segundos")