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
    name = "zara_store_individual_scraper"
    homeURL = "https://www.zara.com/ae/en/"
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
    start_urls = ["https://www.zara.com/ae/en/oversize-twill-trench-coat-p01437305.html?v1=383069783",
"https://www.zara.com/ae/en/structured-wool-cardigan-p02893361.html?v1=389488468",
"https://www.zara.com/ae/en/basic-slim-fit-t-shirt-p05584360.html?v1=389573807",
"https://www.zara.com/ae/en/basic-jogger-trousers-p00761332.html?v1=407839230",
# "https://www.zara.com/ae/en/basic-jogger-trousers-p06543219.html",
"https://www.zara.com/ae/en/basic-jogger-trousers-p00761332.html?v1=386685343",
"https://www.zara.com/ae/en/basic-slim-fit-t-shirt-p05584360.html?v1=389573807",
"https://www.zara.com/ae/en/basic-slim-fit-t-shirt-p05584360.html?v1=389573807",
"https://www.zara.com/ae/en/basic-hoodie-p00761330.html?v1=407839228",
"https://www.zara.com/ae/en/sweatshirt-with-printed-slogan-p06224369.html?v1=388537345",
"https://www.zara.com/ae/en/relaxed-fit-cargo-trousers-p06786301.html?v1=403895021",
"https://www.zara.com/ae/en/cargo-denim-trousers-with-pockets-p05575304.html?v1=382674703",
"https://www.zara.com/ae/en/denim-jacket-with-pockets-p04365408.html?v1=396965327",
"https://www.zara.com/ae/en/quilted-bomber-jacket-p03046520.html?v1=389561756",
"https://www.zara.com/ae/en/slim-fit-jeans-p03991340.html?v1=388283436",
"https://www.zara.com/ae/en/skinny-fit-chino-trousers-p06786405.html?v1=375204098",
"https://www.zara.com/ae/en/baggy-fit-jeans-p08062380.html?v1=415981675",
"https://www.zara.com/ae/en/textured-cotton-sweater-p04696310.html?v1=403268597",
"https://www.zara.com/ae/en/textured-training-t-shirt-p04387312.html?v1=413846328",
"https://www.zara.com/ae/en/2-in-1-training-shorts-p01943320.html?v1=364562843",
"https://www.zara.com/ae/en/basic-training-t-shirt-p04387401.html?v1=380981871",
"https://www.zara.com/ae/en/basic-textured-sweater-p03332320.html?v1=388987366",
"https://www.zara.com/ae/en/basic-textured-sweater-p03332320.html?v1=388987366",
"https://www.zara.com/ae/en/basic-textured-sweater-p03332320.html?v1=388987366",
"https://www.zara.com/ae/en/wool-twill-suit-trousers-p06775206.html?v1=404062145",
"https://www.zara.com/ae/en/oversize-fit-jacket-p02668360.html?v1=413808966",
"https://www.zara.com/ae/en/colour-block-technical-jacket-p03918418.html?v1=397808549",
"https://www.zara.com/ae/en/tie-dye-print-sweatshirt-p04393417.html?v1=417501985",
"https://www.zara.com/ae/en/faded-cargo-bermuda-shorts-p05862429.html?v1=371007225",
"https://www.zara.com/ae/en/cargo-parachute-trousers-p06786303.html?v1=392930424",
"https://www.zara.com/ae/en/textured-sweater-p05755358.html?v1=386723588",
"https://www.zara.com/ae/en/contrast-twill-trousers-p04042028.html?v1=412097878",
"https://www.zara.com/ae/en/textured-chino-bermuda-shorts-p08727425.html?v1=380982279",
"https://www.zara.com/ae/en/baggy-fit-bermuda-jorts-p05575498.html?v1=388190707",
"https://www.zara.com/ae/en/100-linen-bermuda-shorts-p09621003.html?v1=364113492",
"https://www.zara.com/ae/en/cotton---linen-shirt-p01063402.html?v1=364086315",
"https://www.zara.com/ae/en/textured-weave-knit-shirt-p09598319.html?v1=366155562",
"https://www.zara.com/ae/en/oversized-denim-shirt-with-pockets-p03991301.html?v1=364092475",
"https://www.zara.com/ae/en/western-denim-shirt-p01063308.html?v1=373211505",
"https://www.zara.com/ae/en/textured-shirt-p05569812.html?v1=370069147",
"https://www.zara.com/ae/en/compression-training-t-shirt-p01943303.html?v1=387272143",
"https://www.zara.com/ae/en/hooded-down-jacket-p04695314.html?v1=435659250",
"https://www.zara.com/ae/en/running-training-shorts-p01943302.html?v1=372742458",
"https://www.zara.com/ae/en/mesh-textured-shorts-p06096310.html?v1=386924324",
"https://www.zara.com/ae/en/mesh-textured-shorts-p06096300.html?v1=364107406",
"https://www.zara.com/ae/en/skinny-fit-chino-trousers-p06786405.html?v1=375204098",
"https://www.zara.com/ae/en/slim-fit-jeans-p05585320.html?v1=416700747",
"https://www.zara.com/ae/en/polo-sweatshirt-p01501504.html?v1=405849910",
"https://www.zara.com/ae/en/cropped-polo-sweatshirt-p00761307.html?v1=391007376"]
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
    new_cookies = {
        "rid": "1b551eb7-472f-4bc0-8e33-4b8ee0201702",
    "optimizelyEndUserId": "oeu1718121224659r0.6818106508794575",
    "UAITXID": "65509b2f523e6ed59eeb0c2eb89361636ec9c9abf377f0d8b863deb2f786209d",
    "ITXDEVICEID": "bef8f8873c286ad312bb19ae5377cfd1",
    "bm_lso": "E6EFFCE4280915837DB7FFBF7E1AD2DC3F20CB53408071481D2A0994A19D56A5~YAAQhSg0Fyq6tN+UAQAAHYL/+QJ2jsQ1WvRIcx2bkQedFg6bveEytFHwuuAuq96zq8h8OHcoLskzxfNgNERfYUpx2L+qZ27Um0N8s9oWvKV8dN0i7VkYO7uubqj6UTqyAfAjCof2wm4FARyueJrgxhNJYlYsSzjE+ivz+axsNfUw+LMWLPqilxhLI/bONYwYA3BUz5iWhwbIUoT+fL4+8gvP+qxA0MPRyDdZy8wDp4jktC3eHktXd9PArgrLJCdpSX1TfpjBPhkeePIlYdgUdAJEjauW85+I2XzWoWQpDMzNQpj4k+xnUhdhGe7PjMJV7gp/4Eo817MSEPsTzOrWiOmGkXqpO2r5rw6tQYEH0j6W03R0Fcst3+EdEuCEX1dWd8S+LJ7IrFn3VVHStfKEJ8blrsAY+oIWzMdOjCPMWrHqlly98f8sfkVRUk67LlTOdTzG27NFGUqjfDWgmQ==^1739361060448",
    "foreignRegionConfirmed": "ae",
    "optimizelySession": "0",
    "ITXSESSIONID": "d31a2cdff4711677a4affed3104a9c61",
    "_itxo11y_ses.01fa": "*",
    "cart-was-updated-in-standard": "true",
    "IDROSTA": "5ea3cf939604:1c2e1c796a775429819b833bb",
    "bm_ss": "ab8e18ef4e",
    "826b75e46a856af63aa6a715b40616e7": "08e3a1a9f26f48aa1a58a30a3223bf57",
    "_abck": "E37FB0D80B6F2B5BEC61B32B80EEEDC2~0~YAAQZR0gF32P8SCVAQAAfDCwIw2bHa9Gwlq/OXHQA1jlFs6h+jNCu/eu1AZRDNiVxweGWv4MKKzCJIsqY7CZBQBHGPaf2aRi8Ci4g0d6c/btEjzZbLCv6/oWQdxTFWqF4kPGEyKN6z1BIjFaE24hKhthZfIXGUyh5eZeYnbTDb+IaYhbbNUeoHoLdf+5k08wccmB/UBz0LoyBzuXVZIuJGWyjps3YZ9RXffCI0HW3mfL0NCuPBgDXK9zLquwiIO/CnFqBeGy7Ds51ahEDhvXURJBSQka65OAAb8SNjLzDtL3KIWbdb/gXB4WuqpSSa51SRsadWtu+uvSIeROkfxqX2UfnHPDwiJgqYro2MF0szUW3ARsLxHEl50CWctO/qBnywhM8nqPpIdPKnc9tKQylSOL6XZd7qszhLm+73OJJXlbl0S9f/J3Rid8rVWr~-1~-1~1740064101",
    "bm_mi": "F893E0CC7A1CBEEFED4B7F0E3BF8BE6D~YAAQP9s4fWisSyGVAQAAIyazIxrk6VJ4xMErwcKubWOS7IYdRNG/imcUh9IgsvsFLuHJ8sOwvhMq1fYBJKHG2WW1rXxyOBVEfpUvRBN7Jcd3opNCZ4pBgJNs2FF6Ei7RGTzVHLvVDCAqK/ZIIHV/LVetkNpKX0uGuPJtVTPtzvkUwd6kJamXQ1Cpe/ixYEaqr/36bv9DK8PX7dJ8aZlFLZYQNL/KuDZgig6a63LcTKgQzeYX3Q7HqZJ8llFaz/B70oeZmlD3R/4a+Jb2OaLXsUrFt6ZqBZx21mQQV3rNj6bFZUQYcsIMgim2Ed8aMjTVjoUz/GrPI1XnTR3EmATL9bua8mpaoUVRb1MyrUDdzqGhWOaZn3Jn5OSHx8Vends=~1",
    "bm_sv": "7EF2E17F8C2C069CAF35C1AD7CADF3D4~YAAQP9s4fUStSyGVAQAAciyzIxrwsPG603xuHt7cbiMVZnijqLjTP8X08Jxd2bhch+nUbkloDEf/eHdMBMX7UdkNuZLKQ3s7VcYTpmWNZIKmEdmdvUysiUmHQ+pZKXHCgGNxZzPNFc9cIng+XR8bmDhbjVOZPV7Dwri0A44T1izuEQIZkMZFR6IIrAJ/gsHBXq9Z5ZPM7jSIhAdQPXbx1UGkSj02IkfYGcBXW2SmezeQ+eybKL0Z3PNGiJTJui0=~1",
    "OptanonAlertBoxClosed": "2025-02-20T14:13:52.857Z",
    "OptanonConsent": "isGpcEnabled=0&datestamp=Thu+Feb+20+2025+19%3A13%3A53+GMT%2B0500+(Pakistan+Standard+Time)&version=202501.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=d71e6348-f8a4-4b82-9957-47e32a345b0f&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&geolocation=PK%3BPB&AwaitingReconsent=false&isAnonUser=1",
    "TS0122c9b6": "01d57b118c0a4fa8d01f7bec504c3e134504b0fb746a6f2a1a580069cb863c0f63bc92a2ba585a5c41d4ad64aec34f9a00ecf649d6",
    "_itxo11y_id.01fa": "34318b0e-f452-4cfb-994e-ad1569ee2555.1718121146.29.1740060835.1739449538.b996e1f4-0a37-4afc-ac85-9f6df665d25d.01837f36-5201-489f-928e-52fa2efed413.91eaccf4-b1a7-403d-bb77-0ea709063c7b.1740060500938.59"
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
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.item_buffer = []
    
    # @classmethod
    # def from_crawler(cls, crawler, *args, **kwargs):
    #     spider = super(DataStoreSpider, cls).from_crawler(crawler, *args, **kwargs)
    #     crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
    #     return spider 
    
    # def spider_closed(self, spider):
    #     # This method will be called once the spider finishes scraping
    #     self.log("Spider finished scraping. Now you can trigger the image pipeline.")
    #     for item in self.item_buffer:
    #         yield item  
            
    def start_requests(self):
        # Define a URL for an external IP address checker service
        
        
        for url in self.start_urls:
        # Make a request to the external service
            yield SplashRequest(url, self.CustomRequest, cookies=self.new_cookies)
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
        print(response.body)
        # ProductDescription = response.css("meta[property='og:description']::attr(content)").get()
        # print(ProductDescription)
        # print(f"The response URL is {response.url}")
        
        # with open("response_output.txt", "w", encoding="utf-8") as file:
        #     file.write(response.text)
            # json_response = json.loads(response.text)
            # file.write(json.dumps(json_response, indent=4, ensure_ascii=False))
        # processed_seo_keywords = set()
        # product_groups = json_response.get('productGroups', [])
        # for group in product_groups:
        # print(response.url)
        # print(response.body)
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
            # print(f"The following result should be{result}")
        #     #list to store all level 2 categories in 1 level 1 category
            # https://www.zara.com/ww/en/satin-shirt-p02248802.html?v1=355842665&v2=2352904&ajax=true
            CategoryID = result.get('id')
            categoryName = result.get('name')
            
            
            # https://www.zara.com/ww/en/categories?categoryId=2352684&categorySeoId=1055&ajax=true
            if categoryName != "KIDS" and categoryName != "BEAUTY":
                print(f"{categoryName} : {CategoryID}")
                for facet in result.get('subcategories', [{}]):
                    # for collection in facet.get('', [{}]):
                    collectionID =facet.get('id')
                    temporarycollection = facet.get('name')
                    # actualcollection = re.sub(r'\s+', '', temporarycollection)
                    # print(temporarycollection)
                    possibelsubcats= ['BLAZERS', 'DRESSES' 'TOPS | BODYSUITS', 'T-SHIRTS', 'SHIRTS', 'WAISTCOATS', 'SKIRTS', 'SHORTS | SKORTS', 'TROUSERS', 'JEANS', 'CARDIGANS | SWEATERS', 'JACKETS | TRENCH COATS', 'SWEATSHIRTS | JOGGERS', 'HOODIES | SWEATSHIRTS', 'SUITS', 'SWEATERS | CARDIGANS', 'TRACKSUITS', 'OVERSHIRTS', 'BLAZERS', 'POLO SHIRTS', 'SHORTS'  ]
                    # 
                    if(temporarycollection in possibelsubcats):
                    #     print("I am here")
                        for subcategory in facet.get('subcategories', [{}]):
                            # print(subcategory)
                            if(temporarycollection == "TOPS | BODYSUITS"):
                                temporarycollection = "TOPS AND BODYSUITS"
                            elif(temporarycollection == "SHORTS | SKORTS"):
                                temporarycollection = "SHORTS AND SKORTS"
                            elif(temporarycollection == "CARDIGANS | SWEATERS"):
                                temporarycollection = "CARDIGANS AND SWEATERS"
                            elif(temporarycollection == "JACKETS | TRENCH COATS"):
                                temporarycollection = "JACKETS AND TRENCH COATS"
                            elif(temporarycollection == "SWEATSHIRTS | JOGGERS"):
                                temporarycollection = "SWEATSHIRTS AND JOGGERS"
                            elif(temporarycollection == "HOODIES | SWEATSHIRTS"):
                                temporarycollection = "HOODIES AND SWEATSHIRTS"
                            elif(temporarycollection == "SWEATERS | CARDIGANS"):
                                temporarycollection = "SWEATERS AND CARDIGANS"    
                            else:    
                                temporarysubcategory = subcategory.get('name')
                                print(f"the subcategories are{temporarycollection}")
                                redirectcategoryID = subcategory.get('id')
                                # print(redirectcategoryID)
                                seocategoryID = subcategory.get('seo', {}).get('seoCategoryId')


                        

                        
                        # # seocategoryID = facet.get('seo', {}).get('seoCategoryId')
                                print(f"{temporarycollection} : {redirectcategoryID}, {seocategoryID}")
                                if redirectcategoryID and seocategoryID:
                                    productURL = f"{self.product_api_url}/{redirectcategoryID}/products?ajax=true"
                                    
                                    print(f"The product url is {productURL}")
                                    yield Request(
                                        url=productURL,
                                        method='GET',
                                        # body=json.dumps(payload),
                                        callback=self.SubcategoryURLParse,
                                        meta={
                                            'categoryName': categoryName,
                                            "subcategoryname": temporarycollection,
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
        # print(f"The response url is {response.url}")
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

                    # print(component)
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
        print(f"The response url is {response.url}")
        
        categoryname = response.meta['categoryName']
        SubcategoryName = response.meta['subcategoryname']
        # json_text = response.body
        # json_Response = self.extract_json_from_response(json_str)
        # print(response.url)
        # {"noIndex":true,"mkSpots":{"ESpot_Copyright":{"key":"ESpot_Copyright","content":{"content":"<span class='zds-body-s'>©
     
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

        # try:0
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
            imageURLs = []
            ItemColour = []
            colourcode = []
            colourcode_set = set()
            productnamedetail = json_data.get('product', {})
            productmetadata = json_data.get('productMetaData', [{}])
            # print(productmetadata)
            for productmeta in productmetadata:
                # print(productmeta)
                ItemURL = productmeta.get('url')
                Itemname = productmeta.get('name')
                # Itemname = re.sub(r'\s+', '', Itemname)
                Itemprice = productmeta.get('price')
                ItemDescription = productmeta.get('description')
                # Itemcolour = productmeta.get('colorName')
                images = productmeta.get('mainImgs', [{}])
                # print
                # colourcode_set.add(Itemcolour)
                # colourcode = list(colourcode_set)
                
                # break
            # colourcode = list(colourcode_set)
            # print(f"following are the colours for the item{colourcode}")
            
            # product_item['ItemTitle']=Itemname
            # product_item['ItemPrice']=f"{Itemprice} AED"
            # product_item['ItemURL']=ItemURL
            # product_item['ItemColour'] = colourcode
            
            # print(f"following is the Item URL {ItemURL}")
            ImageURL = ""
            processedimageURLs= []
            processedColours= []
            if productnamedetail:                                 
                
                
            
                # product_item['ItemTitle'] = Itemname
                productgenericdetails =productnamedetail.get('detail',{})
                # productURLdetails =productURLdetail.get('',{})
                
                for productcolour in productgenericdetails.get("colors", []):
                    product_item = ProductItem()
                    processedimageURLs = set()

                    # print(productcolour)
                    # with open("product_details.json", 'a') as file:
                    #         json.dump(productcolour, file, indent=4)
                    
                    productcolourvariant = productcolour.get("name")
                    productcolourID = productcolour.get("id")
                    # print(f"Processing colour: {productcolourvariant}, ID: {productcolourID}")
                    product_item['CategoryTitle'] = categoryname
                    product_item['subcategoryTitle'] = SubcategoryName
                    product_item['ItemTitle']=Itemname
                    product_item['ItemPrice']=f"{Itemprice} AED"
                    product_item['ItemURL']=ItemURL
                    product_item['ItemColour'] = productcolourvariant
                    product_item['ItemDescription'] = ItemDescription
                    product_item['image_urls'] = []
                    for images in productcolour.get('mainImgs',[{}]):
                        imagekind = images.get('kind')
                        imagesourcepath = images.get('path')
                        imageidsource = imagesourcepath.split('/')[-2]
                        if (productcolourID == imageidsource):
                            if(imagekind == "plain"):
                                ImageURL = images.get('url')
                                print(ImageURL)
                                print(productcolourvariant)
                                if ImageURL not in processedimageURLs:

                                    # print(f"is {ImageURL} in {processedimageURLs}")
                                    processedimageURLs.add(ImageURL)
                                    # product_item.setdefault('image_urls', [])
                                    product_item['image_urls'].append(ImageURL)
                    
                        
                    
                    # print(ImageURL)
                    # print(product_item)                    
                    yield product_item
                    
            #         self.item_buffer.append(product_item)
            # return None
                #     # print(productgenericdetails)
                #     # productdetailjson = json.loads(productgenericdetails)
                #     # filename = "genericdetailproducts.json"
                #     # with open(filename, 'wb') as f:
                #     #     f.write(productdetailjson, ensure_ascii=False, indent=4).encode('utf-8')
                #     #     self.log(f'Saved item list elements to {filename}')
                #     productdetails =  productgenericdetails.get('colors', [])
                #     # ProductName =  productgenericdetails.get('name')
                #     # ProductRawPrice =  productgenericdetails.get('price')
                #     # ProductActualPrice =  f"{ProductRawPrice} AED"
                #     # ProductColour =  productgenericdetails.get('colorName')
                #     # ProductDescription =  productgenericdetails.get('description')
                #     # print(f"{ProductName} {ProductActualPrice} {ProductActualPrice}{ProductColour}")
                #     
                #         # print(detail)
                #         # Itemprice = detail.get('price')
                #         product_item['ItemPrice'] = Itemprice
                #         Itemcolour = detail.get('name')
                #         product_item['ItemColour'] = Itemcolour
                #         # ItemColour.append(Itemcolour)
                #         # print(ItemColour)
                #     # print(f"Colours are: {Itemcolour}")
                #         # product_item['ItemColour'] = Itemcolour
                        
                #         Itemdescription = detail.get('description')
                        
                #         product_item['ItemDescription'] = Itemdescription
                        # sizes = detail.get('sizes', [{}])
                        
                        # for index, size in enumerate(sizes,start=1):
                        #     sizeguide = size.get('name')
                        #     # productsize.append(sizeguide)
                        #     product_item[f'Size{index}'] = sizeguide
                            
                            # product_item.setdefault('size', []).append(productsize)
                        # for image in images:
                        #     imagekind = image.get('kind')
                        #     if(imagekind == "plain"):
                        #         ImageURL = image.get('url')
                        #         # print(ImageURL)
                        #         if ImageURL:
                                    
                        #             product_item.setdefault('', []).append(productsize)

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
                # product_item['image_urls'].extend(imageURLs)
                # print(imageURLs)
                # 
                        
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

  