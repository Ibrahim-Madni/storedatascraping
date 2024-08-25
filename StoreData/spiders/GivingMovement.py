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
    ItemDescription = scrapy.Field()
    image_urls = scrapy.Field()
    ItemColour = scrapy.Field()
    ItemTitle = scrapy.Field()
    ItemPrice = scrapy.Field()
    ItemType = scrapy.Field()
    ItemBrand = scrapy.Field()
    MetaData1 = scrapy.Field()
    MetaData2 = scrapy.Field()
    MetaData3 = scrapy.Field()
    MetaData4 = scrapy.Field()
    MetaData5 = scrapy.Field()
    MetaData6 = scrapy.Field()
    MetaData7 = scrapy.Field()
    MetaData8 = scrapy.Field()
    MetaData9 = scrapy.Field()
    MetaData10 = scrapy.Field()
    MetaData11 = scrapy.Field()
    MetaData12 = scrapy.Field()
    MetaData13 = scrapy.Field()
    ItemURL = scrapy.Field()
    SubcategoryName = scrapy.Field()
    categoryName = scrapy.Field()
    Size1 = scrapy.Field()
    Size2 = scrapy.Field()
    Size3 = scrapy.Field()
    Size4 = scrapy.Field()
    Size5 = scrapy.Field()
    Size6 = scrapy.Field()
    Size7 = scrapy.Field()
    Size8 = scrapy.Field()
    Size9 = scrapy.Field()
    Size10 = scrapy.Field()
    Size11 = scrapy.Field()
    Size12 = scrapy.Field()
    Size13 = scrapy.Field()
    Size14 = scrapy.Field()
    Size15 = scrapy.Field()
    Size16 = scrapy.Field()
    Size17 = scrapy.Field()
    Size18 = scrapy.Field()
    Size19 = scrapy.Field()
    Size20 = scrapy.Field()
    

