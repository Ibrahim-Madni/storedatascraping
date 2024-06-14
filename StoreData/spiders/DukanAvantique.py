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
    # CategoryTitle = scrapy.Field()
    # subcategoryTitle = scrapy.Field()
    image_urls = scrapy.Field()
    # ItemColour = scrapy.Field()
    ItemTitle = scrapy.Field()
    ItemPrice = scrapy.Field()
    # ItemType = scrapy.Field()
    ItemDescription = scrapy.Field()
    # ItemBrand = scrapy.Field()
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
    Item_URL = scrapy.Field()
    # SubcategoryName = scrapy.Field()
    # categoryName = scrapy.Field()
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
    name = "dukkanavantique"
    homeURL = "https://www.dukkanavantique.com/collections/ss22-collection"
    subcat_item = SubcategoryItem()

        

    def start_requests(self):
        start_urls = ['https://www.dukkanavantique.com/collections/ss22-collection']
        for url in start_urls:
            item = StoreItem()
            yield scrapy.Request(url = "https://www.dukkanavantique.com/collections/ss22-collection", callback=self.parse , meta={'item': item})
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
        # parentSelector = "div > ul[data-testid='floornav'] > li"
        #ajaxSection > x-cell:nth-child(1)
        #product-grid > li:nth-child(1)
        mainclass = "ul#product-grid > li"
        for li in response.css(mainclass):
            #product-grid > li:nth-child(1) > div > div.card-information > div > h3 > a
            itemurl=li.css("div > div.card-information > div > h3 > a::attr(href)").get()
            # GenderClothingName=li.css("a::text").get()
            if itemurl:
                actualurl = f'{self.homeURL}{itemurl}'
                # print(actualurl)
                yield scrapy.Request(url= actualurl , callback= self.parse_menitems)
            
            # GenderClothingWomenURL=li.css("a#women-floor::attr(href)").get()
            # GenderClothingWomenName=li.css("a#women-floor::text").get()
            # print(GenderClothingName)
            # print(GenderClothingURL)
            
            # if GenderClothingURL and GenderClothingURL != '#':
                # absolute_url = urljoin(self.homeURL, CategoryLink)
                # clean_url=self.remove_force_sid(absolute_url)
                # yield  scrapy.Request(url= GenderClothingURL, callback= self.parse_menitems ,meta={'CategoryName': GenderClothingName})
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
    #Slide-template--15262244044980__main-29223350698164 > modal-opener > div > img
    def parse_menitems(self, response):
        # print(response.url)
        # salediv = "span.price-item--sale"
        product_item = ProductItem()
        imagelist = "ul.product__media-list > li"
        sizeslist = "variant-radios > fieldset > label"
        metadatalist = "div.product__description > p"
        product_item['image_urls'] = []
        itemURL= response.url
        product_item['Item_URL'] = itemURL
        # descriptions = []
        for index, metadata in enumerate(response.css(metadatalist)):
            item_description_parts = metadata.css("::text").getall()
            item_description = " ".join(item_description_parts).replace("\u00a0", " ").strip()
            # descriptions.append(item_description)
            metadata_key = f'MetaData{index + 1}'
            product_item[metadata_key] = item_description
        # for index,description in descriptions:
        #     # product_item['ItemDescription'].append(description)
        #     metadata_key = f'MetaData{index + 1}'
        #     product_item[metadata_key] = description
            
        for index,label in enumerate(response.css(sizeslist)):
            sizeguide = label.css("::text").get()
            size=re.sub(r'\s+', ' ',sizeguide) 
            size_key = f'Size{index + 1}'
            product_item[size_key] = size
            # for index in enumerate(sizeguide):
                # size_key = f'Size{index + 1}'
                # product_item[size_key] = index
            # print(sizeguide)
        for li in response.css(imagelist):
            imageendpoint = li.css("modal-opener > div > img::attr(src)").get()
            actualimageurl = f"https:{imageendpoint}"
            product_item['image_urls'].append(actualimageurl)
            # print(actualimageurl)
            # product_item.setdefault('image_urls', []).append(actualimageurl)
            # print(actualimageurl)
