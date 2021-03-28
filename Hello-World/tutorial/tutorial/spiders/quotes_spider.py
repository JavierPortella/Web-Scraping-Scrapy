import scrapy

# Clase que se define toda la lógica para traer información desde internet
class QuotesSpider(scrapy.Spider):

    #Se definen dos atributos
    name = 'quotes'

    # Contiene todas las direcciones url que se desea apuntar. Las páginas para hacer webscraping
    start_urls = [
        'http://quotes.toscrape.com/'
    ]

    # En este método, se define la lógica para extraer información
    def parse(self, response):

        # Crear un archivo que contiene el contenido de la respuesta html
        with open('resultados.html', 'w', encoding='utf-8') as f:

            # Escribir en el archivo 
            f.write(response.text)