class DataStoreSpider(scrapy.Spider):
    name = "movement-spider"
    homeURL = "https://thegivingmovement.com"
    subcat_item = SubcategoryItem()

        

    def start_requests(self):
        start_urls = ['https://thegivingmovement.com/']
        for url in start_urls:
            item = StoreItem()
            yield scrapy.Request(url = "https://thegivingmovement.com/", callback=self.parse , meta={'item': item})
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
        # 
    def parse(self, response):
        # filename = 'html_content.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log(f'Saved HTML content to {filename}')

        # lua_script = """
        # function main(splash, args)
            # -- Wait for the page to load
            # assert(splash:wait(args.wait))
    # 
            # -- Click the element based on the CSS selector
            # local element = splash:select('#wrapper > header > div.row > div > nav > ul > li:nth-child(3) > ul > li:nth-child(1) > a')
            # if element then
                # element:click()
                # assert(splash:wait(args.wait))
            # end
    # 
            # -- Return the full HTML content
            # return splash:html()
        # end
        # """
        # homeURL = "https://www.edeka24.de/"
        # 
        parentSelector = "div.desktop-only > div.navigation.navigation--main > div.navigation__tier-1-container > ul.navigation__tier-1 > li:nth-child(-n+2)"
        for li in response.css(parentSelector):
            GenderURLendpoint=li.css("a.navigation__link::attr(href)").get()
            GenderClothingName=li.css("a.navigation__link::text").get()
            
            GenderClothingURL = self.homeURL + GenderURLendpoint
            # GenderClothingWomenURL=li.css("a#women-floor::attr(href)").get()
            # GenderClothingWomenName=li.css("a#women-floor::text").get()
            print(GenderClothingName)
            print(GenderClothingURL)
            
            if GenderClothingURL and GenderClothingURL != '#':
                # absolute_url = urljoin(self.homeURL, CategoryLink)
                # clean_url=self.remove_force_sid(absolute_url)
                yield  scrapy.Request(url= GenderClothingURL, callback= self.parse_menitems,meta={'CategoryName': GenderClothingName})
            # if GenderClothingWomenURL and GenderClothingWomenURL != '#':
            #     # absolute_url = urljoin(self.homeURL, CategoryLink)
            #     # clean_url=self.remove_force_sid(absolute_url)
            #     yield scrapy.Request(url= GenderClothingWomenURL, callback= self.parse_menitems, meta={'CategoryName': GenderClothingMenName})
            # else:

                # cleaned_url = self.remove_force_sid(CategoryLink)
                # print(cleaned_url)
                # subcat_elements = response.css(f"{full_selector} > ul > li")
                # for li in subcat_elements:
                    # 
                    # subcategoryTitle = li.css("a::text").get()
                    # subcatlink = li.css("a::attr(href)").get()
                    # cleaned_suburl = self.remove_force_sid(subcatlink)
                    # if cleaned_suburl:
                        # yield SplashRequest(cleaned_suburl, callback=self.parse_page, meta={'category_title': category_title, 'subcategoryTitle':subcategoryTitle},  args={'wait': 10, 'timeout': 90})
                # 
    
    def parse_menitems(self, response):
        
       
        lua_script = """
        function main(splash, args)
            local url = args.url  -- This is the ResponseURL you pass as an argument
            splash:go(url)
            splash:wait(2.0)

            local category_button = splash:select("div.x_RqXmD > button[data-index='2']")
            if category_button then
                category_button:click()
                splash:wait(3.0)
            end

            return splash:html()
        end
        """
        # print(response.url)
        # filename = 'html_content_men_page.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log(f'Saved HTML content to {filename}')
        categoryname = response.meta['CategoryName']
        # categoryItem= response.css("div.x_RqXmD > button[data-index='2'] > span.cSfPh9_ > span::text").get()
        # print(categoryname)
        #chrome-sticky-header > div.AIjKzKx > div:nth-child(1) > nav > div > div > button.yI6sHXc.TYb4J9A.fVdHxMU.QNzo9qy > span > span
        responsesplitendpoint = "/".join(response.url.split("/")[-2:])
        collection_name = responsesplitendpoint.split("/")[-1].split("?")[0]
        print(collection_name)
        acceptable_men_subcategories = ["https://thegivingmovement.com/collections/tops-men?nav=true", "/collections/top-long-sleeve-mens?nav=true", "https://thegivingmovement.com/collections/shorts-mens?nav=true", "https://thegivingmovement.com/collections/joggers-mens?nav=true", "https://thegivingmovement.com/collections/jackets-mens?nav=true", "/collections/hoodies-and-sweatshirts-mens?nav=true"]
        acceptable_women_subcategories = ["https://thegivingmovement.com/collections/tshirts-women?nav=true", "https://thegivingmovement.com/collections/top-long-sleeve-womens?nav=true", "/collections/leggings-womens?nav=true", "https://thegivingmovement.com/collections/shorts-womens?nav=true", "https://thegivingmovement.com/collections/joggers-womens?nav=true", "https://thegivingmovement.com/collections/jackets-womens?nav=true", "/collections/hoodies-and-sweatshirts-womens?nav=true" ]
        if collection_name == 'womens-collection':
            subcategoryNavigation = "div#NavigationTier2-1 > div.container > ul > li.navigation__item.navigation__item--with-children.navigation__column > div.navigation__tier-3-container.navigation__child-tier  > ul.navigation__tier-3 > li"
            for li in response.css(subcategoryNavigation):
                subcategoryname = li.css("a::text").get()
                
                allsubcategorylink = li.css("a::attr(href)").get()
                if allsubcategorylink in acceptable_women_subcategories:
                    domain_name = "/".join(allsubcategorylink.split("/")[:3])
                    if domain_name == self.homeURL:
                        yield scrapy.Request(url= allsubcategorylink, callback= self.parse_individualitemdetails, meta={'categoryname': categoryname , 'subcategoryname': subcategoryname})
                    else:
                        subcategorylink = self.homeURL + domain_name
                        yield scrapy.Request(url= subcategorylink, callback= self.parse_individualitemdetails, meta={'categoryname': categoryname , 'subcategoryname': subcategoryname})

        else:
            subcategoryNavigation = "div#NavigationTier2-2 > div.container > ul > li.navigation__item.navigation__item--with-children.navigation__column > div.navigation__tier-3-container.navigation__child-tier  > ul.navigation__tier-3 > li"
            for li in response.css(subcategoryNavigation):
                subcategoryname = li.css("a::text").get()
                allsubcategorylink = li.css("a::attr(href)").get()
                # print(allsubcategorylink)
                if allsubcategorylink in acceptable_men_subcategories:
                    domain_name = "/".join(allsubcategorylink.split("/")[:3])
                    if domain_name == self.homeURL:
                        yield scrapy.Request(url= allsubcategorylink, callback= self.parse_individualitemdetails, meta={'categoryname': categoryname , 'subcategoryname': subcategoryname})
                    else:
                        subcategorylink = self.homeURL + domain_name
                        yield scrapy.Request(url= subcategorylink, callback= self.parse_individualitemdetails, meta={'categoryname': categoryname , 'subcategoryname': subcategoryname})
                # print(subcategoryname)
                # print(allsubcategorylink)
        # subcategoryname = response.css("div.x_RqXmD:nth-of-type(1) > div.EsGFLPm:nth-of-type(3) > div[data-testid='secondarynav-container'] > div.M8Zxf1o > div[data-testid='secondarynav-flyout']  > div.ZAntzlZ.MV4Uu8x > ul.c2oEXGw > li > a::text").get()
        # subcategorylink = response.css("div.x_RqXmD:nth-of-type(1) > div.EsGFLPm:nth-of-type(3) > div[data-testid='secondarynav-container'] > div.M8Zxf1o > div[data-testid='secondarynav-flyout']  > div.ZAntzlZ.MV4Uu8x > ul.c2oEXGw > li > a::attr(href)").get()
        # if subcategorylink and subcategorylink != '#':
            # yield SplashRequest(url= subcategorylink, callback= self.parse_individualitemdetails, meta={'categoryname': categoryname , 'subcategoryname': subcategoryname})
        # subcategoryNavigation = response.xpath('//div[@id="96b432e3-d374-4293-8145-b00772447cde"]/div/div[2]/div/div[1]/ul/li[2]/text()').get()
        # print(subcategoryNavigation)
        # //*[@id="96b432e3-d374-4293-8145-b00772447cde"]
        # //*[@id="96b432e3-d374-4293-8145-b00772447cde"]/div/div[2]/div/div[1]/ul/li[2]
        #\39 6b432e3-d374-4293-8145-b00772447cde > div > div.M8Zxf1o > div > div.ZAntzlZ.MV4Uu8x > ul > li:nth-child(1)
        #  > div.M8Zxf1o > div.GL2wQf0 > 
        # subcategorylink = response.css("div.x_RqXmD > div#e87ba617-daa1-4b64-8f36-ab92e61283f7 > div[data-testid='secondarynav-container'] > div.M8Zxf1o > div[data-testid='secondarynav-flyout']  > div.ZAntzlZ.MV4Uu8x > ul.c2oEXGw > li > a::attr(href)").get()
        
        # subcategoryNavigation = response.css("div.EsGFLPm > div.M8Zxf1o > div.ZAntzlZ.MV4Uu8x > ul.c2oEXGw > li > a::text").get()

        # print(subcategoryNavigation)
        
            # print(subcategorylink)
            # print(subcategoryname)
            # lowercasecategoryname = categoryname.lower()
            # lowercasecategoryname = 'men'
            # endpoint = subcategorylink.split('/')[3]
            # if lowercasecategoryname == allsubcategorylink.split('/')[3].lower():
            #     subcategoryname = li.css("a::text").get()
            #     subcategorylink = li.css("a::attr(href)").get()
            #     print(subcategoryname)
            #     print(subcategorylink)
            #     if subcategorylink and subcategorylink != '#':
            #         yield SplashRequest(url= subcategorylink, callback= self.parse_individualitemdetails, meta={'categoryname': categoryname , 'subcategoryname': subcategoryname})
                    # self.logger.info(f"Passing meta data: subcategoryname={subcategoryname}, categoryname={categoryname}")
