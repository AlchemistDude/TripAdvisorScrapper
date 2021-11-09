import scrapy

#Title = //a[@class="bHGqj Cj b"]//text()[position() > 2]
#rate = //svg[@title]/@title/.
#Type = //div[@class="bhDlF bPJHV eQXRG"]/span[@class="XNMDG"]/span[@class="ceUbJ"]//text()[position() > 0]
#Number of reviews = //span[@class="NoCoR"]/text()[position()<=1]
#reviews = //span[@class="cJMPr NE"]//text()
#next page = //a[@data-page-number and @href]/@href

class TripSpider(scrapy.Spider):
    name = 'trip'
    start_urls = [
    "https://www.tripadvisor.co/Restaurants-g294074-Bogota.html"
    
    ]
    custom_settings = {  #Para exportar en json el diccionario

        'FEED_URI':"trip.json",
        "FEED_FORMAT":"json",
        "CONCURRENT_REQUESTS":24,             #Realice 24 peticiones a la vez
        "MEMUSAGE_LIMIT_MB":2048,              #Maxima memoria ram
        "MEMUSAGE_NOTIFY_MAIL": ['osrodriguezc@unal.edu.co'],#Si se llena la memoria, avisara a los emails que esten en la lista
        "ROBOTSTXT_OBEY":False,         #Obedece las reglas en robotstxt
        "USER_AGENT":'AlchemistDude',                   #Indicarle al servidor quienes somos
        "FEED_EXPORT_ENCODING":'utf-8'
    }

    def parse_restaurants(self,response,**kwargs):
        if kwargs:

            title = kwargs['title']
            rate = kwargs['rate']
            restaurant_type = kwargs['restaurant_type']
            n_reviews = kwargs['n_reviews']
            reviews = kwargs['reviews']
      
        title.extend(response.xpath('//a[@class="bHGqj Cj b"]//text()[position() > 2]').getall()) 
        rate.extend(response.xpath('//svg[@title]/@title/.').getall())
        restaurant_type.extend(response.xpath('//div[@class="bhDlF bPJHV eQXRG"]/span[@class="XNMDG"]/span[@class="ceUbJ"]//text()[position() > 0]').getall())
        n_reviews.extend(response.xpath('//span[@class="NoCoR"]/text()[position()<=1]').getall())
        reviews.extend(response.xpath('//span[@class="cJMPr NE"]//text()').getall())


        next_page_button_link = response.xpath('//a[@data-page-number and @href]/@href').extract()[1]
        
        
        if next_page_button_link != "/Restaurants-g294074-oa30-Bogota.html#EATERY_LIST_CONTENTS" :
             yield response.follow(next_page_button_link, self.parse_restaurants, cb_kwargs={'title':title,'rate':rate,'restaurant_type':restaurant_type,'n_reviews':n_reviews,'reviews':reviews})
        else:
            yield{
            
            'title':title,
            'rate':rate,
            'restaurant_type':restaurant_type,
            'n_reviews':n_reviews,
            'reviews':reviews

            }           
           

    def parse(self,response):
        
        title = response.xpath('//a[@class="bHGqj Cj b"]//text()[position() > 2]').getall()
        rate = response.xpath('//svg[@title]/@title/.').getall()
        restaurant_type = response.xpath('//div[@class="bhDlF bPJHV eQXRG"]/span[@class="XNMDG"]/span[@class="ceUbJ"]//text()[position() > 0]').getall()
        n_reviews = response.xpath('//span[@class="NoCoR"]/text()[position()<=1]').getall()
        reviews = response.xpath('//span[@class="cJMPr NE"]//text()').getall()


        
        next_page_button_link = response.xpath('//a[@data-page-number and @href]/@href').extract()[1]
        if next_page_button_link:
            
            yield response.follow(next_page_button_link, self.parse_restaurants, cb_kwargs={'title':title,'rate':rate,'restaurant_type':restaurant_type,'n_reviews':n_reviews,'reviews':reviews})
 
        
