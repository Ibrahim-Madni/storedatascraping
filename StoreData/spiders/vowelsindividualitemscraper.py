import scrapy
import json
import re
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy_splash import SplashRequest 
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.images import ImagesPipeline
from urllib.parse import unquote, urljoin, quote
from scrapy import Request
# from StoreData.settings import INSTANCE_1_SETTINGS, INSTANCE_2_SETTINGS

#class to store category along with subcategories and also product items
class StoreItem(scrapy.Item):
    CategoryTitle = scrapy.Field()
    Subcategories = scrapy.Field()
    productItems= scrapy.Field()
    categoryImage = scrapy.Field()
    
#class to store subcategory item
class SubcategoryItem(scrapy.Item):
    subcategoryTitle = scrapy.Field()
    productItems = scrapy.Field(default = [])

#class to store product items
class ProductItem(scrapy.Item):
    CategoryTitle = scrapy.Field()
    subcategoryTitle = scrapy.Field()
    ItemTitle = scrapy.Field()
    ItemURL = scrapy.Field()
    ItemPrice = scrapy.Field()
    image_urls = scrapy.Field()
    ItemColour = scrapy.Field()
    images = scrapy.Field()
   
    ItemDescription = scrapy.Field()
   

class DataStoreSpider(scrapy.Spider):
    name = "vowel_scraper"
 
    start_urls = [
        "https://vowels.net/products/cashmere-blend-shirt-cardigan?variant=50018157396199",
        "https://vowels.net/products/cashmere-blend-shirt-cardigan?variant=50018157527271",
        "https://vowels.net/products/tessellated-sweater?variant=50018171420903",
        "https://vowels.net/products/classic-tee-1?variant=50018162180327",
        "https://vowels.net/products/classic-zip-hoodie?variant=48670286086375",
        "https://vowels.net/products/classic-hoodie?variant=48670280548583",
        "https://vowels.net/products/baggy-denim?variant=48670279303399",
        "https://vowels.net/products/baggy-denim?variant=48670279893223",
        "https://vowels.net/products/baggy-fit-canvas-jean?variant=50018154905831",
        "https://vowels.net/products/limonta-puffer-jacket?variant=50018167488743",
        "https://vowels.net/products/limonta-puffer-jacket?variant=50018167587047",
        "https://vowels.net/products/chore-jacket?variant=49269407023335",
        "https://vowels.net/products/chore-jacket?variant=49269406957799",
        "https://vowels.net/products/classic-sweatpant?variant=49269406040295",
        "https://vowels.net/products/classic-sweatpant?variant=49269406138599",
        "https://vowels.net/products/work-pant?variant=50018172207335",
        "https://vowels.net/products/handstitch-knitted-bomber?variant=50018166833383",
        "https://vowels.net/products/cashmere-primaloft-chore-jacket?variant=50018158117095",
        "https://vowels.net/products/double-pocket-shirt-jacket?variant=50018162966759",
        "https://vowels.net/products/double-pocket-shirt-jacket?variant=50018162835687",
        "https://vowels.net/products/sherpa-vest?variant=50018169290983",
        "https://vowels.net/products/printed-button-down-shirt?variant=50018168144103",
        "https://vowels.net/products/classic-tee-1?variant=50018162508007",
        "https://vowels.net/products/classic-crewneck?variant=50018159624423",
        "https://vowels.net/products/classic-crewneck?variant=50018159198439",
        "https://vowels.net/products/classic-crewneck?variant=50018159493351",
        "https://vowels.net/products/classic-crewneck?variant=50018159067367"
    ]
   
    def start_requests(self):
        # Define a URL for an external IP address checker service
        
        
        for url in self.start_urls:
        # Make a request to the external service
            yield SplashRequest(url, self.CustomRequest)
      
    def CustomRequest(self, response):
        product_item = ProductItem()
        ProductTitle = response.css("meta[property='og:title']::attr(content)").get()
        ProductDescription = response.css("meta[property='og:description']::attr(content)").get()
        ProductRawPrice = response.css("meta[property='og:price:amount']::attr(content)").get()
        ProductRealPrice = f"{ProductRawPrice} USD"
        product_info_divs = response.css("div.product-info span::text").getall()
        script_tags = response.xpath('//script[@id="viewed_product"]/text()').getall()
        if script_tags:
            for script_tag in script_tags:
                # print(script_tag)
                matches = re.findall(r'ImageURL:\s*"([^"]+)"', script_tag)
                if matches:
                    # print(matches)
                    for image_url in matches:
                        print("got it")
                        # yield {"image_url": image_url}
                else:
                    self.logger.warning("Image URL not found in a script tag")
        else:
            self.logger.warning("Script tags with id 'viewed_product' not found")
        
        color = None
        for info in product_info_divs:
            match = re.search(r"Color:\s*(.+)", info)
            if match:
                color = match.group(1)
                break

        product_item["ItemTitle"] = ProductTitle
        product_item["ItemURL"] = response.url
        product_item["ItemDescription"] = ProductDescription
        product_item["ItemColour"] = color
        product_item["ItemPrice"] = ProductRealPrice
        product_item["image_urls"] = image_url
        print(f"ProductTitle : {ProductTitle}\nProductDescription : {ProductDescription}\nProductPrice : {ProductRealPrice}\nProductImage : {image_url}\nProductColour : {color}")
        yield product_item
      
  