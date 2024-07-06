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
    name = "Asosstore-spider"
    homeURL = "https://www.asos.com/"
    subcat_item = SubcategoryItem()
    cookies = {
        'browseCountry':'AE',
        'browseCurrency':'AED',
        'browseLanguage':'en-GB',
        'currency':10091,
        'storeCode': 'ROW'
    }

        

    def start_requests(self):
        start_urls = ['https://www.asos.com/']
        for url in start_urls:
            item = StoreItem()
            yield scrapy.Request(url = "https://www.asos.com/", cookies = self.cookies, callback=self.parse , meta={'item': item })
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
        # self.logger.info(f"Reqeust Cookies : {response.request.cookies}")
        # self.logger.info(f"The headers for the request are  {response.headers}")
        parentSelector = "div > ul[data-testid='floornav'] > li"
        for li in response.css(parentSelector):
            GenderClothingURL=li.css("a::attr(href)").get()
            GenderClothingName=li.css("a::text").get()
            print(GenderClothingName)
            print(GenderClothingURL)
            
            if GenderClothingURL and GenderClothingURL != '#':
                yield  scrapy.Request(url= GenderClothingURL, cookies = self.cookies,  callback= self.parse_menitems ,meta={'CategoryName': GenderClothingName})
    
    def parse_menitems(self, response):
        
        print(response.url)
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
    
        categoryname = response.meta['CategoryName']
        
        subcategoryNavigation = response.css("div.x_RqXmD > div.EsGFLPm:nth-of-type(2) > div[data-testid='secondarynav-container'] > div.M8Zxf1o > div[data-testid='secondarynav-flyout']  > div.ZAntzlZ.MV4Uu8x > ul.c2oEXGw > li")
        #goes through all the list items and extracts subcategories within the clothing item sublist
        for li in subcategoryNavigation:
            allsubcategorylink = li.css("a::attr(href)").get()
            # print(allsubcategorylink)
            lowercasecategoryname = categoryname.lower()
            #Comparison parameter
            #this peice of code on Line 187 is used to compare the category name with the endpoint of the extracted subcategory link so we dont have unnecessary subcategoryitems that were within the list that are not relevant to the category
            if lowercasecategoryname == allsubcategorylink.split('/')[3].lower():
                
                subcategoryname = li.css("a::text").get()
                subcategorylink = li.css("a::attr(href)").get()
                print(subcategoryname)
                print(subcategorylink)
                match = re.search(r'cid=(\d+)', subcategorylink)
                if match:
                    cid_value = match.group(1)
                    # print(cid_value)
                    itemsURL = f"https://www.asos.com/api/product/search/v2/categories/{cid_value}?offset=0&includeNonPurchasableTypes=restocking&key-search-mvtid=928254-web-plp-fh-baseline-ranking-cocktail&store=ROW&lang=en-GB&currency=AED&rowlength=2&channel=mobile-web&country=AE&keyStoreDataversion=q1av6t0-39&limit=3000"
                    # print(itemsURL)

                # if subcategorylink and subcategorylink != '#':
                    yield scrapy.Request(url= itemsURL, cookies = self.cookies, callback= self.parse_individualitemdetails, meta={'categoryname': categoryname , 'subcategoryname': subcategoryname})

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
        # print(response.url)
        category = response.meta['categoryname']
        subcategoryname = response.meta['subcategoryname']
        json_data = json.loads(response.body)
        product_data = json_data.get('products', [])
        for product in product_data:
            itemname = product.get('name')
            product_price = product.get('price', {}).get('current', {}).get('text')
            product_url = product.get('url')
            actualproduct_url = f"{self.homeURL}/{product_url}"
            yield scrapy.Request(url= actualproduct_url, cookies = self.cookies, callback= self.parse_itempage, meta={'itemname': itemname, 'product_price':product_price,  'subcategoryname': subcategoryname, 'categoryname': category})
            # print(itemname)
            # print(product_price_details)

        # print(response.bcdy)
        # url = response.url
        # print(url)
        # response_body = response.body
        # print(response_body)

        # Define the filename using the URL (optional)
        # filename = 'Response body text.txt'

        # # Write the response body to a file
        # with open(filename, 'wb') as f:
        #     f.write(response_body)

        # self.log(f'Saved file {filename}')
        
        
        
        # self.logger.info(f"Retrieved meta data: subcategoryname={subcategoryname}, categoryname={category}")
        # ItemSections= "section.listingPage_HfNlp > article"
        # LoadMoreButton = response.css("a[data-auto-id='loadMoreProducts']::attr(href)").get()
        # #product-205597587 > a > div.productMediaContainer_kmkXR.mediaContainer_rdzv9 > div > img
        # #product-203390299 > a > div.productMediaContainer_kmkXR.mediaContainer_rdzv9 > div > img
        # for article in response.css(ItemSections):
        #     # itemnames = article.css("a > p.productDescription_sryaw::text").get()
        #     #product-203390299 > a > div.productMediaContainer_kmkXR.mediaContainer_rdzv9 > div > img
        #     itemURL = article.css("a::attr(href)").get()
        #     itemname = article.css("div.productInfo_rwyH5 > p.productDescription_sryaw::text").get()
        #     #product-206835688 > a > div.productMediaContainer_kmkXR.mediaContainer_rdzv9 > div
        #     #product-206492427 > a > div.productMediaContainer_kmkXR.mediaContainer_rdzv9 > div > img
        #     #product-205491471 > a > div.productMediaContainer_kmkXR.mediaContainer_rdzv9 > div > img
        #     # itemimage = article.css("a > div.productMediaContainer_kmkXR.mediaContainer_rdzv9 > div > img::attr(src)").get()
        #     # print(itemimage)
        #     # for img in itemimage:
        #     #     images = img.css("::attr(src)").get()
        #     #     print(images)
        #     itemprice = article.css("span.originalPrice_jEWt1 > span.price__B9LP::text").get()
        #     print(itemprice)
            # print(itemimage)
            # print(itemname)
            
            
            # print(itemURL)
        #     if itemURL:
        #             

        #     # print(itemnames)
            
       
        
        # if LoadMoreButton:
        #     # print("LoadMoreButton found")
        #     yield scrapy.Request(url= LoadMoreButton, cookies = self.cookies, callback= self.parse_individualitemdetails, meta={'itemname': itemname, 'subcategoryname': subcategoryname, 'categoryname': category})
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
        product_item['ItemURL'] = response.url
        # print(categoryname)
        # print(SubcategoryName)   
        Itemname = response.meta['itemname']
        ItemPrice = response.meta['product_price']
        # product_price= ""
        # product_price_json = None
        # pricecontent  = response.xpath('//script[contains(., "window.asos.pdp.config.stockPriceResponse")]/text()').get()
        # product_price_json_match = re.search(r'window\.asos\.pdp\.config\.stockPriceResponse = ({.*?});', pricecontent)
        # if product_price_json_match:
        #     product_price_json = product_price_json_match.group(1)
        #     product_price_data = json.loads(product_price_json)
        #     product_price = product_price_data.get('productPrice', {}).get('current', {}).get('text')
            
        # else:
        #     # Handle the case where the pattern is not found in pricecontent
        #     print("Pattern not found in pricecontent")
        # product_price_json = re.search(r'window\.asos\.pdp\.config\.stockPriceResponse = ({.*?});', pricecontent).group(1)
        # product_item['ItemPrice'] = re.sub(r'\s+', '', product_price)
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
        product_item['ItemPrice'] = ItemPrice
        
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
        # # window.asos.pdp.config.stockPriceResponse
        script_content = response.xpath('//script[contains(., "window.asos.pdp.config.product")]/text()').get()
        # script_content_price = response.xpath('//script[contains(., "window.asos.pdp.config.stockPriceResponse")]/text()').get()
        # price_pattern = re.compile(r'window\.asos\.pdp\.config\.stockPriceResponse\s*=\s*\'(.*?)\';', re.DOTALL)
        product_json = re.search(r'window\.asos\.pdp\.config\.product = ({.*?});', script_content).group(1)
        product_data = json.loads(product_json)
        # productPrice
        # Load the JSON data
        # price_match = price_pattern.search(script_content)
        # if price_match:
        #     product_price_json = price_match.group(1)
        #     product_price_data = json.loads(product_price_json)
        #     product_price = product_price_data[0]['productPrice']['current']['text']
        #     print("Product Price:", product_price)
        #     product_item['ItemPrice'] = product_price
        # product_data_price = json.loads(script_content_price)
        # Now you can access the product data
        # product_price=product_price_data.get('productPrice', {}).get('current', {}).get('text')
        # print(product_price)
        ItemColour = []
        productbrandName = product_data.get('brandName')
        product_item['ItemBrand'] = productbrandName
        producttype = product_data.get('productType', {}).get('name')
        product_item['ItemType'] = producttype
        productvariants = product_data.get('variants', [])
        productimages= product_data.get('images', [])
        # product_item['Size'] = []
        
        # product_name = product_data.get('name')
            
        for index, variant in enumerate(productvariants):
        #         # product_item['Size'].append(productsize)
            productsize = variant.get('size')
            size_key = f'Size{index + 1}'
        #         # Use the created item class
                
        #         # Set the metadata value in the item
            product_item[size_key] = re.sub(r'\s+', '', productsize)
            colour = variant.get('colour')
            ItemColour.append(colour)
            product_item['ItemColour'] =  colour
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
