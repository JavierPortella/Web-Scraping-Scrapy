import scrapy

# XPath para obtener el link de cada archivo, su título, contenido
XPATH_LINKS_DECLASSIFIED = '//a[starts-with(@href, "collection") and (parent::h3|parent::h2)]/@href'
XPATH_TITLES = '//h1[@class="documentFirstHeading"]/text()'
XPATH_PARAGRAPH = '//div[@class="field-item even"]//p[not(@class) and not(a) and not(strong)]/text()'
XPATH_PARAGRAPH_2 = '//div[@class="field-item even"]//p[not(@class)]/text()'
XPATH_IMAGE = '//div[@class="field-item even"]//a[not(@class) and @target="_blank"]/img/@src'

# Clase que se define toda la lógica para traer información desde internet
class SpiderCIA(scrapy.Spider):

    #Se definen dos atributos

    # Nombre unico cada spider.
    name = 'cia'

    # Lista de urls. Contiene todas las direcciones url que se desea apuntar.
    start_urls = [
        'https://www.cia.gov/readingroom/historical-collections'
    ]
    
    # Configuraciones de Scrapy
    custom_settings = {
        # Guardado de archivos   
        'FEED_URI': 'cia.json',
        'FEED_FORMAT': 'json',

        # Cambiar el encoding del archivo
        'FEED_EXPORT_ENCODING': 'utf-8',

        # No violar pautas de robots.txt
        'ROBOTSTXT_OBEY': True
    }

    # Método obligatorio de todo spider. En este método, se define la lógica para analizar un archivo 
    # y extraer informacion valiosa a partir de el.
    def parse(self, response):

        # Extraer los links de la página
        links_declassified = response.xpath(XPATH_LINKS_DECLASSIFIED).getall()
        
        # Recorrer lista de links
        for link in links_declassified:

            # Seguir los links. Response.urljoin une la url principal con el link
            yield response.follow(link, callback=self.parse_link, cb_kwargs={'url': response.urljoin(link)})

    
    def parse_link(self, response, **kwargs):

        # Extraer la url y guardar en una variable
        link = kwargs['url']

        # Extraer el título
        title = response.xpath(XPATH_TITLES).get()

        # Extraer el contenido.
        paragraph = response.xpath(XPATH_PARAGRAPH).getall()

        # Comprobando que la lista no esté vacía
        if len(paragraph) == 0:
            paragraph2 = response.xpath(XPATH_PARAGRAPH_2).getall()
            path = paragraph2[0].find(".")
            paragraph[0] = paragraph2[0][:path]
        
        body = ''.join(paragraph)
    
        # Extraer la imagen
        image =  response.xpath(XPATH_IMAGE).get()
        
        # Guardar todo lo extraído
        yield {
            'url': link,
            'title': title,
            'body': body,
            'image': image
        }