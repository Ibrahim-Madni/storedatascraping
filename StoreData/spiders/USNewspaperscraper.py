import scrapy
import json
import re
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
    ItemSalePrice = scrapy.Field()
    ItemUnit = scrapy.Field()
    ItemBrand = scrapy.Field()
    image_urls = scrapy.Field()
    ItemColour = scrapy.Field()
    images = scrapy.Field()
    size = scrapy.Field()
    ItemDescription = scrapy.Field()
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
    MetaData14 = scrapy.Field()
    MetaData15 = scrapy.Field()
    MetaData16 = scrapy.Field()
    MetaData17 = scrapy.Field()
    MetaData18 = scrapy.Field()
    MetaData19 = scrapy.Field()
    MetaData20 = scrapy.Field()

class DataStoreSpider(scrapy.Spider):
    name = "newspaperus"
    homeURL = "https://ae.loropiana.com/en/"
    subcat_item = SubcategoryItem()
    product_api_url = "https://www.zara.com/ae/en/category"
    
    # custom_headers = {
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    # 'Sec-Ch-Ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    # 'Sec-Ch-Ua-Mobile': '?0',
    # 'Sec-Ch-Ua-Platform': '"Windows"',
    # 'Sec-Fetch-Dest': 'empty',
    # 'Sec-Fetch-Mode': 'cors',
    # 'Sec-Fetch-Site': 'cross-site',
    # ... any other headers you want to include ...
    # }

    custom_cookies = {
        '__Secure-1PAPISID': '6wl3847Xx2qcWqlY/AsU77BmANv5IW123L',
        '__Secure-3PSID': 'g.a000iQjrgnUeyyQzOhvVffwQwSUJ_9seUWKidq00jq3KvLaMvMAFV7Vidr5w_6Nwu7_KM66w_wACgYKAXkSAQASFQHGX2MiN1UHzdWd0zfAioR-zTotVxoVAUF8yKpSwri6zp2HXm8zJ9Op8oMw0076',
        'n_user': 's%3Aj%3A%7B%22userId%22%3A4277683698%2C%22userToken%22%3A%22QWpQjtHVCEy5Y0Dq7AqNYdbzTjlqfNO4KhxjW%2FoCLnI%3D%22%2C%22WCToken%22%3A%224277683698%252Cyn5Pr7QgxswLauy8IUxXVudZ9yZMDAfJUojXpKz67DrN45KoKh6zc2gAdymqprOvYFkyl80CepKtuO4l9ckwCPByUt8aLC7bxfyQgZ0r7uTFB7VRbiH9P5DcqjjdEohaeA6mGrd3hh6kXmKmnRPqunKxUqRNlmx0SQotgQX6XG8487UZ%252FR1er7%252F6QTahmOX7tE2RsDzrOfcdIcXPH%252FEpoGtcfPqTxCyMu%252FPu4X%252BuJng%253D%22%2C%22kind%22%3A%22persistent%22%2C%22storeId%22%3A22701%7D.C0tesDdRoprxSsbUiEfwkaQXZ5rnsVFJoHrVHRLD8GU',
        'n_suser': 's%3Aj%3A%7B%22userId%22%3A4277683698%2C%22userToken%22%3A%22QWpQjtHVCEy5Y0Dq7AqNYdbzTjlqfNO4KhxjW%2FoCLnI%3D%22%2C%22WCTrustedToken%22%3A%224277683698%252CvtnI2d2PMb2rqU1Us02rXkUaI%252FtcTzjEpLzH1Rn0UXU%253D%22%7D.y9PXx%2BmsV7eVJ5s9vbKRBL4KD8FZnsN8bD5NViGHk2E',
        'NID': '513=Nzcip1nKNsM8XxmOwy952t9UxMLNSL-5N50K_3XdkJXkrpQbsdnLkzJDiIwvxHMhM9MD9n8D-gAQI2oVicT9tQYzIcemypJcHhRoaoo7ssopMnE4qqqBFNIZ2fPKXx00WV7QnbrYx2l0baoxBb6Lt01PGnQm6Orf0M2QpLcDomFKw3m-SBWKl6M',
        # 6wl3847Xx2qcWqlY/AsU77BmANv5IW123L
        # s%3Aj%3A%7B%22userId%22%3A4277683698%2C%22userToken%22%3A%22QWpQjtHVCEy5Y0Dq7AqNYdbzTjlqfNO4KhxjW%2FoCLnI%3D%22%2C%22WCToken%22%3A%224277683698%252Cyn5Pr7QgxswLauy8IUxXVudZ9yZMDAfJUojXpKz67DrN45KoKh6zc2gAdymqprOvYFkyl80CepKtuO4l9ckwCPByUt8aLC7bxfyQgZ0r7uTFB7VRbiH9P5DcqjjdEohaeA6mGrd3hh6kXmKmnRPqunKxUqRNlmx0SQotgQX6XG8487UZ%252FR1er7%252F6QTahmOX7tE2RsDzrOfcdIcXPH%252FEpoGtcfPqTxCyMu%252FPu4X%252BuJng%253D%22%2C%22kind%22%3A%22persistent%22%2C%22storeId%22%3A22701%7D.C0tesDdRoprxSsbUiEfwkaQXZ5rnsVFJoHrVHRLD8GU
        '__Secure-3PAPISID': '6wl3847Xx2qcWqlY/AsU77BmANv5IW123L',
        # g.a000iQjrgnUeyyQzOhvVffwQwSUJ_9seUWKidq00jq3KvLaMvMAFV7Vidr5w_6Nwu7_KM66w_wACgYKAXkSAQASFQHGX2MiN1UHzdWd0zfAioR-zTotVxoVAUF8yKpSwri6zp2HXm8zJ9Op8oMw0076
        # g.a000iQjrgnUeyyQzOhvVffwQwSUJ_9seUWKidq00jq3KvLaMvMAFV7Vidr5w_6Nwu7_KM66w_wACgYKAXkSAQASFQHGX2MiN1UHzdWd0zfAioR-zTotVxoVAUF8yKpSwri6zp2HXm8zJ9Op8oMw0076
        'ITXSESSIONID': '94acc0613fee90a7b7afba631dd89b3f',
        'ITXDEVICEID': 'f2eadf2c76b22575b28a033021b39c09',
        'JSESSIONID': '0000DTTHQxHaivMpJv29qYOT5r7:2aa2asqcy',
        'IDROSTA':'3b3254b170c7:238e05f99f6b22abeef6e4f7f',
        # 'TS0122c9b6': '0165eae04fc090d4fe65bca4057abde3ccc21430644075c7bec7abbbf535e5f6e7c712b836e7e246ee94c25933a9aeff2cbaf087cd',
        # 'bm_sv': '74BCAEBA6F7F769BFFECEE40EE04897E~YAAQZR0gF5AcbgKPAQAAAu2QGBfGq5x0IDBARj3ltiK6qCBVDTJT7x8AeZ43hx7nmAO9JE90SK3wkeNlel6FTv0FdR0p0kkkzT/Tp97NFc7fk+wyPT/IcHGRtT9UTRnWdVPntwOThtxjg7Uw43S6W5jX759gPn5IgYwJZQkMPE69GRrRJ3ie1B94upEzfVX9PfER75zKXkQPJxXnUZacKehm6eLy2FAPC4iGVabykwmsGP/QSF202k3yzJHhFAU=~1'
    }
     
    # custom_cookies={
                    # 'ITXSESSIONID': '71fee5cda8aa57ee7427246d4bed66e1',
                    # 'IDROSTA' : '39d2489e0357:113b59487f4604207f79de7ce',
                    # 'SSID' : 'A4ORZo4aKjWJpe08k',
                    # 'userType': 'guest',
                    # 'SID' : 'g.a000iQjrgnUeyyQzOhvVffwQwSUJ_9seUWKidq00jq3KvLaMvMAFKHXOMSo-AViTlWB3VOlEMQACgYKAYgSAQASFQHGX2MiKu9EgSIa4_MrhT2n4Ro1bRoVAUF8yKoExCqRpGzx3eeItkUVkMyn0076'
                # }
                # custom_cookies{
                    # 'ITXSESSIONID': 'REPLACE_WITH_CAPTURED_VALUE',
                    # 'IDROSTA': 'REPLACE_WITH_CAPTURED_VALUE',
                    # Potentially missing from headers, add if captured
                    # 'SSID': 'REPLACE_WITH_CAPTURED_VALUE',
                    # 'userType': 'guest',
                    # Potentially missing from headers, add if captured
                    # 'SID': 'REPLACE_WITH_CAPTURED_VALUE',
                    # 'bm_sv': 'REPLACE_WITH_CAPTURED_VALUE',
                    # 'TS0122c9b6': 'REPLACE_WITH_CAPTURED_VALUE',
                    # '_ga_HCEXQGE0MW': 'REPLACE_WITH_CAPTURED_VALUE',
                    # '_gat_UA-18083935-1': 'REPLACE_WITH_CAPTURED_VALUE',
                    # '_itxo11y_id.01fa': 'REPLACE_WITH_CAPTURED_VALUE',
                # }               