#ProductInfo-template--15262244044980__main > h1
        ItemTitle = response.css("h1.product__title::text").get()
        product_item['ItemTitle']=re.sub(r'\s+', ' ', ItemTitle).strip()

        ItemPrice = response.css("span.price-item--regular::text").get()
        product_item['ItemPrice'] = re.sub(r'\s+', ' ', ItemPrice).strip()
        # re.sub(r'\s+', ' ', ItemPrice).strip()
        # print(ItemPrice)
        # if(salediv):
        #     print("item on sale")
        yield(product_item)
        # print(ItemTitle)
        
        #ProductInfo-template--15262244044980__main > variant-radios > fieldset > label:nth-child(3)
        #Slide-template--15262244044980__main-29223350698164 > modal-opener > div > img
    #     product_item = ProductItem()
    #    #MainProduct-template--16591591932061__main > x-grid > x-cell.bullet-product-content
    #     itemname = response.css("section#xtitle > h1::text").get()
    #     product_item['ItemTitle'] = itemname
    #     itemdescription = "#MainProduct-template--16591591932061__main > x-grid > x-cell.bullet-product-content > product-content > section.description > div > p"
    #     for index,itemdesc in enumerate(response.css(itemdescription)):
    #         actualdescription = itemdesc.css("::text").get()
    #         metadata_key = f'MetaData{index + 1}'
    #         product_item[metadata_key] = actualdescription

    #     itemprice = response.css("#price-template--16591591932061__main > div > div > div.price__regular > span::text").get()
    #     product_item['ItemPrice'] = itemprice
    #     sizeoptions = "#Option-template--16591591932061__main-0 > option"
    #     for index,sizeoption in enumerate(response.css(sizeoptions)):
    #         size= sizeoption.css("::text").get()
    #         size_key = f'Size{index + 1}'
    #             # Use the created item class
                
    #             # Set the metadata value in the item
    #         product_item[size_key] = re.sub(r'\s+', '', size)
    #         # product_item['ItemDescription'].append(size)

    #     for imageurlcard in response.css("x-cell.slider__slide "):
    #         imageurl = imageurlcard.css("a > picture > img::attr(src)").get()
    #         actualimageurl = f'https:{imageurl}'
    #         product_item.setdefault('image_urls', []).append(actualimageurl)
    #     print(product_item)
    #     yield product_item
        # lua_script = """
        # function main(splash, args)
        #     local url = args.url  -- This is the ResponseURL you pass as an argument
        #     splash:go(url)
        #     splash:wait(2.0)

        #     local category_button = splash:select("div.x_RqXmD > button[data-index='2']")
        #     if category_button then
        #         category_button:click()
        #         splash:wait(3.0)
        #     end

        #     return splash:html()
        # end
        # """
        # filename = 'html_content_men_page.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log(f'Saved HTML content to {filename}')
        # print("I am here")
        # categoryname = response.meta['CategoryName']
        # categoryItem= response.css("div.x_RqXmD > button[data-index='2'] > span.cSfPh9_ > span::text").get()
        # print(categoryname)
        #chrome-sticky-header > div.AIjKzKx > div:nth-child(1) > nav > div > div > button.yI6sHXc.TYb4J9A.fVdHxMU.QNzo9qy > span > span
        # subcategoryNavigation = "div.x_RqXmD:nth-of-type(1) > div.EsGFLPm:nth-of-type(3) > div[data-testid='secondarynav-container'] > div.M8Zxf1o > div[data-testid='secondarynav-flyout']  > div.ZAntzlZ.MV4Uu8x > ul.c2oEXGw > li"
        # subcategoryNavigation = "div.x_RqXmD:nth-of-type(1) > div.EsGFLPm:nth-of-type(2) > div[data-testid='secondarynav-container'] > div.M8Zxf1o > div[data-testid='secondarynav-flyout']  > div.ZAntzlZ.MV4Uu8x > ul.c2oEXGw > li"
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
        # for li in response.css(subcategoryNavigation):
        #     subcategoryname = li.css("a::text").get()
        #     allsubcategorylink = li.css("a::attr(href)").get()
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
            #         yield scrapy.Request(url= subcategorylink, callback= self.parse_individualitemdetails, meta={'categoryname': categoryname , 'subcategoryname': subcategoryname})
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
        lua_script = """
        function main(splash, args)
            local url = args.url  -- This is the ResponseURL you pass as an argument
            splash:go(url)
            splash:wait(2.0)

            local previous_height = splash:evaljs("document.body.scrollHeight")
            
            while true do
                local more_button = splash:select(".loadButton_wWQ3F")
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
        category = response.meta['categoryname']
        subcategoryname = response.meta['subcategoryname']
        
        self.logger.info(f"Retrieved meta data: subcategoryname={subcategoryname}, categoryname={category}")
        # self.log(f'Saved HTML content and item names to {filename}')
        # filename = 'individual_clothes_page.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log(f'Saved HTML content to {filename}')
        ItemSections= "section.listingPage_HfNlp > article"
        LoadMoreButton = response.css("a[data-auto-id='loadMoreProducts']::attr(href)").get()
        # print(LoadMoreButton)
        # itemnames_list = [] 
        for article in response.css(ItemSections):
            # itemnames = article.css("a > p.productDescription_sryaw::text").get()
            itemURL = article.css("a::attr(href)").get()
            itemname = article.css("a > p.productDescription_sryaw::text").get()
            #price-template--15262244044980__main > div > div > div.price__regular > span.price-item.price-item--regular
            itemprice = article.css("span..price-item--regular::text").get()
            print(itemprice)
            
            
            # print(itemURL)
            if itemURL:
                yield scrapy.Request(url= itemURL, callback= self.parse_itempage, meta={'itemname': itemname, 'subcategoryname': subcategoryname, 'categoryname': category})    

            # print(itemnames)
            
       
        
        if LoadMoreButton:
            # print("LoadMoreButton found")
            yield scrapy.Request(url= LoadMoreButton, callback= self.parse_individualitemdetails, meta={'itemname': itemname, 'subcategoryname': subcategoryname, 'categoryname': category})
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
        categoryname = response.meta['categoryname']
        SubcategoryName = response.meta['subcategoryname']
        print(categoryname)
        print(SubcategoryName)   
        Itemname = response.meta['itemname']
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
        product_item['categoryName'] = categoryname
        product_item['SubcategoryName'] = SubcategoryName
        # try:
        #     if ItemPrice:
        #         product_item['ItemPrice'] = re.sub(r'\s+', '', ItemPrice)
        #     else:
        #          raise ValueError("Item price is NULL")

        # except ValueError as e:
        # # Log the error message
        #     self.logger.error(f"Failed to extract item price: {str(e)}")
        #     if retry_count > 0:
        #     # Retry the extraction with reduced retry_count
        #         self.logger.info(f"Retrying item price extraction. Retries left: {retry_count}")
        #         time.sleep(5)  # Add a delay before retrying
        #         return self.extract_item_price(response, retry_count - 1)
        #     else:
        #         self.logger.error("Maximum retry attempts reached. Giving up on item price extraction.")
        #     # Handle failure to extract item price after maximum retries
        #     # For example, set a default value
        #         product_item['ItemPrice'] = "N/A"
        product_item['ItemTitle'] = Itemname
        
        ProductDetailContainer = "div.F_yfF > ul > li"
        for index, li in enumerate(response.css(ProductDetailContainer)):
            ProductExtendedDetails = li.css("::text").get()
            # print(ProductExtendedDetails)
            if ProductExtendedDetails:
                # Dynamically create metadata keys based on the iteration index
                metadata_key = f'MetaData{index + 1}'
                # Use the created item class
                
                # Set the metadata value in the item
                product_item[metadata_key] =ProductExtendedDetails
        # window.asos.pdp.config.stockPriceResponse
        script_content = response.xpath('//script[contains(., "window.asos.pdp.config.product")]/text()').get()
        script_content_price = response.xpath('//script[contains(., "window.asos.pdp.config.stockPriceResponse")]/text()').get()
        price_pattern = re.compile(r'window\.asos\.pdp\.config\.stockPriceResponse\s*=\s*\'(.*?)\';', re.DOTALL)
        product_json = re.search(r'window\.asos\.pdp\.config\.product = ({.*?});', script_content).group(1)
        product_data = json.loads(product_json)
        # productPrice
        # Load the JSON data
        price_match = price_pattern.search(script_content)
        if price_match:
            product_price_json = price_match.group(1)
            product_price_data = json.loads(product_price_json)
            product_price = product_price_data[0]['productPrice']['current']['text']
            print("Product Price:", product_price)
            product_item['ItemPrice'] = product_price
        # product_data_price = json.loads(script_content_price)
        # Now you can access the product data
        # product_price=product_price_data.get('productPrice', {}).get('current', {}).get('text')
        # print(product_price)
        
        productbrandName = product_data.get('brandName')
        product_item['ItemBrand'] = productbrandName
        producttype = product_data.get('productType', {}).get('name')
        product_item['ItemType'] = producttype
        productvariants = product_data.get('variants', [])
        productimages= product_data.get('images', [])
        # product_item['Size'] = []
        
        # product_name = product_data.get('name')
            
        for index, variant in enumerate(productvariants):
                # product_item['Size'].append(productsize)
            productsize = variant.get('size')
            size_key = f'Size{index + 1}'
                # Use the created item class
                
                # Set the metadata value in the item
            product_item[size_key] = re.sub(r'\s+', '', productsize)
            colour = variant.get('colour')
            product_item['ItemColour'] = re.sub(r'\s+', '', colour)
            # print(size)
            # print(colour)
        product_item['image_urls'] = []
        # product_item['image_urls'] = image_urls
        for image in productimages:
            imageURL = image.get('url')
            if imageURL:
                product_item['image_urls'].append(imageURL)
                break
            # image_urls = [image.get('url') for image in product_images]
        print(product_item)
        yield product_item
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
