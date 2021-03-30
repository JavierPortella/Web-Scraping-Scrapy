import scrapy

# Titulo = //h1/a/text()
# Citas = //span[@class="text" and @itemprop="text"]/text()
# Top Ten Tags = //span[@class="tag-item"]/a/text()
# Next page button = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()

# Clase que se define toda la lógica para traer información desde internet
class QoutesSpider(scrapy.Spider):

    #Se definen dos atributos

    # Nombre unico cada spider.
    name = 'quotes' 

    # Lista de urls. Contiene todas las direcciones url que se desea apuntar.
    start_urls = [
        'http://quotes.toscrape.com/'
    ]

    custom_settings = {
        # Guardado de archivos
        'FEED_URI': 'quotes.json',
        'FEED_FORMAT': 'json',
        
        # Numero maximo peticiones asincronas 
        'CONCURRENT_REQUEST': 24,
        
        # Cantidad máxima de RAM
        'MEMUSAGE_LIMIT_MB': 2048,

        # Lista de email, que Scrapy avisa si el spyder excede la cantidad máxima de RAM
        'MEMUSAGE_NOTIFY_MAIL': ['rb@rb.com'],
            
        # No violar pautas de robots.txt
        'ROBOTSTXT_OBEY': True,
        
        # Custom User Agent
        'USER_AGENT': 'Nothing',

        # Cambiar el encoding del archivo
        'FEED_EXPORT_ENCODING': 'utf-8'
    }

    # Método que extrae exclusivamente las citas
    def parse_only_quotes(self, response, **kwargs):

        # Preguntar si existe kwarg
        if kwargs:

            # Guardar en una variable local lo que contiene ese diccionario kwargs (Guardar las citas).
            quotes = kwargs['quotes']
            authors = kwargs['authors']
        
        # Agregar a la lista quotes nuevos resultados (Agregar citas)
        quotes.extend(response.xpath('//span[@class="text" and @itemprop="text"]/text()').getall())

        authors.extend(response.xpath('//small[@class="author" and @itemprop="author"]/text()').getall())

        # Variable que contiene el link a la siguiente página
        next_page_button_link = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()
        
        # Verifica que next_page_button_link exista
        if next_page_button_link:

            # Volverá a llamar a la misma función
            yield response.follow(next_page_button_link,
                                  callback=self.parse_only_quotes,
                                  cb_kwargs={'quotes': quotes, 'authors': authors})
        else:

            # Al no existir la variable, guardar todo en un diccionario
            yield {
                'quotes':  list(zip(quotes, authors))
            }

    # Método obligatorio de todo spider. En este método, se define la lógica para analizar un archivo 
    # y extraer informacion valiosa a partir de el. Generador.
    def parse(self, response):

        # Extraer el título de la página
        title = response.xpath('//h1/a/text()').get()

        # Extraer el contenido de todas las citas
        quotes = response.xpath( '//span[@class="text" and @itemprop="text"]/text()').getall()

        # Extraer los top ten tags
        top_tags = response.xpath('//span[@class="tag-item"]/a/text()').getall()

        authors = response.xpath('//small[@class="author" and @itemprop="author"]/text()').getall()

        # Si existe dentro de la ejecucion de este spider, un atributo de nombre top se guarda el resultado, dentro de mi variable top.
        # Si ese resultado no existe, se obtiene None
        top = getattr(self, 'top', None)

        # Verifica que top exista
        if top:

            # Se desea que top se desea un número
            top = int(top)

            # Guardar el resultado, extraendo un número específico de top tags
            top_tags = top_tags[:top]

        # Retorna parcialemnte los datos. Va a llevar esos datos directamente a un lugar
        yield {
                'title': title,
                'top_tags': top_tags
        }


        # Variable que contiene el atributo href del botón next de la página principal
        next_page_button_link = response.xpath('//ul[@class="pager"]//li[@class="next"]/a/@href').get()

        # Se verifica si next_page_button_link existe, pues en algun momento se llegará a la última página.
        if next_page_button_link:

            # El método follow nos permite seguir al link (Scrapy toma la url absoluta y añadir el resto)
            # Este metodo posee un callback (Método que se ejecutará automaticamente despues de haber cambiado de url).
            yield response.follow(next_page_button_link, 
                                  callback = self.parse_only_quotes, 
                                  cb_kwargs = {'quotes': quotes, 'authors': authors})