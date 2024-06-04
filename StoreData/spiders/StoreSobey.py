import scrapy
import json
from scrapy.crawler import CrawlerProcess
from scrapy_splash import SplashRequest 
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.images import ImagesPipeline
from urllib.parse import unquote, urljoin, quote
from scrapy import Request

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
    images = scrapy.Field()

class DataStoreSpider(scrapy.Spider):
    name = "datasobey-spider"
    homeURL = "https://danube.sa/"
    subcat_item = SubcategoryItem()
    
    custom_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
    'Sec-Ch-Ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    # ... any other headers you want to include ...
    }
        
    custom_cookies = {
        "danube_district_id": "40",
        "show_app_popover": "false",
        "algolia_user_token": "anonymous-a01edb64-0501-46b6-adf2-e294c5cd9604",
        "show_store_selector": "false",
        "_danube_session": "bDd0dXhQTXZLVDQ3dWpwbUY0dTZzYVg2SFdEaVJFUTJiQ2R5OXFGTVVKWWh0UE5xR01TM1E5a2JKUGdrajZuV1pPVkZ2Y201eGdobEpURml1RmRrb1VDVHNXRDVMTERMNnY4NXJVS0dQbkVNbjNzMHNhL0RLdXlJYXl5QnRNOXB2UFdDcHNVMTJnblVlRkZXU0Jsemh3PT0tLUo5Z0tOVzhhSDk2UHBPUGgxRlk4eHc9PQ%3D%3D--245d0d410a68c2451bf133d9ea4d4845c1b81e2c"
    } 


    def start_requests(self):
        # Define a URL for an external IP address checker service
        url = 'https://danube.sa/en/departments'

        # Make a request to the external service
        yield scrapy.Request(url, self.parse, cookies=self.custom_cookies, headers = self.custom_headers)
    #parsing level 1 categories
    def parse(self, response):
        
        #need these selectors to in order to test dont remove
        # childSelector = "div.danube-5-cols-md"
        # elements = response.xpath('//*[@id="wrapper"]/div[contains(@class, "container")]/div[contains(@class, "row--departments")]/div[contains(@class, "danube-5-cols-md")][2]')
        elements = response.css("#wrapper > div.container.department-page > div.row.row--departments > div.danube-5-cols-md")
       
        for element in elements:
           
            category_title= element.css(f"div.department-box__inner-container > div.department-box__title::text").get()
            print(category_title)
            imageUrl = element.css(f"div.department-box__image::attr(style)").get()
            category_image = imageUrl.split("url(")[-1].strip(");")
            print(category_image)
            CategoryLink = element.css(f"div.department-box__inner-container > a.department-box__all-link::attr(href)").get()
            print(CategoryLink)
            # # Subcategories = []
            if CategoryLink and CategoryLink != '#':
                absolute_url = urljoin(self.homeURL, CategoryLink)
                print("absolute URL\n")
                print(absolute_url)
                if absolute_url:
                    yield scrapy.Request(url= absolute_url,callback = self.CustomRequest, cookies = self.custom_cookies, headers = self.custom_headers, meta={'category_title': category_title, "category_image":category_image} )
    #  creating and sending request to individual categories          
    def CustomRequest(self, response):
        
        api_url = "https://1d2iewlqad-dsn.algolia.net/1/indexes/*/queries"
        headers = {
            "x-algolia-agent": "Algolia for vanilla JavaScript (lite) 3.27.0;instantsearch.js 2.10.3;JS Helper 2.26.0",
            "x-algolia-application-id": "1D2IEWLQAD",
            "x-algolia-api-key": "87ca3b6b2ce56f0bb76fc194a8d170e2",
            "Content-Type": "application/json",  # Specify content type as JSON
        }
        payload = {
            "requests": [
                {
                    "indexName": "spree_products",

                    "params": "query=&maxValuesPerFacet=9999&page=0&filters=tenant_id%20%3D%201&facets=%5B%22price%22%2C%22taxons_en.lvl0%22%2C%22taxons_en.lvl1%22%2C%22taxons_en.lvl2%22%2C%22taxons_en.lvl0%22%2C%22taxons_en.lvl1%22%2C%22taxons_en.lvl2%22%5D&tagFilters=",
                },
                # ... other request dictionaries ...
            ]}
        category_title = response.meta.get('category_title')
        category_image = response.meta.get("category_image")
        encoded_category_title = quote(category_title)
        params = payload["requests"][0]["params"]
        #encoding category title 
        params += f"&facetFilters=%5B%5B%22taxons_en.lvl1%3ADepartments%20%3E%20{encoded_category_title}%22%5D%5D"
        updated_payload = payload.copy()
        # Update the 'params' field in the first request dictionary
        updated_payload["requests"][0]["params"] = params
        
        #sending request to get level2 categories
        yield Request(
            url=api_url,
            method='POST',
            headers=headers,
            body=json.dumps(payload),
            callback=self.parse_api_response,
            meta={
            'category_title': category_title,
            "category_image": category_image,
            'params': params
            }
        )
    # parsing the level2 categories
    def parse_api_response(self, response):
        headers = {
            "x-algolia-agent": "Algolia for vanilla JavaScript (lite) 3.27.0;instantsearch.js 2.10.3;JS Helper 2.26.0",
            "x-algolia-application-id": "1D2IEWLQAD",
            "x-algolia-api-key": "87ca3b6b2ce56f0bb76fc194a8d170e2",
            "Content-Type": "application/json",  # Specify content type as JSON
        }
        json_response = json.loads(response.text)
        
        category_title = response.meta.get('category_title')
        category_image = response.meta.get("category_image")
        params = response.meta.get('params')
        new_url ="https://danube.sa/en/departments/meat-poultry-seafood"
        
        # getting the subcategories response
        for result in json_response.get('results', []):
            #list to store all level 2 categories in 1 level 1 category
            found_keys = []
            
            for facet in result.get('facets', []):
            
                if facet in ["price", "taxons_en.lvl0", "taxons_en.lvl1", "taxons_en.lvl2"]:
                    facet_data = result['facets'][facet]
                    
                    target_key = None
                    if isinstance(facet_data, dict):
                        for key, value in facet_data.items():
                            if category_title in key:
                                # if  in taxons.get:
                                parts = key.split(f" > {category_title} >" )
                                if len(parts) >= 2:
                                    target_key = parts[-1]
                                    found_keys.append(target_key)
                                   
            # # Your logic here...
                    if found_keys:
                        for key in found_keys:
                            print(category_title)
                            print(key)
                            #sending request to level 2 categories
                            yield  scrapy.Request(
                                new_url,
                                
                                self.customSubCategoriesRequest,
                                meta={
                                    "category_title": category_title,
                                    "sub_category": key,
                                    'category_image': category_image
                                }
                            )   
                    else:
                        print("No Target Keys found") 
    #this method send a request to each level2 category to send to get the total pages
    def customSubCategoriesRequest(self,response):
        api_url = "https://1d2iewlqad-dsn.algolia.net/1/indexes/*/queries"
        headers = {
            "x-algolia-agent": "Algolia for vanilla JavaScript (lite) 3.27.0;instantsearch.js 2.10.3;JS Helper 2.26.0",
            "x-algolia-application-id": "1D2IEWLQAD",
            "x-algolia-api-key": "87ca3b6b2ce56f0bb76fc194a8d170e2",
            "Content-Type": "application/json",  # Specify content type as JSON
        }
        payload = {
            "requests": [
                {
                    "indexName": "spree_products",
                    "params": "query=&maxValuesPerFacet=9999&page=0&filters=tenant_id%20%3D%201&facets=%5B%22price%22%2C%22taxons_en.lvl0%22%2C%22taxons_en.lvl1%22%2C%22taxons_en.lvl2%22%2C%22taxons_en.lvl3%22%2C%22taxons_en.lvl0%22%2C%22taxons_en.lvl1%22%2C%22taxons_en.lvl2%22%2C%22taxons_en.lvl3%22%5D&tagFilters=",
                },
                
            ]}
        category_title = response.meta.get('category_title')
        sub_category_title = response.meta.get('sub_category')
        category_image = response.meta.get("category_image")
        encoded_category_title = quote(category_title)
        encoded_sub_category_title = quote(sub_category_title)

        params = payload["requests"][0]["params"]
        params += f"&facetFilters=%5B%5B%22taxons_en.lvl2%3ADepartments%20%3E%20{encoded_category_title}%20%3E{encoded_sub_category_title}%22%5D%5D"
        updated_payload = payload.copy()
        updated_payload["requests"][0]["params"] = params

        yield Request(
            url=api_url,
            method='POST',
            headers=headers,
            body=json.dumps(payload),
            callback=self.custom_Request_level_3,
            meta={
            'category_title': category_title,
            "subcategrories_title": sub_category_title,
            'params': params,
            "category_image": category_image
            }
        ) 


       

                   
    def custom_Request_level_3(self, response): 
        
        
        
        json_response = json.loads(response.text)
        noOfPages = json_response.get('results')[0]["nbPages"]
        

        # Serialize the combined data list and write it to the JSON file
        # with open(output_file_path, 'w') as file:
        #     json.dump(json_response, file, indent=4)   

        # return
        
        api_url = "https://1d2iewlqad-dsn.algolia.net/1/indexes/*/queries"
        headers = {
            "x-algolia-agent": "Algolia for vanilla JavaScript (lite) 3.27.0;instantsearch.js 2.10.3;JS Helper 2.26.0",
            "x-algolia-application-id": "1D2IEWLQAD",
            "x-algolia-api-key": "87ca3b6b2ce56f0bb76fc194a8d170e2",
            "Content-Type": "application/json",  # Specify content type as JSON
        }
        payload = {
            "requests": [
                {
                    "indexName": "spree_products",
                    "params": "query=&maxValuesPerFacet=9999&filters=tenant_id%20%3D%201&facets=%5B%22price%22%2C%22taxons_en.lvl0%22%2C%22taxons_en.lvl1%22%2C%22taxons_en.lvl2%22%2C%22taxons_en.lvl3%22%2C%22taxons_en.lvl0%22%2C%22taxons_en.lvl1%22%2C%22taxons_en.lvl2%22%2C%22taxons_en.lvl3%22%5D&tagFilters=",
                },
                
            ]}
            
        for page in range(noOfPages):
            
            
            category_title = response.meta.get('category_title')
            sub_category_title = response.meta.get('subcategrories_title')
            print(f"page {page} of {sub_category_title}")
            category_image = response.meta.get("category_image")
            encoded_category_title = quote(category_title)
            encoded_sub_category_title = quote(sub_category_title)
            params = payload["requests"][0]["params"]
            print(f"encoded {encoded_sub_category_title}")
            print(encoded_category_title)
            params += f"&facetFilters=%5B%5B%22taxons_en.lvl2%3ADepartments%20%3E%20{encoded_category_title}%20%3E{encoded_sub_category_title}%22%5D%5D"
            # getting products from every page
            # updating the page number
            params += f"&page={page}"


            updated_payload = payload.copy()
            updated_payload["requests"][0]["params"] = params

            print(f"Updated Params: {params}")
            

            yield Request(
                url=api_url,
                method='POST',
                headers=headers,
                body=json.dumps(payload),
                callback=self.parse_api_response_level_3,
                meta={
                'category_title': category_title,
                "subcategrories_title": sub_category_title,
                'params': params,
                "category_image": category_image
                }
            ) 
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

  