# 49c0dd3c1a139954d92cf03d7e7dc1eb  
# 3e375721b0d0:14ed3e6f239a056a0e7beaa57 :  ZaraHomepage
# b1fea1cbb7af:2db675bb44fce6d97c6dbab26 : WOmen / Men: individual item page


    def start_requests(self):
        # Define a URL for an external IP address checker service
        url = 'https://ae.loropiana.com/en'

        # Make a request to the external service
        yield SplashRequest(url, self.CustomRequest)
    #parsing level 1 categories
    # def parse(self, response):

        #to run different settings for different users
        # getting the instance settings from custom_settings_variable
        # instanceSetting = self.settings.get('CUSTOM_SETTINGS_VARIABLE')
        # print(instanceSetting,"this is the setting")
        # xpathsSetting = ''
        # if(instanceSetting == "INSTANCE_1_SETTINGS"):
            # getting the xpaths
            # xpathsSetting = self.settings.get("INSTANCE_1_SETTINGS")
            # print("here")
            # print(xpathsSetting)
        # elif(instanceSetting == "INSTANCE_2_SETTINGS"):
            # xpathsSetting = self.settings.get("INSTANCE_2_SETTINGS")
        # elif(instanceSetting == "INSTANCE_3_SETTINGS"):
            # xpathsSetting = self.settings.get("INSTANCE_3_SETTINGS")
        # 
        
        # XPATHSetting = xpathsSetting.get('XPATH_SELECTORS')
        # Use the XPath selectors specific to this instance
        # xpath_selector_1 = XPATHSetting.get('xpath_selector_1')
        #getting all the categories in the elements variable
        # elements = response.xpath(xpath_selector_1)
       
        # for element in elements:
           
        #     category_title= element.css(f"div.department-box__inner-container > div.department-box__title::text").get()
        #     print(category_title)
        #     imageUrl = element.css(f"div.department-box__image::attr(style)").get()
        #     category_image = imageUrl.split("url(")[-1].strip(");")
        #     print(category_image)
        #     CategoryLink = element.css(f"div.department-box__inner-container > a.department-box__all-link::attr(href)").get()
        #     print(CategoryLink)
        #     # # Subcategories = []
        #     if CategoryLink and CategoryLink != '#':
        #         absolute_url = urljoin(self.homeURL, CategoryLink)
        #         print("absolute URL\n")
        #         print(absolute_url)
        #         if absolute_url:
        #             yield scrapy.Request(url= absolute_url,callback = self.CustomRequest, cookies = self.custom_cookies, headers = self.custom_headers, meta={'category_title': category_title, "category_image":category_image} )

        #  creating and sending request to individual categories          
    def CustomRequest(self, response):
        # filename ="loropianamaindata.html"
        # with open(filename, 'wb')  as f:
        #     f.write(response.body)
        #     self.log(f'Saved HTML content to {filename}')
        processedlinks = []
        navigatablesubcategorylist = ['knitwear', 'shirts and tops','top and t shirts', 'trousers and shorts', 'dresses', 'skirts', 'blazers', 'outerwear jackets', 'coats and capes', 'denim', 'polo and t shirts', 'shirts', 'trousers and bermudas', 'suits', 'blazers', 'vests', 'coats and trench', 'outerwear jackets', 'denim', 'knitwear',  ]
        Navigationlist= "ul.CAFFEINA-menu__main > li.CAFFEINA-menu__item"
        for li in response.css(Navigationlist):
            subcategoryalttitle= li.css("a::attr(title)").get()
            for navigationtitles in navigatablesubcategorylist:
                    if(subcategoryalttitle == navigationtitles):                        
                        Subcategoryname = li.css("a > span::text").get()
                        Subcategorylink = li.css("a::attr(href)").get()
                        Subcategorycode = li.css("a::attr(data-third-lvl-code)").get()
                        # print(Subcategorycode)
                        match = re.search(r'/c/([^/]+)/', Subcategorylink)
                        if match:
                            category = match.group(1)
                        if(Subcategorylink not in processedlinks):
                            processedlinks.append(Subcategorylink)
                            if(Subcategoryname):
                                actualurl = f"{self.homeURL}c/{Subcategorycode}/results?page=0"
                                print(f"{Subcategoryname} : {Subcategorylink}, {category}")
                                yield SplashRequest(actualurl, self.parse_api_response, meta={"categoryname": category, "subcategoryname": Subcategoryname })
                            else:
                                actualurl = f"{self.homeURL}c/{Subcategorycode}/results?page=0"
                                print(f"{subcategoryalttitle} : {Subcategorylink}, {category}")
                                yield SplashRequest(actualurl, self.parse_api_response, meta={"categoryname": category, "subcategoryname": subcategoryalttitle })


        # api_url = "https://www.zara.com/ae/en/categories?"
        # # headers = {
        #     # "x-algolia-agent": "Algolia for vanilla JavaScript (lite) 3.27.0;instantsearch.js 2.10.3;JS Helper 2.26.0",
        #     # "x-algolia-application-id": "1D2IEWLQAD",
        #     # "x-algolia-api-key": "87ca3b6b2ce56f0bb76fc194a8d170e2",
        #     # "Content-Type": "application/json",  # Specify content type as JSON
        # # }
        # # categoryId=2351649&categorySeoId=708&ajax=true
        # # https://www.zara.com/ww/en/categories?categoryId=2351649&categorySeoId=708&ajax=true
        # payload = {
        #             "categoryId": "2351649",
        #             "categorySeoId": "708",
        #             "ajax" : "true"
        #         # ... other request dictionaries ...
        #         }
        # url_with_params = api_url + "&".join([f"{key}={value}" for key, value in payload.items()])
        
        # # category_title = response.meta.get('category_title')
        # # category_image = response.meta.get("category_image")
        # # encoded_category_title = quote(category_title)
        # # params = payload["requests"][0]["params"]
        # #encoding category title 
        # # params += f"&facetFilters=%5B%5B%22taxons_en.lvl1%3ADepartments%20%3E%20{encoded_category_title}%22%5D%5D"
        # # updated_payload = payload.copy()
        # # Update the 'params' field in the first request dictionary
        # # updated_payload["requests"][0]["params"] = params
        
        # #sending request to get level2 categories
        # yield Request(
        #     url=url_with_params,
        #     method='GET',
        #     # body=json.dumps(payload),
        #     callback=self.parse_api_response,
            
            
        # )
    # parsing the level2 categories
    def parse_api_response(self, response):
        print(response.url)
        # processedlinks = []
        individualprocessedlinks = []
        category_title = response.meta.get('categoryname')
        sub_category_title = response.meta.get('subcategoryname')
        json_content = response.css("pre::text").get()  # Extract text from the 'pre' element
        # Now you can load the json_content into a dictionary using json.loads()
        data = json.loads(json_content)
        totalnumberofpages= data.get('pagination',{}).get('numberOfPages')
        # print(totalnumberofpages)
        cataloguedata = data.get('results', {})
        for item in cataloguedata:
            itemurlendpoint = item.get('url')
            individualitemurl = f"{self.homeURL}{itemurlendpoint}"
            itemtype = item.get('eshopMaterialCode')
            itemname = item.get('name')
            itemprice = item.get('price', {}).get('formattedValue')
            catalogueimages = item.get('images', [])
            for image in catalogueimages:
                imagetype = image.get('format')
                if imagetype == "front-mobile":
                    imageurl = image.get("url")
                    if individualitemurl not in individualprocessedlinks:
                        individualprocessedlinks.append(individualitemurl)
                        yield SplashRequest(individualitemurl, self.SubcategoryURLParse, meta={"categoryname": category_title, "subcategoryname": sub_category_title , "imageurl": imageurl, "itemtype": itemtype, "itemname":itemname, "itemprice": itemprice})
                    # print(f"item's digital url is{itemdigitalurl} while the item type itself is {itemtype} while it has the following name {itemname} while it being priced at {itemprice}while it has the following relevant imageurl{imageurl}")
        processedlinks = []
        for i in range(1, totalnumberofpages):
            next_page_url = f"{response.url.replace('page=0', f'page={i}')}"
            if next_page_url not in processedlinks:
                processedlinks.append(next_page_url)
                yield SplashRequest(next_page_url, self.parse_next_page_response, meta={"categoryname": category_title, "subcategoryname": sub_category_title })
    



    def parse_next_page_response(self, response):
        individualprocessedlinks = []
        category_title = response.meta.get('categoryname')
        sub_category_title = response.meta.get('subcategoryname')
        # category_title = response.meta.get('categoryname')
        # sub_category_title = response.meta.get('subcategoryname')
        json_content = response.css("pre::text").get()
        data = json.loads(json_content)
        cataloguedata = data.get('results', {})
        for item in cataloguedata:
            itemurlendpoint = item.get('url')
            individualitemurl = f"{self.homeURL}{itemurlendpoint}"
            itemtype = item.get('eshopMaterialCode')
            itemname = item.get('name')
            itemprice = item.get('price', {}).get('formattedValue')
            catalogueimages = item.get('images', [])
            for image in catalogueimages:
                imagetype = image.get('format')
                if imagetype == "front-mobile":
                    imageurl = image.get("url")
                    if individualitemurl not in individualprocessedlinks:
                        individualprocessedlinks.append(individualitemurl)
                        yield SplashRequest(individualitemurl, self.SubcategoryURLParse, meta={"categoryname": category_title, "subcategoryname": sub_category_title , "imageurl": imageurl, "itemtype": itemtype, "itemname":itemname, "itemprice": itemprice})
    
    def SubcategoryURLParse(self,response):
        # filename ="loropianaitemdata.html"
        product_item = ProductItem()
        category_title = response.meta.get('categoryname')
        product_item["CategoryTitle"] = category_title
        sub_category_title = response.meta.get('subcategoryname')
        product_item["subcategoryTitle"] =sub_category_title
        product_item["ItemURL"] = response.url
        itemtitle = response.meta.get('itemname')
        product_item["ItemTitle"] =itemtitle
        itemprice = response.meta.get('itemprice')
        product_item["ItemPrice"] =itemprice
        itemtype = response.meta.get('itemtype')
        product_item["ItemBrand"] =itemtype
        imageurl = response.meta.get('imageurl')
        product_item["image_urls"]= imageurl
        itemcolour = response.css("div.colourvalue > span::text").get()
        product_item["ItemColour"] =itemcolour
        separated_text = []
        # print(itemcolour)
        text = response.css("div#productDetail > div.content > p.t-product-copy::text").get()
        if not text:
            product_item["MetaData1"] ="N/A"    
        if "<br>" in text: 
            text_parts = text.split("<br>")
            for index, text_part in enumerate(text_parts):
                
                metadata_key = f'MetaData{index + 1}'
                product_item[metadata_key] =text_part
        else:
            product_item["MetaData1"] =text    
        # print(product_item)
        yield product_item
        # with open(filename, 'wb')  as f:
        #     f.write(response.body)
        #     self.log(f'Saved HTML content to {filename}')
        # category_title = response.meta.get('categoryName')
        # sub_category_title = response.meta.get('subcategoryname')
        # categoryId = response.meta.get('categoryID')
        # json_response = json.loads(response.text)
        # processed_seo_keywords = set()
        # product_groups = json_response.get('productGroups', [])
        # for group in product_groups:
        #     elements = group.get('elements', [])
        #     for element in elements:
        #         commercial_components = element.get('commercialComponents', [])
        #         for component in commercial_components:
        #             # marketingmetainfo = component.get('marketingMetaInfo',{})
        #             # if not isinstance(marketingmetainfo, list):
        #                 # marketingmetainfo = [marketingmetainfo] 
        #             # for marketmeta in marketingmetainfo:
        #                 # mappinginfo = marketmeta.get('mappingInfo', [])
        #                 # for mapping in mappinginfo:
        #                     # regions = mapping.get("regions", [])
        #                     # for region in regions:
        #                         # area_link = region.get('areaLink', {})
        #                         # mainlink = area_link.get('url')
        #                         # endpoint = area_link.get('queryParams')
        #                         # print(mainlink)
        #                         # print(endpoint)


        #             seo = component.get('seo', {})
        #             ProductSEOkeyword = seo.get('keyword')
        #             SEOProductID = seo.get('seoProductId')
        #             DiscerningProductID = seo.get('discernProductId')
        #             # print(f"{ProductSEOkeyword} : SEOID = {SEOProductID} , Discerning ID {DiscerningProductID}")
        #             if ProductSEOkeyword not in processed_seo_keywords:
        #                 # print("no processed keywords")
        #                 processed_seo_keywords.add(ProductSEOkeyword)
        #                 individualItemRequest = F"{self.homeURL}{ProductSEOkeyword}-p{SEOProductID}.html?v1={DiscerningProductID}&v2={categoryId}&ajax=true"
        #                 # print(individualItemRequest)
        #             #    https://www.zara.com/ww/en/textured-round-neck-blazer-p02254187.html?v1=367663930&v2=2352684&ajax=true

        #             #     # productURL = f"{self.product_api_url}/{redirectcategoryID}/products?ajax=true"
        #                 yield Request(
        #                     url=individualItemRequest,
        #                     method='GET',
        #                     # body=json.dumps(payload),
        #                     callback=self.custom_Request_level_3,
        #                     meta={
        #                         'categoryName': category_title,
        #                         "subcategoryname": sub_category_title,
        #                     # 'params': params,
        #                         # "categoryID": redirectcategoryID
        #                     }         
        #                 )
        

    def extract_json_from_response(self, response_text):
        # Use regular expression to find JSON content
        categoryname = response.meta['categoryName']
        SubcategoryName = response.meta['subcategoryname']
        son_match = re.search(r'\{.*\}', response_text)
        if json_match:
            # Extract the matched JSON string
            json_str = json_match.group(0)
            # Parse the JSON string
            json_data = json.loads(json_str)
            return json_data
        else:
            print("No JSON content found in the response.")
            return None

    def custom_Request_level_3(self, response):
        # print(response.url)
        product_item = ProductItem()
        categoryname = response.meta['categoryName']
        SubcategoryName = response.meta['subcategoryname']
        # json_text = response.body
        # json_Response = self.extract_json_from_response(json_str)
        # print(response.url)
        # {"noIndex":true,"mkSpots":{"ESpot_Copyright":{"key":"ESpot_Copyright","content":{"content":"<span class='zds-body-s'>©
        product_item['CategoryTitle'] = categoryname
        product_item['subcategoryTitle'] = SubcategoryName
        sizerange = []
        json_str = response.body.decode('utf-8')
        start_index = json_str.find('<script')
        end_index = json_str.find('</script>') + len('</script>')
        productsize = []
        productimages=[]
        if start_index != -1 and end_index != -1:
        # Remove the JavaScript code from the JSON string
            json_str = json_str[:start_index] + json_str[end_index:]
            # print(json_str)

        # try:
            # json_response = json.loads(json_str)
            # Write JSON data to a file
            # with open("abc.json", 'a') as file:
                # json.dump(json_response, file, indent=4)
        # except json.decoder.JSONDecodeError as e:
            # print("Error decoding JSON:", e)
            json_data = json.loads(json_str)
        #   json_data['content'] = json_data['content'].replace('\n', '').replace('\\"', '"').replace('\\', '')
            # with open("abc.json", 'a') as file:
            #   json.dump(json_data, file, indent=4)
            # product_details = 
            # print(product_details)
            # with open("product_details.json", 'a') as file:
            #   json.dump(product_details, file, indent=4)
            ItemURL = ""
            Itemname = ""
            Itemprice = ""
            Itemcolour = ""
            ItemColour = []
            colourcode = []
            colourcode_set = set()
            productnamedetail = json_data.get('product', {})
            productmetadata = json_data.get('productMetaData', [{}])
            for productmeta in productmetadata:
                ItemURL = productmeta.get('url')
                Itemname = productmeta.get('name')
                Itemprice = productmeta.get('price')
                Itemcolour = productmeta.get('colorName')
                colourcode_set.add(Itemcolour)
                # colourcode = list(colourcode_set)
                
                # break
            colourcode = list(colourcode_set)
            print(f"following are the colours for the item{colourcode}")
            
            product_item['ItemTitle']=Itemname
            product_item['ItemPrice']=f"{Itemprice} AED"
            product_item['ItemURL']=ItemURL
            product_item['ItemColour'] = colourcode
            
            # print(f"following is the Item URL {ItemURL}")
            if productnamedetail:                                 
                
                
            
                # product_item['ItemTitle'] = Itemname
                productgenericdetails =productnamedetail.get('detail',{})
                # productURLdetails =productURLdetail.get('',{})
                
                
                if productgenericdetails:
                    productdetails =  productgenericdetails.get('colors', [])
                    
                    for detail in productdetails:
                        # Itemprice = detail.get('price')
                        # product_item['ItemPrice'] = Itemprice
                        # Itemcolour = detail.get('name')
                        # ItemColour.append(Itemcolour)
                        # print(ItemColour)
                    # print(f"Colours are: {Itemcolour}")
                        # product_item['ItemColour'] = Itemcolour
                        
                        Itemdescription = detail.get('description')
                        
                        product_item['ItemDescription'] = Itemdescription
                        sizes = detail.get('sizes', [{}])
                        images = detail.get('mainImgs', [{}])
                        for index, size in enumerate(sizes,start=1):
                            sizeguide = size.get('name')
                            # productsize.append(sizeguide)
                            product_item[f'Size{index}'] = sizeguide
                            
                            # product_item.setdefault('size', []).append(productsize)
                        for image in images:
                            imagekind = image.get('kind')
                            if(imagekind == "plain"):
                                ImageURL = image.get('url')
                                if ImageURL:
                                    product_item.setdefault('image_urls', []).append(ImageURL)
                        # product_item.setdefault('ItemColour', []).append(Itemcolour)
                                # print(Itemname)
            #                     # print(Itemcolour)
            #                     # print(Itemprice)
            #                     # print(Itemdescription)
            #                     # print(ImageURL)
            #                     # print(product_item)
            #                     # break
                    # yield SplashRequest(url= ItemURL, callback= self.IndividualPageParse,  meta={ 'categoryName': categoryname,"subcategoryname": SubcategoryName,"itemname": Itemname, "productsize": productsize, "productimages": productimages })
                            # 'params': params,
                                # "categoryID": redirectcategoryID
                    # print(ItemColour)
                    print(product_item)                        
                    yield product_item
                        
                        # Itemprice = productdetails.get('price')
                # Itemdescription = productdetail.get('description')
                        # print(Itemname)
                        # print(Itemprice)
                        # print(Itemcolour)
                        # print(Itemdescription)
                # print(Itemdescription)
            #     sizes = productdetail.get('sizes')
            #     images = productdetail.get('mainImgs') 
            #     for size in sizes():
            #         sizerange.append(size)

            #     for image in images:
            #         imageset = image.get('set')
            #         if(imageset == 2):
            #             ImageURL = image.get('url')
                        # print(Itemname)
                        # print(Itemprice)
                        # print(Itemdescription)
                        # print(sizerange)
                        # print(ImageURL)
                

            


        # print(response.url)
        # sub_category_title = response.meta.get('subcategrories_title')
        
        
        # json_response = json.loads(response.text)
        # #getting number of pages to control pagination
        # noOfPages = json_response.get('results')[0]["nbPages"]
        
        # api_url = "https://1d2iewlqad-dsn.algolia.net/1/indexes/*/queries"
        # headers = {
        #     "x-algolia-agent": "Algolia for vanilla JavaScript (lite) 3.27.0;instantsearch.js 2.10.3;JS Helper 2.26.0",
        #     "x-algolia-application-id": "1D2IEWLQAD",
        #     "x-algolia-api-key": "87ca3b6b2ce56f0bb76fc194a8d170e2",
        #     "Content-Type": "application/json",  # Specify content type as JSON
        # }
        # payload = {
        #     "requests": [
        #         {
        #             "indexName": "spree_products",
        #             "params": "query=&maxValuesPerFacet=9999&filters=tenant_id%20%3D%201&facets=%5B%22price%22%2C%22taxons_en.lvl0%22%2C%22taxons_en.lvl1%22%2C%22taxons_en.lvl2%22%2C%22taxons_en.lvl3%22%2C%22taxons_en.lvl0%22%2C%22taxons_en.lvl1%22%2C%22taxons_en.lvl2%22%2C%22taxons_en.lvl3%22%5D&tagFilters=",
        #         },
                
        #     ]}
        # page = 0
        # # looping through the every page of the subcategory
        # while(page <= noOfPages):
        #     category_title = response.meta.get('category_title')
        #     sub_category_title = response.meta.get('subcategrories_title')
        #     category_image = response.meta.get("category_image")
        #     #encoding the category and subcategory title to add in the api request
        #     encoded_category_title = quote(category_title)
        #     encoded_sub_category_title = quote(sub_category_title)
        #     params = payload["requests"][0]["params"]
        #     params += f"&facetFilters=%5B%5B%22taxons_en.lvl2%3ADepartments%20%3E%20{encoded_category_title}%20%3E{encoded_sub_category_title}%22%5D%5D"
        #     # getting products from every page
        #     # updating the page number
        #     params += f"&page={page}"
        #     updated_payload = payload.copy()
        #     updated_payload["requests"][0]["params"] = params
        #     page += 1
        #     yield Request(
        #         url=api_url,
        #         method='POST',
        #         headers=headers,
        #         body=json.dumps(payload),
        #         callback=self.parse_api_response_level_3,
        #         meta={ 
        #         'category_title': category_title,
        #         "subcategrories_title": sub_category_title,
        #         'params': params,
        #         "category_image": category_image
        #         }
        #     ) 

    def IndividualPageParse(self, response):
        print(response.url)
        colourcode = []
        categoryname = response.meta['categoryName']
        SubcategoryName = response.meta['subcategoryname']
        itemname= response.meta['itemname']
        productsize = response.meta['productsize']
        productimages = response.meta['productimages']
        # itemprice = response.css("article > div > div.product-detail-view__main > div.product-detail-view__side-bar > div > div.product-detail-info__info > div.product-detail-info__price > div > span > span > span > div > span::text").get()
        itemcolours = "div.product-detail-color-selector > div > ul >li"
        for li in response.css(itemcolours):
            colour = li.css("button > div.product-detail-color-selector__color-area > span::text").get()
            colourcode.append(colour)
        
        
        print(f"categoryname = {categoryname}")
        # print(f"following si the price for item{itemprice}")
        print(f"Subcategoryname = {SubcategoryName}")
        print(f"Itemname = {itemname}")
        print(f"product sizes are = {productsize}")
        print(f"product Images are  = {productimages}")

    def parse_api_response_level_3(self, response):
        json_response = json.loads(response.text)
        category_title = response.meta['category_title']
        subcategrories_title =response.meta['subcategrories_title']
        category_item = StoreItem()
        category_item['CategoryTitle'] = category_title
        category_item['categoryImage'] = response.meta.get("category_image")
        category_item['Subcategories'] = []
        subcategories = []
        for result in json_response.get("results",[]):
          
           hit_counter = 0  # Initialize a counter
           #getting product items
           for hit in result.get("hits",[]):
               
                
                product_item = ProductItem()
                product_item["ItemTitle"] = hit.get("full_name_en")
                customimages = hit.get("image")
                product_item["image_urls"] = customimages
                checkOnSale = hit.get("on_sale")
                if(checkOnSale):

                    product_item["ItemSalesPrice"] = hit.get("price")
                else :
                    
                    product_item["ItemPrice"] = hit.get("price")
                
                subcategories.append(product_item)
                hit_counter +=1
        subcat_item = SubcategoryItem()
        subcat_item['subcategoryTitle'] = subcategrories_title
        subcat_item['productItems'] = subcategories
        category_item['Subcategories'].append(subcat_item)
        yield category_item        

  