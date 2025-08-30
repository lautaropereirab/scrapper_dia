
# Proyecto #1: Web Scraping del Supermercado DIA

## Descripción

Este proyecto implementa un **proceso automatizado de web scraping** para recolectar información estructurada directamente desde el sitio web del supermercado **DIA Online**.  
El foco principal está en la **automatización de la navegación y extracción de datos** (categorías, productos y precios), garantizando que el script recorra la web como lo haría un usuario y almacene resultados listos para análisis.

## Flujo del Proceso
1. **Acceso y navegación inicial**  
   Selenium abre el sitio, despliega el menú de categorías y permite navegar entre páginas internas.
2. **Exploración de categorías**  
   El script identifica y recorre categorías y subcategorías, interactuando con menús y *checkboxes* dinámicos.
3. **Carga dinámica de productos**  
   Mediante *scroll* automático y clics en el botón **“Mostrar más”**, se cargan todos los ítems visibles de cada listado.
4. **Extracción con BeautifulSoup**  
   Se parsea el HTML para obtener por producto: nombre/descriptor, precios, descuentos, precio por kilo/unidad, enlace al producto e imagen.
5. **Estructuración y almacenamiento**  
   Los datos se consolidan en un **DataFrame de pandas**, se agrega la **fecha de scrapeo** y se exportan a **CSV**.

## Esquema de Datos (salida)
Columnas principales del dataset:
- `descuento_1`, `descuento_2`  
- `campo_vacio_1`, `campo_vacio_2`, `campo_vacio_3`  
- `producto`  
- `precio_sin_descuento`, `precio`, `precio_por_k`  
- `link`, `imagen`  
- `fecha_scrapeo` (añadida en cada ejecución)

## Instalación

La instalación es sencilla y solo requiere clonar este repositorio:

```bash
git clone https://github.com/lautaropereirab/scrapper_dia.git
```

Todos los requisitos de software están incluidos en el mismo.

## Librerías Utilizadas

Este proyecto utiliza las siguientes librerías:
* **selenium**: automatiza navegación e interacción con la web
* **BeautifulSoup (bs4)**: parseo y extracción desde HTML
* **pandas**: DataFrame + exportación a CSV.
* **lxml**: parser rápido y eficiente
* **time / datetime / re**: esperas, marcas temporales y regex

## Posibles Casos de Uso

- Monitorear **variaciones de precios** en el tiempo  
- Construir **dashboards** (promos, top categorías, evolución de precios)  
- Analizar **impacto de descuentos/campañas**  
- Desarrollar **modelos predictivos** sencillos  
- Integrar en apps de **compra inteligente** y comparativas 

## Autor

Este proyecto fue creado y es mantenido por [Lautaro Pereira Basile](https://github.com/lautaropereirab)

## Contacto
Si tienes alguna pregunta o sugerencia, no dudes en contactarme a través de mi perfil de [LinkedIn](https://www.linkedin.com/in/lautaropereirab/)

o por [lautaropereirabasile@gmail.com](mailto:lautaropereirabasile@gmail.com)