# 

            # print(subcategoryname) 
        # for button in response.css(categoryItem):
      
            # categoryItemName= button.css("span::text").get()
      
            # print(categoryItemName)
        # filename = 'html_content_men_page.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log(f'Saved HTML content to {filename}')
    def parse_individualitemdetails(self, response):
        # lua_script = """
        # function main(splash, args)
        #     local url = args.url  -- This is the ResponseURL you pass as an argument
        #     splash:go(url)
        #     splash:wait(2.0)

        #     local previous_height = splash:evaljs("document.body.scrollHeight")
            
        #     while true do
        #         local more_button = splash:select(".loadButton_wWQ3F")
        #         if more_button then
        #             more_button:click()
        #             splash:wait(3.0)
        #         else
        #             break
        #         end

        #         local current_height = splash:evaljs("document.body.scrollHeight")
        #         if current_height == previous_height then
        #             break
        #         end
        #         previous_height = current_height
        #     end

        #     return splash:html()
        # end
        # """
        categoryname = response.meta['categoryname']
        subcategoryname = response.meta['subcategoryname']
        processed_urls = []
        processed_nextpage_urls = []
        # print(categoryname)
        # print(subcategoryname)
        next_button =  response.css("link[rel='next']::attr(href)").get()
        
        # print(next_button)
        for product in response.css("div.product_card_all"):
            # print(product)
            # productlink = product.css("div.block-inner > div > div.product-info > div > div > a::attr(href)").get()
            productname = product.css("div.block-inner > div > div.product-info > div > div > a > p::text").get()
            productcolour = product.css("div.product-block-options__inner > span")
            for colourvariants in productcolour:
                actualcolour = colourvariants.css("::attr(data-color)").get()
                productvariantlink = colourvariants.css("::attr(data-url)").get()
                productpriceraw = colourvariants.css("::attr(data-price-text)").get()
                pattern = r"</?span[^>]*>"
                if productpriceraw:
                    productprice = re.sub(pattern, "", productpriceraw).strip()
                    pattern_unwanted = r'[^\dAED\s]'
                    actualproductprice = re.sub(pattern_unwanted, "", productprice).strip()
                    # print(actualproductprice)
                    if productvariantlink not in processed_urls:
                        processed_urls.append(productvariantlink)
                        actualproductlink= f"{self.homeURL}{productvariantlink}"
                        yield scrapy.Request(url= actualproductlink, callback= self.parse_itempage, meta={'categoryname': categoryname , 'subcategoryname': subcategoryname, 'productprice': actualproductprice, "colour": actualcolour, "productname": productname })
                    
        if next_button:
            next_page_url = f"{self.homeURL}{next_button}"
            if next_page_url not in processed_nextpage_urls:
                processed_nextpage_urls.append(next_page_url)
                yield scrapy.Request(url= next_page_url, callback= self.parse_individualitemdetails, meta={'categoryname': categoryname , 'subcategoryname': subcategoryname})
                    # if productprice:
                    #     currency = productprice.group(1)
                    #     value = int(productprice.group(2))
                        # print(currency, value)
                    # print(f"actual colour is {actualcolour}, the colour variant link is {productvariantlink} and the raw product price is {productprice}") 
            # productpriceinteger = product.css("div.block-inner > div > div.product-info > div > div > a > div > span > span::text").get()
            # print(f"product link : {productlink}, product Name is : {productname}, and the productpriceinteger is : {productpriceinteger}")
    def parse_next_page_individualitemdetails(self, response):
        categoryname = response.meta['categoryname']
        subcategoryname = response.meta['subcategoryname']
        processed_urls = []
        # print(categoryname)
        # print(subcategoryname)
        next_button =  response.css("link[rel='next']::attr(href)").get()
        
        # print(next_button)
        for product in response.css("div.product_card_all"):
            # print(product)
            # productlink = product.css("div.block-inner > div > div.product-info > div > div > a::attr(href)").get()
            productname = product.css("div.block-inner > div > div.product-info > div > div > a > p::text").get()
            productcolour = product.css("div.product-block-options__inner > span")
            for colourvariants in productcolour:
                actualcolour = colourvariants.css("::attr(data-color)").get()
                productvariantlink = colourvariants.css("::attr(data-url)").get()
                productpriceraw = colourvariants.css("::attr(data-price-text)").get()
                pattern = r"</?span[^>]*>"
                if productpriceraw:
                    productprice = re.sub(pattern, "", productpriceraw).strip()
                    pattern_unwanted = r'[^\dAED\s]'
                    actualproductprice = re.sub(pattern_unwanted, "", productprice).strip()
                    # print(actualproductprice)
                     
                    if productvariantlink not in processed_urls:
                        processed_urls.append(productvariantlink)
                        actualproductlink= f"{self.homeURL}{productvariantlink}"
                        
                        yield scrapy.Request(url= actualproductlink, callback= self.parse_itempage, meta={'categoryname': categoryname , 'subcategoryname': subcategoryname, 'productprice': actualproductprice, "colour": actualcolour, "productname": productname })
        if next_button:
            next_page_url = f"{self.homeURL}{next_button}"
            yield scrapy.Request(url= next_page_url, callback= self.parse_last_page_individualitemdetails, meta={'categoryname': categoryname , 'subcategoryname': subcategoryname})
        
        
    def parse_last_page_individualitemdetails(self, response):
        categoryname = response.meta['categoryname']
        subcategoryname = response.meta['subcategoryname']
        processed_urls = []
        # print(categoryname)
        # print(subcategoryname)
        # next_button =  response.css("link[rel='next']::attr(href)").get()
        
        # print(next_button)
        for product in response.css("div.product_card_all"):
            # print(product)
            # productlink = product.css("div.block-inner > div > div.product-info > div > div > a::attr(href)").get()
            productname = product.css("div.block-inner > div > div.product-info > div > div > a > p::text").get()
            productcolour = product.css("div.product-block-options__inner > span")
            for colourvariants in productcolour:
                actualcolour = colourvariants.css("::attr(data-color)").get()
                productvariantlink = colourvariants.css("::attr(data-url)").get()
                productpriceraw = colourvariants.css("::attr(data-price-text)").get()
                pattern = r"</?span[^>]*>"
                if productpriceraw:
                    productprice = re.sub(pattern, "", productpriceraw).strip()
                    pattern_unwanted = r'[^\dAED\s]'
                    actualproductprice = re.sub(pattern_unwanted, "", productprice).strip()
                    # print(actualproductprice)
                    if productvariantlink not in processed_urls:
                        processed_urls.append(productvariantlink)
                        actualproductlink= f"{self.homeURL}{productvariantlink}"

                        yield scrapy.Request(url= actualproductlink, callback= self.parse_itempage, meta={'categoryname': categoryname , 'subcategoryname': subcategoryname, 'productprice': actualproductprice, "colour": actualcolour, "productname": productname })
       
    #shopify-section-template--14532118544419__main > div > div.container.container--no-max > div.filter-container.filter-container--side.filter-container--show-filters-desktop.filter-container--mobile-initialised > div.filters-adjacent.collection-listing > div > div:nth-child(1)
        # print(response.url)
        # category = response.meta['categoryname']
        # subcategoryname = response.meta['subcategoryname']
        
        # self.logger.info(f"Retrieved meta data: subcategoryname={subcategoryname}, categoryname={category}")
        # # self.log(f'Saved HTML content and item names to {filename}')
        # # filename = 'individual_clothes_page.html'
        # # with open(filename, 'wb') as f:
        #     # f.write(response.body)
        # # self.log(f'Saved HTML content to {filename}')
        # Itemcatalogue = "div.product-info > div.inner > div.innerer"
        # for div in response.css(Itemcatalogue):
        #     subitemURL= div.css("a.product-link::attr(href)").get()
        #     itemname= div.css("a.product-link > p::text").get()
        #     if subitemURL:
        #         itemURL = self.homeURL + subitemURL 
        #         yield scrapy.Request(url= itemURL, callback= self.parse_itempage, meta={'itemname': itemname, 'subcategoryname': subcategoryname, 'categoryname': category})
        # LoadMoreButton = response.css("a.pagination__next.inh-col.underline.underline--on-hover::attr(href)").get()
        # print(LoadMoreButton)
        # if(LoadMoreButton):
        #     itemURL = self.homeURL + subitemURL 
        #     yield scrapy.Request(url= LoadMoreItemsURL, callback= self.parse_individualitemdetails, meta={'itemname': itemname, 'subcategoryname': subcategoryname, 'categoryname': category})
        # # # print(LoadMoreButton)
        # # # itemnames_list = [] 
        # for div in response.css(ItemSections):
        #     # itemnames = article.css("a > p.productDescription_sryaw::text").get()
        #     subitemURL = div.css("a.product-link::attr(href)").get()
        #     itemname = div.css("a.product-link > p::text").get()
        # #     # itemprice = article.css("a > p.container_s8SSI > span.originalPrice_jEWt1 > span.price__B9LP::text").get()
        #     # print(itemname)
            
            
        #     # print(itemURL)
        #     if subitemURL:
        #         itemURL = self.homeURL + subitemURL 
        #         yield scrapy.Request(url= itemURL, callback= self.parse_itempage, meta={'itemname': itemname, 'subcategoryname': subcategoryname, 'categoryname': category})    

        #     # print(itemnames)
            
       
        
        # if LoadMoreButton:
        #     LoadMoreItemsURL = self.homeURL + LoadMoreButton  
        #     print("LoadMoreButton found")
        #     yield scrapy.Request(url= LoadMoreItemsURL, callback= self.parse_individualitemdetails, meta={'itemname': itemname, 'subcategoryname': subcategoryname, 'categoryname': category})
            # if itemnames:
            #     itemnames_list.append(itemnames) 

        # filename = 'individual_clothes_page.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        #     f.write(b'\n\n')  # Add newlines for better readability
        #     f.write(b'Item Names:\n')
        #     for itemname in itemnames_list:
        #         f.write(itemname.encode('utf-8'))  # Write item names to the file
        #         f.write(b'\n')  # Add a newline after each item name

        # self.log(f'Saved HTML content and item names to {filename}')
        # filename = 'individual_clothes_page.html'
        # with open(filename, 'wb') as f:
            # f.write(response.body)
        # self.log(f'Saved HTML content to {filename}')
        # print(response)
    def parse_itempage(self, response):
        product_item = ProductItem()
        # 
        # 

        # 
        product_item_list = []

        categoryname = response.meta['categoryname']
        SubcategoryName = response.meta['subcategoryname']
        productprice = response.meta['productprice']
        colour = response.meta['colour']
        productname = response.meta['productname']
        #headlessui-disclosure-panel-2 > ul > li:nth-child(1)
        product_item['ItemURL'] = response.url
        product_item['CategoryTitle'] = categoryname
        product_item['subcategoryTitle'] = SubcategoryName
        product_item['ItemTitle'] = productname
        product_item['ItemPrice'] = productprice
        product_item['ItemColour'] = colour
        metadatalist = response.css("div.pb-16 > disclosure-panel > ul > li")
        metadatafit = response.css("div > disclosure-panel > p").get()
        description_pattern = r"<strong>(.*?)</strong>"
        descriptionmatch = re.search(description_pattern, metadatafit)
        if descriptionmatch:
            strong_content = descriptionmatch.group(1)
            product_item['ItemDescription'] = strong_content
        else:
            print("No match found")
        for index, metadata in enumerate(metadatalist):
            ProductExtendedDetails = metadata.css("::text").get()
            # print(ProductExtendedDetails)
            if ProductExtendedDetails:
                # Dynamically create metadata keys based on the iteration index
                metadata_key = f'MetaData{index + 1}'
                # Use the created item class
                
                # Set the metadata value in the item
                product_item[metadata_key] =ProductExtendedDetails
        # for metadata in metadatalist:

        #     metadatatext = metadata.css("::text").get()
        # 

        # # Use re.search to find the match
        # match = re.search(pattern, metadatafit)

        # # Extract the content inside the <strong> tags if a match is found
        # if match:
        #     strong_content = match.group(1)
        #     product_item['ItemDescription'] = match
        # else:
        #     print("No match found")
        script_content = response.xpath('//script[@id="back-in-stock-helper"]/text()').get()
        if script_content:
            # Step 3: Use Regex to Extract JSON
            json_pattern = re.compile(r'_BISConfig\.product\s*=\s*(\{.*?\});', re.DOTALL)
            match = json_pattern.search(script_content)
            
            if match:
                json_data = match.group(1)
                # self.log(f'Extracted JSON: {json_data}')

                image_pattern = re.compile(r'"media":\s*(\[[^\]]*\])')

                # Search for the pattern in the JSON data
                image_match = image_pattern.search(json_data)
                image = ""
                matching_images = []
                # actualimage =""
                if image_match:
                    media_value_str = image_match.group(1)
                    media_value = json.loads(media_value_str)
                    for media_item in media_value:
                        if media_item.get("alt") == colour:
                            matching_images.append(media_item.get("src"))
                        

                    actualimage = f"https:{matching_images[-2]}"
                    # print(actualimage)
                    product_item['image_urls'] =actualimage
                    
                    # if media_value.get([{}],"alt") == colour:
                    #     print("done value")
                        # image = media.get("src")
                        # print(image)

                # with open(output_file, 'w', encoding='utf-8') as f:
                #     json.dump(product_data, f, ensure_ascii=False, indent=4)
                
                # self.log(f'Successfully wrote product data to {output_file}')

                # images_pattern = r'"media": \[(\{[^]]*\})\]'
                # images_matches = re.search(images_pattern, product_data)
                # if images_matches:
                #     print(images_matches)
                # else:
                #     print("Media array not found.")

