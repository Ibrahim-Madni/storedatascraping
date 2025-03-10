import scrapy
import json
import re
import csv
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
    ItemPrice = scrapy.Field()
    ItemSalePrice = scrapy.Field()
    ItemUnit = scrapy.Field()
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

class DataStoreSpider(scrapy.Spider):
    name = "logoimages"
    allowed_domains = ["gettyimages.com", "https://www.gettyimages.com/", "www.gettyimages.com/", "localhost"]

    homeURL = "https://www.gettyimages.com"
    subcat_item = SubcategoryItem()
    product_api_url = "https://www.gettyimages.com/search/2/image-film?phrase=Lululemon%20logo&sort=best"
    
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
        
        # for page in range(1, 35):
        url = 'https://www.gettyimages.com/search/2/image?phrase=apple%20logo&family=editorial'
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
        # print(response.url)
        # gallery-items-container
        # for imageURLS in response.css("div[data-testid='gallery-items-container']"):
        product_item = response.meta.get('item', ProductItem())

        # image_urls = []
            # imagereferenceLinks = response.css("a > figure > picture > img::attr(src)").getall()
        # https://www.gettyimages.com/search/2/image?family=editorial&phrase=dior%20brand%20logo&sort=mostpopular
        # nextpageurl = "https://www.gettyimages.com/search/2/image-film?phrase=uniqlo%20logo&sort=best&page=2"
        nextpageurl = response.css("a[data-testid='pagination-button-next']::attr(href)").get()
        if nextpageurl:
            completenextpageurl = f"{self.homeURL}{nextpageurl}"
        else:
            completenextpageurl = None
        # completenextpageurl = f"{self.homeURL}{nextpageurl}"
        gallerycont = "div[data-testid = 'gallery-items-container'] > div.vItTTzk8rQvUIXjdVfi4"

        for gallery in response.css(gallerycont):
            print(gallery)
            imagereferenceLinks = gallery.css("article.KMczDbsqNlj9Y2shxCNZ > a > figure > picture > img::attr(src)").get()            
            # print(imagereferenceLinks)
        #     if imagereferenceLinks:
                
        #         product_item.setdefault('image_urls', []).append(imagereferenceLinks)
        #         # numberofproductitemsperpage = len(product_item['image_urls'])
        #         # print(f"The total number of product items per page are {numberofproductitemsperpage}")
        #             # print(product_item)
        # if completenextpageurl:

        #     yield scrapy.Request(completenextpageurl, callback=self.CustomRequest, meta={'item': product_item})
        # else:
        #     # numberofproductitems = len(product_item['image_urls'])
        #     # print(f"The total number of product items are {numberofproductitems}")
            

        #     yield(product_item)
        #     # with open('output_file.csv', 'a', newline='') as f:
            #     writer = csv.writer(f)
            # If needed, write headers (only once, outside of loop)
            # writer.writerow(product_item.keys())
            
            # Write the values for each product item
                # writer.writerow(product_item.values())
        
        # print(product_item)
        
            # print(product_item)
            # yield product_item
                
                # image_urls.append(imagereferenceLinks)
                # print(image_urls)
        
        # yield  scrapy.Request(url= completenextpageurl, callback= self.parse_nextpageimages ,meta={'image_urls': image_urls})
    
    def parse_nextpageimages(self, response):
        print(response.url)
        # image_next_urls = response.meta.get('image_urls')
        # # print(image_urls
        # image_urls_next=[]
        # image_urls_next.append(image_urls)
        # image_urls_next.append(image_next_urls)
        nextpageurl = response.css("a[data-testid='pagination-button-next']::attr(href)").get()
        # print(nextpageurl)
        completenextpageurl = f"{self.homeURL}{nextpageurl}"
        gallerycont = "a > figure > picture > img"
        for gallery in response.css(gallerycont):
            imagereferenceLinks = gallery.css("::attr(src)").get()            
            if imagereferenceLinks:
                image_urls.append(imagereferenceLinks)
                # print(image_urls)

        # for page in range(3, 9):
        #     productURL = f"https://www.gettyimages.com/search/2/image-film?phrase=uniqlo%20logo&sort=best&page={page}"
        #     # print(image_urls_next)
            if nextpageurl:
                yield  scrapy.Request(url= completenextpageurl, callback= self.parse_nextpageimages ,meta={'image_urls': image_urls})
        product_item['image_urls']=image_urls
        # print(product_item)
        yield(product_item) 
    
    def parse_api_response(self, response):
        # print(response.body)
        # headers = {
        #     "x-algolia-agent": "Algolia for vanilla JavaScript (lite) 3.27.0;instantsearch.js 2.10.3;JS Helper 2.26.0",
        #     "x-algolia-application-id": "1D2IEWLQAD",
        #     "x-algolia-api-key": "87ca3b6b2ce56f0bb76fc194a8d170e2",
        #     "Content-Type": "application/json",  # Specify content type as JSON
        # }
        json_response = json.loads(response.text)
        # print(json_response)
        # category_title = response.meta.get('category_title')
        # category_image = response.meta.get("category_image")
        # params = response.meta.get('params')
        # new_url ="https://danube.sa/en/departments/meat-poultry-seafood"
        # with open("abc.json", 'a') as file:
        #     json.dump(json_response, file, indent=4)   
        # # getting the subcategories response
        # found_keys = []
        for result in json_response.get('categories', []):
            # print(result)
        #     #list to store all level 2 categories in 1 level 1 category
            # https://www.zara.com/ww/en/satin-shirt-p02248802.html?v1=355842665&v2=2352904&ajax=true
            CategoryID = result.get('id')
            categoryName = result.get('name')
            print(f"{categoryName} : {CategoryID}")
            
            # https://www.zara.com/ww/en/categories?categoryId=2352684&categorySeoId=1055&ajax=true
            for facet in result.get('subcategories', [{}]):
                subcategoryID =facet.get('id')
                temporarysubcatName = facet.get('name')
                redirectcategoryID = facet.get('redirectCategoryId')
                actualsubcategoryName = re.sub(r'\s+', '', temporarysubcatName)

                

                
                seocategoryID = facet.get('seo', {}).get('seoCategoryId')
                # print(f"{actualsubcategoryName} : {subcategoryID} , {redirectcategoryID}, {seocategoryID}")
                if redirectcategoryID and seocategoryID:
                    productURL = f"{self.product_api_url}/{redirectcategoryID}/products?ajax=true"
                    yield Request(
                        url=productURL,
                        method='GET',
                        # body=json.dumps(payload),
                        callback=self.SubcategoryURLParse,
                        meta={
                            'categoryName': categoryName,
                            "subcategoryname": actualsubcategoryName,
                            # 'params': params,
                            "categoryID": redirectcategoryID
                        }         
                    )
                # print(f"subcategoryName + {actualsubcategoryName}" )
                # print(f"redirectcategoryid + {redirectcategoryID}" )
                # print(facet)
            # 
        #         if facet in ["price", "taxons_en.lvl0", "taxons_en.lvl1", "taxons_en.lvl2"]:
        #             facet_data = result['facets'][facet]
                    
        #             target_key = None
        #             if isinstance(facet_data, dict):
        #                 for key, value in facet_data.items():
        #                     if category_title in key:
        #                         # if  in taxons.get:
        #                         parts = key.split(f" > {category_title} >" )
        #                         if len(parts) >= 2:
        #                             target_key = parts[-1]
        #                             found_keys.append(target_key)
        # print(f"{category_title} and found keys {found_keys}")                          
        # # # Your logic here...
        # counter = 0
        # if found_keys:
        #     #if there are subcategories the send go in to the custom categories
        #     for key in found_keys:

        #         if(key == " Milk \\ Milk Alternatives"):
        #             yield  scrapy.Request(
        #             new_url,
                    
        #             self.customSubCategoriesRequest,
        #             meta={
        #                 "category_title": category_title,
        #                 "sub_category": "Milk \\ Milk Alternatives",
        #                 'category_image': category_image
        #             })   
        #         else:
        #             yield  scrapy.Request(
        #             new_url,
                    
        #             self.customSubCategoriesRequest,
        #             meta={
        #                 "category_title": category_title,
        #                 "sub_category": key,
        #                 'category_image': category_image
        #             }
        #         ) 
               
        #         #sending request to level 2 categories
                  
        # else:
        #     print("no keys found")
            #  

    #this method send a request to each level2 category to send to get the total pages
    def SubcategoryURLParse(self,response):
        category_title = response.meta.get('categoryName')
        sub_category_title = response.meta.get('subcategoryname')
        categoryId = response.meta.get('categoryID')
        json_response = json.loads(response.text)
        processed_seo_keywords = set()
        product_groups = json_response.get('productGroups', [])
        for group in product_groups:
            elements = group.get('elements', [])
            for element in elements:
                commercial_components = element.get('commercialComponents', [])
                for component in commercial_components:
                    # marketingmetainfo = component.get('marketingMetaInfo',{})
                    # if not isinstance(marketingmetainfo, list):
                        # marketingmetainfo = [marketingmetainfo] 
                    # for marketmeta in marketingmetainfo:
                        # mappinginfo = marketmeta.get('mappingInfo', [])
                        # for mapping in mappinginfo:
                            # regions = mapping.get("regions", [])
                            # for region in regions:
                                # area_link = region.get('areaLink', {})
                                # mainlink = area_link.get('url')
                                # endpoint = area_link.get('queryParams')
                                # print(mainlink)
                                # print(endpoint)


                    seo = component.get('seo', {})
                    ProductSEOkeyword = seo.get('keyword')
                    SEOProductID = seo.get('seoProductId')
                    DiscerningProductID = seo.get('discernProductId')
                    # print(f"{ProductSEOkeyword} : SEOID = {SEOProductID} , Discerning ID {DiscerningProductID}")
                    if ProductSEOkeyword not in processed_seo_keywords:
                        # print("no processed keywords")
                        processed_seo_keywords.add(ProductSEOkeyword)
                        individualItemRequest = F"{self.homeURL}{ProductSEOkeyword}-p{SEOProductID}.html?v1={DiscerningProductID}&v2={categoryId}&ajax=true"
                        # print(individualItemRequest)
                    #    https://www.zara.com/ww/en/textured-round-neck-blazer-p02254187.html?v1=367663930&v2=2352684&ajax=true

                    #     # productURL = f"{self.product_api_url}/{redirectcategoryID}/products?ajax=true"
                        yield Request(
                            url=individualItemRequest,
                            method='GET',
                            # body=json.dumps(payload),
                            callback=self.custom_Request_level_3,
                            meta={
                                'categoryName': category_title,
                                "subcategoryname": sub_category_title,
                            # 'params': params,
                                # "categoryID": redirectcategoryID
                            }         
                        )
        

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
            productnamedetail = json_data.get('product', {})
            if productnamedetail:                                 
                Itemname = productnamedetail.get('name')
                product_item['ItemTitle'] = Itemname
                productgenericdetails =productnamedetail.get('detail',{})
                itemColour = []
                if productgenericdetails:
                    productdetails =  productgenericdetails.get('colors', [{}])
                    
                    for detail in productdetails:
                        Itemprice = detail.get('price')
                        product_item['ItemPrice'] = Itemprice
                        Itemcolour = detail.get('name')
                        # product_item['ItemColour'] = Itemcolour
                        product_item.setdefault('ItemColour', []).append(Itemcolour)
                        Itemdescription = detail.get('description')
                        product_item['ItemDescription'] = Itemdescription
                        sizes = detail.get('sizes', [{}])
                        images = detail.get('mainImgs', [{}])
                        for index, size in enumerate(sizes,start=1):
                            productsize = size.get('name')
                            product_item[f'Size{index}'] = productsize
                            
                            # product_item.setdefault('size', []).append(productsize)
                        for image in images:
                            imagekind = image.get('kind')
                            if(imagekind == "other"):
                                ImageURL = image.get('url')
                                if ImageURL:
                                    product_item.setdefault('image_urls', []).append(ImageURL)
                                # print(Itemname)
                                # print(Itemcolour)
                                # print(Itemprice)
                                # print(Itemdescription)
                                # print(ImageURL)
                                # print(product_item)
                                # break
                    
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
            #             print(Itemname)
            #             print(Itemprice)
            #             print(Itemdescription)
            #             print(sizerange)
            #             print(ImageURL)
                

            


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

  