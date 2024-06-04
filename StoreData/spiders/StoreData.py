import scrapy
import json
from scrapy.crawler import CrawlerProcess
from scrapy_splash import SplashRequest 
from scrapy.pipelines.images import ImagesPipeline
import os 
import re
from scrapy.pipelines.images import ImagesPipeline
from urllib.parse import unquote, urljoin

class StoreItem(scrapy.Item):
    CategoryTitle = scrapy.Field()
    Subcategories = scrapy.Field()
    productItems= scrapy.Field()

class SubcategoryItem(scrapy.Item):
    subcategoryTitle = scrapy.Field()
    productItems = scrapy.Field()

class ProductItem(scrapy.Item):
    images = scrapy.Field()
    CategoryTitle = scrapy.Field()
    subcategoryTitle = scrapy.Field()
    image_urls = scrapy.Field()
    ItemTitle = scrapy.Field()
    ItemPrice = scrapy.Field()
    ItemSalePrice = scrapy.Field()
    ItemUnit = scrapy.Field()

class DataStoreSpider(scrapy.Spider):
    name = "datastore-spider"
    homeURL = "https://www.edeka24.de/"
    subcat_item = SubcategoryItem()

        

    def start_requests(self):
        start_urls = ['https://www.edeka24.de/']
        for url in start_urls:
            item = StoreItem()
            yield SplashRequest(url = "https://www.edeka24.de/", callback=self.parse , meta={'item': item}, args={'wait': 10, 'timeout': 90})
    def remove_force_sid(self, url):
    # Splitting URL into base and parameters
        base_url, _, params = url.partition('?')
    
    # Splitting parameters by '&' and filtering out the 'force_sid' parameter
        cleaned_params = [param for param in params.split('&') if 'force_sid=' not in param]
    
    # Joining base URL and cleaned parameters
        cleaned_url = base_url
        if cleaned_params:
            cleaned_url += '?' + '&'.join(cleaned_params)
    
        return cleaned_url
        
    def parse(self, response):
        lua_script = """
        function main(splash, args)
            -- Wait for the page to load
            assert(splash:wait(args.wait))
    
            -- Click the element based on the CSS selector
            local element = splash:select('#wrapper > header > div.row > div > nav > ul > li:nth-child(3) > ul > li:nth-child(1) > a')
            if element then
                element:click()
                assert(splash:wait(args.wait))
            end
    
            -- Return the full HTML content
            return splash:html()
        end
        """
        homeURL = "https://www.edeka24.de/"
        
        parentSelector = "#wrapper > header > div.row > div > nav > ul "
        childElements = ["li:nth-child(1)","li:nth-child(2)", "li:nth-child(3)", "li:nth-child(4)","li:nth-child(5)","li:nth-child(6)","li:nth-child(7)","li:nth-child(8)"]
        for element in childElements:
            full_selector = f"{parentSelector} > {element}"
            category_title= response.css(f"{full_selector} > a::attr(data-title)").get()
            CategoryLink = response.css(f"{full_selector} > a::attr(href)").get()
            if CategoryLink and CategoryLink != '#':
                absolute_url = urljoin(self.homeURL, CategoryLink)
                clean_url=self.remove_force_sid(absolute_url)
                yield SplashRequest(clean_url, self.parse_items, meta={'category_title': category_title},  args={'wait': 10, 'timeout': 90})
            else:
                cleaned_url = self.remove_force_sid(CategoryLink)
                print(cleaned_url)
                subcat_elements = response.css(f"{full_selector} > ul > li")
                for li in subcat_elements:
                    
                    subcategoryTitle = li.css("a::text").get()
                    subcatlink = li.css("a::attr(href)").get()
                    cleaned_suburl = self.remove_force_sid(subcatlink)
                    if cleaned_suburl:
                        yield SplashRequest(cleaned_suburl, callback=self.parse_page, meta={'category_title': category_title, 'subcategoryTitle':subcategoryTitle},  args={'wait': 10, 'timeout': 90})
                
   
    def parse_page(self, response):

        lua_script = """
        function main(splash, args)
            local url = args.url  -- This is the ResponseURL you pass as an argument
            splash:go(url)
            splash:wait(2.0)

            local previous_height = splash:evaljs("document.body.scrollHeight")
            
            while true do
                local more_button = splash:select("#loader-btn")
                if more_button then
                    more_button:click()
                    splash:wait(3.0)
                else
                    break
                end

                local current_height = splash:evaljs("document.body.scrollHeight")
                if current_height == previous_height then
                    break
                end
                previous_height = current_height
            end

            return splash:html()
        end
        """
        category_title = response.meta['category_title']
        subcategoryTitle = response.meta['subcategoryTitle']
        ResponseURL = response.url
        yield SplashRequest(ResponseURL, self.parse_items, meta={'category_title': category_title, 'subcategoryTitle':subcategoryTitle}, endpoint='execute', args={'lua_source': lua_script, 'url': ResponseURL, 'wait': 10, 'timeout': 90})


    def parse_items(self, response):


        category_title = response.meta['category_title']
        category_item = StoreItem()
        category_item['CategoryTitle'] = category_title
        category_item['Subcategories'] = []
        ProductTiles = response.css(".product-item > div.row")
        for div in ProductTiles:
            product_item = ProductItem()   

            image_url = div.css("div.col-sm-12 > div.product-image > a > img::attr(src)").get()
            product_item['image_urls'] = [image_url] 

            imagetitle= div.css("div.col-sm-12 > div.product-details > a > h2::text").get().strip()
            product_item['ItemTitle'] =   imagetitle

            salespriceelement =div.css("div.col-sm-12 > div.product-details > div.left > div.price.salesprice::text").get()
            if salespriceelement:
                print(salespriceelement)
                product_item['ItemSalePrice']=re.sub(r'\s+', '', salespriceelement)                 
            else:
                Itemprice = div.css("div.col-sm-12 > div.product-details > div.left > div.price::text").get()
                if Itemprice:
                    print(Itemprice)
                    product_item['ItemPrice']=re.sub(r'\s+', '', Itemprice)
            
            Itemunit= div.css("div.col-sm-12 > div.product-details > div.left > p.price-note::text").get()
            if Itemunit:
                    product_item['ItemUnit'] =re.sub(r'\s+', '', Itemunit)
            print(f"Product Item: {product_item}")
            if product_item:
                subcategoryTitle = response.meta.get('subcategoryTitle', "default_subcategory")
                subcat_exists = False
                for subcat in category_item['Subcategories']:
                    if subcat['subcategoryTitle'] == subcategoryTitle:
                        subcat['productItems'].append(product_item)
                        subcat_exists = True
                        break

                if not subcat_exists:
                    subcat_item = SubcategoryItem()
                    subcat_item['subcategoryTitle'] = subcategoryTitle
                    subcat_item['productItems'] = [product_item]
                    category_item['Subcategories'].append(subcat_item)

        yield category_item