# Search for the pattern in the API response
        
        
            
        # print(f"categoryname: {categoryname}, subcategoryname : {SubcategoryName}, productprice : {productprice}, colour: {colour}, productname : {productname}")
        # Itemname = response.meta['itemname']
        # ItemPrice = response.meta['itemprice']
        # product_price_json = None
        # pricecontent  = response.xpath('//script[contains(., "window.asos.pdp.config.stockPriceResponse")]/text()').get()
        # product_price_json_match = re.search(r'window\.asos\.pdp\.config\.stockPriceResponse = ({.*?});', pricecontent)
        # if product_price_json_match:
            # product_price_json = product_price_json_match.group(1)
            # product_price_data = json.loads(product_price_json)
            # product_price = product_price_data.get('productPrice', {}).get('current', {}).get('text')
            # product_item['ItemPrice'] = re.sub(r'\s+', '', product_price)
        # else:
            # Handle the case where the pattern is not found in pricecontent
            # print("Pattern not found in pricecontent")
        # product_price_json = re.search(r'window\.asos\.pdp\.config\.stockPriceResponse = ({.*?});', pricecontent).group(1)
        # product_item['categoryName'] = categoryname
        # product_item['SubcategoryName'] = SubcategoryName
        # # try:
        # #     if ItemPrice:
        # #         product_item['ItemPrice'] = re.sub(r'\s+', '', ItemPrice)
        # #     else:
        # #          raise ValueError("Item price is NULL")

        # # except ValueError as e:
        # # # Log the error message
        # #     self.logger.error(f"Failed to extract item price: {str(e)}")
        # #     if retry_count > 0:
        # #     # Retry the extraction with reduced retry_count
        # #         self.logger.info(f"Retrying item price extraction. Retries left: {retry_count}")
        # #         time.sleep(5)  # Add a delay before retrying
        # #         return self.extract_item_price(response, retry_count - 1)
        # #     else:
        # #         self.logger.error("Maximum retry attempts reached. Giving up on item price extraction.")
        # #     # Handle failure to extract item price after maximum retries
        # #     # For example, set a default value
        # #         product_item['ItemPrice'] = "N/A"
        # product_item['ItemTitle'] = Itemname
        
        # ProductDetailContainer = "div.F_yfF > ul > li"
        # for index, li in enumerate(response.css(ProductDetailContainer)):
        #     ProductExtendedDetails = li.css("::text").get()
        #     # print(ProductExtendedDetails)
        #     if ProductExtendedDetails:
        #         # Dynamically create metadata keys based on the iteration index
        #         metadata_key = f'MetaData{index + 1}'
        #         # Use the created item class
                
        #         # Set the metadata value in the item
        #         product_item[metadata_key] =ProductExtendedDetails
        # # window.asos.pdp.config.stockPriceResponse
        # script_content = response.xpath('//script[contains(., "window.asos.pdp.config.product")]/text()').get()
        # script_content_price = response.xpath('//script[contains(., "window.asos.pdp.config.stockPriceResponse")]/text()').get()
        # price_pattern = re.compile(r'window\.asos\.pdp\.config\.stockPriceResponse\s*=\s*\'(.*?)\';', re.DOTALL)
        # product_json = re.search(r'window\.asos\.pdp\.config\.product = ({.*?});', script_content).group(1)
        # product_data = json.loads(product_json)
        # # productPrice
        # # Load the JSON data
        # price_match = price_pattern.search(script_content)
        # if price_match:
        #     product_price_json = price_match.group(1)
        #     product_price_data = json.loads(product_price_json)
        #     product_price = product_price_data[0]['productPrice']['current']['text']
        #     print("Product Price:", product_price)
        #     product_item['ItemPrice'] = product_price
        # # product_data_price = json.loads(script_content_price)
        # # Now you can access the product data
        # # product_price=product_price_data.get('productPrice', {}).get('current', {}).get('text')
        # # print(product_price)
        
        # productbrandName = product_data.get('brandName')
        # product_item['ItemBrand'] = productbrandName
        # producttype = product_data.get('productType', {}).get('name')
        # product_item['ItemType'] = producttype
        # productvariants = product_data.get('variants', [])
        # productimages= product_data.get('images', [])
        # # product_item['Size'] = []
        
        # # product_name = product_data.get('name')
            
        # for index, variant in enumerate(productvariants):
        #         # product_item['Size'].append(productsize)
        #     productsize = variant.get('size')
        #     size_key = f'Size{index + 1}'
        #         # Use the created item class
                
        #         # Set the metadata value in the item
        #     product_item[size_key] = re.sub(r'\s+', '', productsize)
        #     colour = variant.get('colour')
        #     product_item['ItemColour'] = re.sub(r'\s+', '', colour)
        #     # print(size)
        #     # print(colour)
        # product_item['image_urls'] = []
        # # product_item['image_urls'] = image_urls
        # for image in productimages:
        #     imageURL = image.get('url')
        #     if imageURL:
        #         product_item['image_urls'].append(imageURL)
        #     # image_urls = [image.get('url') for image in product_images]
        # print(product_item)
        if product_item not in product_item_list:
            product_item_list.append(product_item)  # Add the new product_item to the list
            yield product_item
        # yield product_item
        # gender = prodULRdata.get('gender')
        # print(productbrandName)
        # print(producttype)
        # print(product_name)
        # print(gender)
        # ProductColour = response.css("div.L3V0U > p::text").get()
        # print(ProductColour)
        
        # for li in response.css(ProductDetailContainer):
        #     # ProductBrand = li.css("div#productDescriptionDetails > div.F_yfF > a[1] > strong::text").get()
        #     ProductCategory = li.css("div#productDescriptionDetails > div.F_yfF > a:nth-child(2)  > strong::text").get()
        # print(ProductCategory)
            # print(ProductBrand)


        # ProductSizes = []
        # ProductSizes = response.css()
        # print(response)
        # filename = 'html_content_itempage.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log(f'Saved HTML content to {filename}')
        #  
        # ItemTitle = response.css("h1.jcdpl::text").get()
        # itemPrice = response.css("span.MwTOWl::text").get()
        # 
        # ItemPrice = response.css("div.layout-aside > div[data-testid ='product-price'] > span[data-testid='current-price']").get()
        # print(ItemTitle)
        # print(itemPrice)


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

