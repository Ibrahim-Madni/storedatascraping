import scrapy
import json
from scrapy.crawler import CrawlerProcess
import scrapy.downloadermiddlewares
import scrapy.downloadermiddlewares.retry
import scrapy.spidermiddlewares
from scrapy_splash import SplashRequest 
from scrapy.pipelines.images import ImagesPipeline
import os 
import re
from scrapypuppeteer import PuppeteerRequest
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
    MetaData14 = scrapy.Field()
    MetaData14 = scrapy.Field()
    ItemURL= scrapy.Field()
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
    name = "farfetchindividualitemsspider"
    homeURL = "https://www.farfetch.com"
    subcat_item = SubcategoryItem()
    lua_script = """
    function main(splash)
        -- Go to the URL (replace with your actual URL)
        assert(splash:go(splash.args.url))

        -- Wait for the page to load (adjust wait time if needed)
        splash:wait(2)

        -- Select the button using the CSS selector
        local button = splash:select("div#slice-container > div.ltr-1p6ifn1.eg8xtxy3 > div > div.ltr-10pik5s.eg8xtxy2 > button")

        -- Ensure the button was found before attempting to click it
        if button then
            -- Click the button using mouse_click method
            assert(button:mouse_click())

            -- Optional: Wait for the page to reload after clicking (adjust wait time if needed)
            splash:wait(2)

            -- Return the rendered HTML
            return splash:html()
        else
            return {
                error = "Button not found"
            }
        end
    end
    """
        

    def start_requests(self):
        start_urls = ['https://www.farfetch.com/ae/shopping/men/adidas-los-angeles-football-club-2425-home-jersey-t-shirt-item-23491453.aspx?storeid=10806',
                      'https://www.farfetch.com/ae/shopping/men/y-3-logo-print-perforated-t-shirt-item-23047845.aspx?storeid=10267',
                      'https://www.farfetch.com/ae/shopping/men/adidas-argentina-24-home-jersey-t-shirt-item-23981104.aspx?storeid=10962',
                      'https://www.farfetch.com/ae/shopping/men/adidas-x-wales-bonner-organic-cotton-t-shirt-item-22053118.aspx?storeid=12263',
                      'https://www.farfetch.com/ae/shopping/men/adidas-x-wales-bonner-organic-cotton-t-shirt-item-22053118.aspx?storeid=12263',
                      'https://www.farfetch.com/ae/shopping/men/nike-x-matthew-williams-nrg-t-shirt-item-17805471.aspx?storeid=12850',
                      'https://www.farfetch.com/ae/shopping/men/adidas-x-nts-radio-teamgeist-recycled-polyester-t-shirt-item-24114403.aspx?storeid=14928',
                      'https://www.farfetch.com/ae/shopping/men/adidas-x-nts-radio-teamgeist-recycled-polyester-t-shirt-item-24114403.aspx?storeid=14928',
                      'https://www.farfetch.com/ae/shopping/men/adidas-logo-print-cotton-t-shirt-item-19937473.aspx?storeid=14288',
                      'https://www.farfetch.com/ae/shopping/men/marcelo-burlon-county-of-milan-x-kappa-logo-patch-polo-shirt-item-19455404.aspx?storeid=11935',
                      'https://www.farfetch.com/ae/shopping/men/marcelo-burlon-county-of-milan-optical-short-sleeve-t-shirt-item-20155862.aspx?storeid=12550',
                      'https://www.farfetch.com/ae/shopping/men/ea7-emporio-armani-logo-print-tracksuit-item-19765738.aspx?storeid=9053',
                      'https://www.farfetch.com/ae/shopping/men/nike-x-mmw-logo-print-shorts-set-item-23673940.aspx?storeid=12850',
                      'https://www.farfetch.com/ae/shopping/men/calvin-klein-logo-embroidered-shorts-item-22727018.aspx?storeid=13633',
                      'https://www.farfetch.com/ae/shopping/men/adidas-archive-track-shorts-item-24373243.aspx?storeid=10962',
                      'https://www.farfetch.com/ae/shopping/men/adidas-q3-atlanta-track-shorts-item-24388220.aspx?storeid=10962',
                      'https://www.farfetch.com/ae/shopping/men/polo-ralph-lauren-polo-pony-drawstring-running-shorts-item-23011474.aspx?storeid=11719',
                      'https://www.farfetch.com/ae/shopping/men/sporty-rich-olympic-gym-cotton-track-shorts-item-22965797.aspx?storeid=14287',
                      'https://www.farfetch.com/ae/shopping/men/awake-ny-embroidered-logo-cotton-track-shorts-item-23676851.aspx?storeid=11935',
                      'https://www.farfetch.com/ae/shopping/men/maison-kitsune-colour-block-track-shorts-item-23504862.aspx?storeid=10122',
                      'https://www.farfetch.com/ae/shopping/men/new-balance-logo-embroidered-track-shorts-item-23650111.aspx?storeid=10962',
                      'https://www.farfetch.com/ae/shopping/men/new-balance-archive-1997-crinkled-deck-shorts-item-23651010.aspx?storeid=10962',
                      'https://www.farfetch.com/ae/shopping/men/izzue-stripe-detail-cotton-shorts-item-23685726.aspx?storeid=12667',
                      'https://www.farfetch.com/ae/shopping/men/boss-reflective-logo-bermuda-shorts-item-23526506.aspx?storeid=11935',
                      'https://www.farfetch.com/ae/shopping/men/marcelo-burlon-county-of-milan-snakes-print-track-shorts-item-18785512.aspx?storeid=11871',
                      'https://www.farfetch.com/ae/shopping/men/lacoste-smart-paris-pique-polo-shirt-item-21417939.aspx?storeid=9334',
                      'https://www.farfetch.com/ae/shopping/men/polo-ralph-lauren-logo-embroidered-long-sleeve-shirt-item-14143979.aspx?storeid=13537',
                      'https://www.farfetch.com/ae/shopping/men/ballantyne-short-sleeve-knit-shirt-item-19934783.aspx?storeid=9026',
                      'https://www.farfetch.com/ae/shopping/men/cruciani-short-sleeve-fine-knit-shirt-item-23370504.aspx?storeid=9921',
                      'https://www.farfetch.com/ae/shopping/men/ami-paris-boxy-short-sleeve-shirt-item-23974248.aspx?storeid=9846',
                      'https://www.farfetch.com/ae/shopping/men/brunello-cucinelli-padded-cashmere-cardigan-item-23690076.aspx?storeid=12190',
                      'https://www.farfetch.com/ae/shopping/men/tom-ford-ribbed-knitted-jumper-item-23838650.aspx?storeid=13890',
                      'https://www.farfetch.com/ae/shopping/men/calvin-klein-cotton-blend-quarter-zip-jumper-item-19442819.aspx?storeid=10136',
                      'https://www.farfetch.com/ae/shopping/men/npeal-cable-knit-half-zip-jumper-item-20623621.aspx?storeid=9969',
                      'https://www.farfetch.com/ae/shopping/men/polo-ralph-lauren-embroidered-logo-polo-shirt-item-18076885.aspx?storeid=13367',
                      'https://www.farfetch.com/ae/shopping/men/polo-ralph-lauren-long-sleeved-polo-shirt-item-15626095.aspx?storeid=12491',
                      'https://www.farfetch.com/ae/shopping/men/polo-ralph-lauren-pony-embroidered-cotton-polo-shirt-item-22525032.aspx?storeid=14288',
                      'https://www.farfetch.com/ae/shopping/men/polo-ralph-lauren-embroidered-logo-pique-polo-shirt-item-22522913.aspx?storeid=14288',
                      'https://www.farfetch.com/ae/shopping/men/vilebrequin-chill-terry-cloth-shirt-item-22719646.aspx?storeid=15614',
                      'https://www.farfetch.com/ae/shopping/men/polo-ralph-lauren-long-sleeved-polo-shirt-item-15626095.aspx?storeid=12491',
                      'https://www.farfetch.com/ae/shopping/men/ami-paris-logo-embroidered-cotton-shirt-item-21820953.aspx?storeid=10116',
                      'https://www.farfetch.com/ae/shopping/men/pt-torino-straight-leg-tailored-trousers-item-18184339.aspx?storeid=9661',
                      'https://www.farfetch.com/ae/shopping/men/tom-ford-cotton-straight-leg-trousers-item-19587203.aspx?lang=en-US&size=22&storeid=9782&utm_source=google&utm_medium=cpc&utm_keywordid=33913866&utm_shoppingproductid=19587203-22&pid=google_search&af_channel=Search&c=807410387&af_c_id=807410387&af_siteid=&af_keywords=pla-297186054669&af_adset_id=40241117165&af_ad_id=191626448567&af_sub1=33913866&af_sub5=19587203-22&is_retargeting=true&shopping=yes&gad_source=1&gclid=CjwKCAjw74e1BhBnEiwAbqOAjC0WwW6JM9j2WXoh2c05O2kn3JCGmUZEc5MuyPvHDImeVosn6xKY7hoCm0EQAvD_BwE',
                      'https://www.farfetch.com/ae/shopping/men/boggi-milano-straight-leg-cotton-blend-trousers-item-21275304.aspx?storeid=15159',
                      'https://www.farfetch.com/ae/shopping/men/ferragamo-straight-leg-tailored-trousers-item-22586889.aspx?storeid=9782',
                      'https://www.farfetch.com/ae/shopping/men/etro-tailored-wool-trousers-item-23757791.aspx?storeid=9710&rtype=inspire_portal_pdp_generic_a&rpos=3&rid=427bfbf8-46b9-49ee-a298-db9abe967433',
                      'https://www.farfetch.com/ae/shopping/men/zegna-tapered-leg-cotton-blend-chino-trousers-item-22496527.aspx?storeid=11663&rtype=inspire_portal_pdp_generic_a&rpos=7&rid=00588165-ef10-40e2-ab9d-bf3068ef4740',
                      'https://www.farfetch.com/ae/shopping/men/zegna-pleated-tapered-trousers-item-22496620.aspx?storeid=11905&rtype=inspire_portal_pdp_generic_a&rpos=9&rid=ce3047c9-b954-400f-aa06-12de98912829',
                      'https://www.farfetch.com/ae/shopping/men/dolce-gabbana-pressed-crease-tailored-flannel-trousers-item-20047783.aspx?storeid=11935',
                      'https://www.farfetch.com/ae/shopping/men/golden-goose-gingham-check-trousers-item-17936521.aspx?storeid=9600',
                      'https://www.farfetch.com/ae/shopping/men/circolo-1901-pow-check-cropped-trousers-item-19182274.aspx?storeid=9683',
                      'https://www.farfetch.com/ae/shopping/men/rota-checked-tailored-trousers-item-20939426.aspx?storeid=11518',
                      'https://www.farfetch.com/ae/shopping/men/zegna-crossover-checked-wool-trousers-item-22496735.aspx?storeid=11905',
                      'https://www.farfetch.com/ae/shopping/men/lardini-prince-of-wales-check-wool-slim-cut-trousers-item-21369107.aspx?storeid=9111',
                      'https://www.farfetch.com/ae/shopping/men/paul-smith-tailored-cotton-trousers-item-22479414.aspx?storeid=10479',
                      'https://www.farfetch.com/ae/shopping/men/apc-dart-detailed-tapered-trousers-item-22972841.aspx?storeid=9683',
                      'https://www.farfetch.com/ae/shopping/men/mc2-saint-barth-crab-print-swim-shorts-item-23448739.aspx?storeid=9514',
                      'https://www.farfetch.com/ae/shopping/men/vilebrequin-logo-applique-swim-shorts-item-23028178.aspx?storeid=10280',
                      'https://www.farfetch.com/ae/shopping/men/vilebrequin-noumea-graphic-print-swim-shorts-item-24008463.aspx?storeid=15614',
                      'https://www.farfetch.com/ae/shopping/men/karl-lagerfeld-hotel-karl-striped-swim-shorts-item-20575380.aspx?storeid=11825',
                      'https://www.farfetch.com/ae/shopping/men/jw-anderson-graphic-print-striped-swim-shorts-item-21288653.aspx?storeid=12077',
                      'https://www.farfetch.com/ae/shopping/men/versace-greca-border-swim-shorts-item-15361831.aspx?storeid=13309',
                      'https://www.farfetch.com/ae/shopping/men/brunello-cucinelli-graphic-print-swim-shorts-item-23159199.aspx?storeid=12966',
                      'https://www.farfetch.com/ae/shopping/men/paul-smith-sea-life-print-drawstring-swim-shorts-item-19944024.aspx?storeid=10188',
                      'https://www.farfetch.com/ae/shopping/men/drole-de-monsieur-logo-print-swim-shorts-item-22698529.aspx?storeid=10122',
                      'https://www.farfetch.com/ae/shopping/men/lacoste-crocodile-print-drawstring-swim-shorts-item-22960345.aspx?storeid=15187',
                      'https://www.farfetch.com/ae/shopping/men/ami-paris-elasticated-waist-swim-shorts-item-21819655.aspx?storeid=14115',
                      'https://www.farfetch.com/ae/shopping/men/ea7-emporio-armani-logo-print-swim-shorts-item-13545024.aspx?storeid=11918',
                      'https://www.farfetch.com/ae/shopping/men/palm-angels-pa-city-logo-print-swim-shorts-item-21820659.aspx?storeid=9383',
                      'https://www.farfetch.com/ae/shopping/men/glanshirt-long-sleeve-linen-shirt-item-22717671.aspx?storeid=12276',
                      'https://www.farfetch.com/ae/shopping/men/zegna-long-sleeve-linen-shirt-item-20250493.aspx?storeid=11905',
                      'https://www.farfetch.com/ae/shopping/men/nn07-arne-linen-shirt-item-24058488.aspx?storeid=11004',
                      'https://www.farfetch.com/ae/shopping/men/givenchy-graphic-print-cotton-t-shirt-item-24588460.aspx?storeid=10704',
                      'https://www.farfetch.com/ae/shopping/men/120-lino-botanical-print-linen-shirt-item-23834769.aspx?storeid=14986',
                      'https://www.farfetch.com/ae/shopping/men/vilebrequin-x-vilebrequin-charlie-linen-shirt-item-22763508.aspx?storeid=13537',
                      'https://www.farfetch.com/ae/shopping/men/vilebrequin-embroidered-logo-polo-shirt-item-22719545.aspx?storeid=15614',
                      'https://www.farfetch.com/ae/shopping/men/vilebrequin-comores-linen-shirt-item-22718811.aspx?storeid=15614',
                      'https://www.farfetch.com/ae/shopping/men/boss-short-sleeve-linen-t-shirt-item-23072437.aspx?storeid=12917',
                      'https://www.farfetch.com/ae/shopping/men/nahmias-butterfly-beach-print-cotton-t-shirt-item-20031015.aspx?storeid=9460',
                      'https://www.farfetch.com/ae/shopping/men/polo-ralph-lauren-embroidered-logo-cotton-t-shirt-item-18991898.aspx?storeid=13539',
                      'https://www.farfetch.com/ae/shopping/men/lacoste-logo-patch-cotton-t-shirt-item-21518451.aspx?storeid=14288',
                      'https://www.farfetch.com/ae/shopping/men/lacoste-logo-embroidered-cotton-t-shirt-item-22734847.aspx?storeid=12629'
                      ]
        
        # Sold Out Items
            # https://www.farfetch.com/ae/shopping/men/rossignol-logo-print-lightweight-t-shirt-item-19579157.aspx?storeid=10216
            # https://www.farfetch.com/ae/shopping/men/on-running-pace-cleancloud-t-shirt-item-22766497.aspx?storeid=13537
            # https://www.farfetch.com/ae/shopping/men/adidas-argentina-24-home-jersey-t-shirt-item-23981104.aspx?storeid=10962

        for url in start_urls:
            # starturl = "https://www.farfetch.com/ae/shopping/men/adidas-los-angeles-football-club-2425-home-jersey-t-shirt-item-23491453.aspx?storeid=10806"
            item = StoreItem()
            yield SplashRequest(url, self.parse_individualitemdetails)

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

    def errback_httpbin(self, failure):
        self.log(f"Request failed: {failure.request}")
        self.log(f"Failure value: {failure.value}")
        if failure.check(scrapy.spidermiddlewares.httperror.HttpError):
            response = failure.value.response
            self.log(f"HTTP Error Response URL :{response.url}")
            self.log(f"HTTP Error Response status code :{response.status}")
            self.log(f"HTTP Error Response headers :{response.headers}")
        elif failure.check(scrapy.downloadermiddlewares.retry.RetryMiddleware):
            self.log(f"Retrying URL:{failure.request.url}")

    def parse(self, response):
        #collapsed-panel-category > div > ul > li:nth-child(1)
        
        # filename ="returnedsplashdata.html"
        # with open(filename, 'wb')  as f:
        #     f.write(response.body)
        #     self.log(f'Saved HTML content to {filename}')
        # print(response.body)
        url = response.url
        url_parts = url.split('/')

        # Extract the desired part by index (for example, the 5th part which is 'women')
        extracted_part = url_parts[5]
        # print(extracted_part)
        categoryname = ""
        if extracted_part == "women":
            categoryname = extracted_part
        elif extracted_part == "men":
            categoryname == extracted_part
        print(categoryname) 
        possiblewomensubcaturls = ['/ae/shopping/women/activewear-1/items.aspx', '/ae/shopping/women/coats-1/items.aspx', '/ae/shopping/women/denim-1/items.aspx', '/ae/shopping/women/dresses-1/items.aspx', '/ae/shopping/women/jackets-1/items.aspx', '/ae/shopping/women/skirts-1/items.aspx', '/ae/shopping/women/tops-1/items.aspx', '/ae/shopping/women/trousers-1/items.aspx']
        possiblemensubcaturls = ['/ae/shopping/women/activewear-1/items.aspx', '/ae/shopping/women/coats-1/items.aspx', '/ae/shopping/women/denim-1/items.aspx', '/ae/shopping/women/dresses-1/items.aspx', '/ae/shopping/women/jackets-1/items.aspx', '/ae/shopping/women/skirts-1/items.aspx', '/ae/shopping/women/tops-1/items.aspx', '/ae/shopping/women/trousers-1/items.aspx']
        # #catalog-actions > div.ltr-4ew8u6 > div > div > a:nth-child(1)
        a_tags = "nav#unstructured_navigation > a"
        for a in response.css(a_tags):

            href = a.css('::attr(href)').get()
            subcatname = a.css('::text').get()
            # print(f'Text: {text}, Href: {href}')
            if href in possiblewomensubcaturls:
                actualurl = f"{self.homeURL}{href}"
                yield SplashRequest(actualurl, self.parse_menitems, meta={'subcategoryname':subcatname }, args={'wait': 7})

                
        # "div[data-selector='catalog-quick-filters'] > a"
        # for filter in response.css(filterdata):
        #     print("filter found")
        #     itemlinks = filter.get("::attr(href)").get()
        #     print(itemlinks)
        # data = response.body.decode('utf-8')
        # with open(filename, 'w', encoding='utf-8') as f:
        #     f.write(data)
        #     self.log(f'Saved HTML content to {filename}')
        # hrefs = []
        # clothingnavigationitems = "div[data-testid='filterContainer'] > ul > li"
        # for li in response.css(clothingnavigationitems):
        #     navigationURL = li.css("a::attr(href)").get()
        #     navigationnames = li.css("a::text").get()
        #     print(navigationnames)
        #     print(navigationURL)


        # script_elements = response.xpath('//script').extract()
        # for script in script_elements:
        #     if 'window.__HYDRATION_STATE__="' in script:
        #         # filename = 'farfetch_url_document.html'
        #         # with open(filename, 'w', encoding='utf-8') as f:
        #         # print(script)
        #         script_content = script.strip('<script>').strip('</script>')
        #         # print(script_content)
        #         # products = json.loads(script_content)
        #         # filename = "farfetch"
        #         # with open(filename, 'w', encoding='utf-8') as f:
        #         #         f.write(script_content)
        #         #         self.log(f'Saved HTML content to {filename}')
        #         # print(products)
        #         # try:
        #         #     data = json.loads(script_content)
        #         #     url = data.get('uri', data.get('url'))  # Check for both 'uri' and 'url' keys
        #         #     if url:
        #         #         return url
        #         # except json.JSONDecodeError:
        #         #     pass
        #         pattern = r'"href\":\ ?"(.*?)"'  # Capture everything between quotes

        #         match = re.search(pattern, script_content)

        #         if match:
        #             print("i was here")
        #             extracted_href = match.group(1)
        #             print(extracted_href)
        #         else:
        #             print("im fucked")
                # url_pattern = r"\"uri\":\".*?\"|\"url\":\".*?\"(?=,)"  # Match 'uri' or 'url'
                # match = re.search(url_pattern, script_content)

                # if match:
                #     
                #     url = match.group(0)[7:-1]  # Extract URL group and remove quotes
                #     return url
                # else:
                #     print("im fucked")
    #             url_pattern = r"\"url\":\".*?\"(?=,)"  # Escape special characters

    #             # Search for the URL using the pattern
    #             match = re.search(url_pattern, script_content)
    #             if match:
    # # Extract the URL group
    #                 url = match.group(0)[7:-1]  # Remove leading/trailing characters
    #                 print(url)  # Print the extracted URL
    #             else:
    #                 print("URL not found in the script data.")
                # match = re.search(r'"url":"(.*?)"', script_content)
                # if match:
                #     href = match.group(1)
                #     print(href)

                # hrefs.extend(re.findall(r'"url\":\s*"(.*?)"', script))
                # print(hrefs)
        # Now hrefs list contains all the extracted href contents
        # for href in hrefs:
        #     self.log(f"Extracted href: {href}")
                # Print the script for debugging
                # print("Full script content:")
                # print(script)

        #         # Remove <script> tags
        #         script_content = script.strip('<script>').strip('</script>')

        #         # Debug: Print the initial part of the script content
        #         # print("Initial part of script content:")
        #         # print(script_content[:500])  # Print first 500 characters to inspect

        #         # Find the start and end of the JSON content
        #         json_start = script_content.find(':[{\\"scaleId\\":34061,\\"size\\":\\"XXS\\"},{\\"scaleId\\":34061,\\"size\\":\\"XS\\"}],') + len(':[{\\"scaleId\\":34061,\\"size\\":\\"XXS\\"},{\\"scaleId\\":34061,\\"size\\":\\"XS\\"}],')
        #         json_end = script_content.rfind(',\\"value\\":\\"991324\\",\\"description\\":\\"ÊtreCécile\\",\\"count\\":3,\\"deep\\":0}],''')
        #         context_radius = 70
        #         print(f"Context around json_start ({json_start}):")
        #         print(script_content[json_start-context_radius:json_start+context_radius])
        #         # print(f"Context around json_end ({json_end}):")
        #         # print(script_content[json_end-context_radius:json_end+context_radius])

        #         print(f"The starting point for the JSON is {json_start}")
        #         print(f"The ending point for the JSON is {json_end}")
        #         if json_start != -1 and json_end != -1:
        #             print("i AM FINALLY HERE")
        #             # Extract the JSON content ensuring json_end is included
        #             json_content = script_content[json_start:json_end + len(',\\"value\\":\\"991324\\",\\"description\\":\\"ÊtreCécile\\",\\"count\\":3,\\"deep\\":0}],')]
                    
        #             # Clean up the extracted JSON content
        #             json_content = json_content.replace('\\"', '"').replace('\\n', '').replace('\\t', '').replace('\\', '')
        #             json_content = json_content.strip('"')
        #             print(json_content)
                    # filename = 'farfetch_url_document.html'
                    # with open(filename, 'w', encoding='utf-8') as f:
                    #     f.write(json_content)
                    # self.log(f'Saved HTML content to {filename}')
                # Extract JSON content if valid indices are found
                # if json_start != -1 and json_end != -1:
                    # json_content = script_content[json_start:json_end]

                    # Debug: Print the extracted JSON content
                      # Print first 500 characters to inspect

                    # Replace escaped characters

                    # Remove leading and trailing quotes if any
                    
        #slice-header > div:nth-child(1) > nav > div:nth-child(1) > div.ltr-1w6gijd.etawori0 > a:nth-child(1)
        # parentSelector = "a[data-ffref='hd_gender']"
        # for a in response.css(parentSelector):
        #     GenderClothingURL=a.css("::attr(href)").get()
        #     # GenderClothingName=li.css("a::text").get()
        #     # print(GenderClothingName)
        #     print(GenderClothingURL)
            
            # if GenderClothingURL and GenderClothingURL != '#':
            #     yield  scrapy.Request(url= GenderClothingURL, callback= self.parse_menitems ,meta={'CategoryName': GenderClothingName})
    
    def parse_menitems(self, response):
        print(response.url)
        # filename ="returnedindividualsubcategoryinformation.html"
        # with open(filename, 'wb')  as f:
        #     f.write(response.body)
        #     self.log(f'Saved HTML content to {filename}')
        subcategory = response.meta['subcategoryname']
        script_elements = response.xpath('//script').extract()
        images = []
        processed_urls = []
        itemimage = ""
        nextpageURL= f"{response.url}{paginationbutton}"
        print(nextpageURL)
        paginationbutton = response.css("a[data-component='PaginationNextActionButton']::attr(href)").get()
        if paginationbutton != None:
            nextpageURL = f"{response.url}{paginationbutton}"
            print(nextpageURL)
            # yield SplashRequest(nextpageURL, self.parse_menitems, meta={'subcategoryname': subcategory}, args={'wait': 7})
        else:
            # If pagination button is not found, retry
            retry_count = response.meta.get('retry_count', 0)
            if retry_count < 3:  # Retry up to 3 times
                self.logger.info(f"Pagination button not found, retrying... (Attempt {retry_count + 1})")
                yield SplashRequest(response.url, self.parse_menitems, meta={'subcategoryname': subcategory, 'retry_count': retry_count + 1}, args={'wait': 7})
            else:
                self.logger.warning(f"Pagination button not found after {retry_count} retries, giving up.")
        # print(paginationbutton)
     
        
        # for idx, script in enumerate(script_elements):
        #     if 'type="application/ld+json"' in script and '"itemListElement"' in script:
        #         json_content = script.split('>', 1)[1].rsplit('</script>', 1)[0].strip()
        #         json_data = json.loads(json_content)
                
        #         # print(json_data)
        #         item_list_elements = json_data.get("itemListElement", [])
        #         for items in item_list_elements:
        #             itemname = items.get("name")
        #             # print(itemname)
        #             itemprice = items.get("offers",{}).get("price")
        #             itembrand = items.get("brand",{}).get("name")
        #             itempriceunit = items.get("offers",{}).get("priceCurrency")
        #             actualitemprice = f"{itemprice}{itempriceunit}"
        #             itemurl = items.get("offers",{}).get("url")
        #             actualitemurl = f"{self.homeURL}{itemurl}"
        #             if actualitemurl not in processed_urls:
        #                 processed_urls.append(actualitemurl)
        #                 for image in items.get("image", []):
        #                     itemimage = image
        #                     break
        #             # print(itemimage)
        #                 # itemimage = image
        #                 yield SplashRequest(url= actualitemurl, callback= self.parse_individualitemdetails, meta={'itemname': itemname, 'itemprice': actualitemprice , 'subcategory': subcategory, 'itembrand': itembrand, 'image': itemimage})
        
        # yield SplashRequest(url= nextpageURL, callback= self.parse_menitems, meta={'subcategory': subcategory, })
                    # if actualitemurl:
                        # 
                    # print(f"following are the item properties name: {itemname}, price: {itemprice}{itempriceunit}, itemurl : {itemurl}")

                # filename = "itemlist.json"
                # with open(filename, 'wb') as f:
                #     f.write(json.dumps(item_list_elements, ensure_ascii=False, indent=4).encode('utf-8'))  # Convert list to JSON string and encode to bytes
                #     self.log(f'Saved item list elements to {filename}')
                # print(item_list_elements)
            # else:
            #     print("nothing was found")
        #     # Create a filename for each script element
        #     filename = f"scriptcontent_{idx+1}.html"

        #     # Write the content to the file
        #     with open(filename, 'wb') as f:
        #         f.write(script.encode('utf-8'))  # Encode the string to bytes
        #         self.log(f'Saved HTML content to {filename}')
        # if '"itemListElement"' in script_elements:
        #     print(script_elements)
        # else:
        #     print("im fucked")
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
    
        # categoryname = response.meta['CategoryName']
        
        # subcategoryNavigation = response.css("div.x_RqXmD > div.EsGFLPm:nth-of-type(3) > div[data-testid='secondarynav-container'] > div.M8Zxf1o > div[data-testid='secondarynav-flyout']  > div.ZAntzlZ.MV4Uu8x > ul.c2oEXGw > li")
        # #goes through all the list items and extracts subcategories within the clothing item sublist
        # for li in subcategoryNavigation:
        #     allsubcategorylink = li.css("a::attr(href)").get()
        #     lowercasecategoryname = categoryname.lower()
        #     #Comparison parameter
        #     #this peice of code on Line 187 is used to compare the category name with the endpoint of the extracted subcategory link so we dont have unnecessary subcategoryitems that were within the list that are not relevant to the category
        #     if lowercasecategoryname == allsubcategorylink.split('/')[3].lower():
        #         subcategoryname = li.css("a::text").get()
        #         subcategorylink = li.css("a::attr(href)").get()
        #         print(subcategoryname)
        #         print(subcategorylink)
        #         if subcategorylink and subcategorylink != '#':
        #             yield SplashRequest(url= subcategorylink, callback= self.parse_individualitemdetails, meta={'categoryname': categoryname , 'subcategoryname': subcategoryname})

    def parse_individualitemdetails(self, response):
        product_item = ProductItem()
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
        itemurl = response.url
        product_item['ItemURL']= response.url
        itemimage = response.css("meta[property='og:image']::attr(content)").get()
        product_item['image_urls']= itemimage
        itemprice = response.css("meta[property='product:custom_label_4']::attr(content)").get()
        if itemprice:
            product_item['ItemPrice']= itemprice  
        else:
            product_item['ItemPrice']= "NA"
        itemname = response.css("meta[property='og:title']::attr(content)").get()
        product_item['ItemTitle']= itemname
        #itemname = response.css("meta[property='og:title']::attr(content)").get()
        metadatalist = response.css("ul._fdc1e5 > li")
        ParentURL = ""
        ParentURL = response.css("li[data-component='BreadcrumbWrapper'] > a::attr(href)")[3].get() 
        if not ParentURL:
            ParentURL = response.css("li[data-component='BreadcrumbWrapper'] > a::attr(href)")[2].get()
            
        parts = ParentURL.split('/')
        category = parts[3]
        subcategory = parts[5]
        product_item['CategoryTitle'] = category
        product_item['subcategoryTitle'] = subcategory
        # print(ParentURL)
        index = 0
        for index,metadata in enumerate(metadatalist):
            metatext = metadata.css("::text").get()
            if index == 0:
                product_item['ItemColour'] = metatext
            metadatakey = f"MetaData{index+1}"
            product_item[f"{metadatakey}"] = metatext
        print(product_item)
        yield product_item
        # script_content = response.xpath('//script[contains(., "window.__HYDRATION_STATE__")]/text()').get()

        # # Use regex to find the JSON content starting with {"apolloInitialState
        # if script_content:
        #     product_json = re.search(r'window\.__HYDRATION_STATE__\s*=\s*(\{.*\});?', script_content).group(1)

        # Parse the JSON data
        #     product_data = json.loads(product_json)
        #     # print(product_data)
        # else:
        #     print("nothing found")
        # product_json = re.search(r'window\.__HYDRATION_STATE__ = ({.*?});', script_content).group(1)
        # product_data = json.loads(product_json)
        # {'itemname': itemname, 'itemprice': actualitemprice , 'subcategory': subcategory}
        # Itemname = response.meta['itemname']
        # Itemprice = response.meta['itemprice']
        # subcategoryname = response.meta['subcategory']
        # itembrand = response.meta['itembrand']
        # itemimage = response.meta['image']
        # print(f"following are the item details Itemname: {Itemname}, /n Itemprice : {Itemprice}, /n subcategorydetail : {subcategoryname}, /n itembrand: {itembrand}, /n itemimage : {itemimage}")
        # itemhighlights = "ul._fdc1e5 > li"
        # itemcomposition = "div.ltr-92qs1a > p"
        # for listitem in response.css(itemhighlights):
        #     itemdetail = listitem.css("::text").get()
        #     # print(itemdetail)
        # for metadataitem in response.css(itemcomposition):
        #     metadata = metadataitem.css("::text").get()
            # print(metadata)
        # self.logger.info(f"Retrieved meta data: subcategoryname={subcategoryname}, categoryname={category}")
        # ItemSections= "section.listingPage_HfNlp > article"
        # LoadMoreButton = response.css("a[data-auto-id='loadMoreProducts']::attr(href)").get()
        # #product-205597587 > a > div.productMediaContainer_kmkXR.mediaContainer_rdzv9 > div > img
        # #product-203390299 > a > div.productMediaContainer_kmkXR.mediaContainer_rdzv9 > div > img
        # for article in response.css(ItemSections):
        #     # itemnames = article.css("a > p.productDescription_sryaw::text").get()
        #     #product-203390299 > a > div.productMediaContainer_kmkXR.mediaContainer_rdzv9 > div > img
        #     itemURL = article.css("a::attr(href)").get()
        #     itemname = article.css("a > p.productDescription_sryaw::text").get()
        #     #product-206835688 > a > div.productMediaContainer_kmkXR.mediaContainer_rdzv9 > div
        #     #product-206492427 > a > div.productMediaContainer_kmkXR.mediaContainer_rdzv9 > div > img
        #     #product-205491471 > a > div.productMediaContainer_kmkXR.mediaContainer_rdzv9 > div > img
        #     # itemimage = article.css("a > div.productMediaContainer_kmkXR.mediaContainer_rdzv9 > div > img::attr(src)").get()
        #     # print(itemimage)
        #     # for img in itemimage:
        #     #     images = img.css("::attr(src)").get()
        #     #     print(images)
        #     # itemprice = article.css("a > p.container_s8SSI > span.originalPrice_jEWt1 > span.price__B9LP::text").get()
        #     # print(itemimage)
        #     # print(itemname)
            
            
        #     # print(itemURL)
        #     if itemURL:
        #         yield scrapy.Request(url= itemURL, callback= self.parse_itempage, meta={'itemname': itemname, 'subcategoryname': subcategoryname, 'categoryname': category})    

        #     # print(itemnames)
            
       
        
        # if LoadMoreButton:
        #     # print("LoadMoreButton found")
        #     yield scrapy.Request(url= LoadMoreButton, callback= self.parse_individualitemdetails, meta={'itemname': itemname, 'subcategoryname': subcategoryname, 'categoryname': category})
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
        # print(categoryname)
        # print(SubcategoryName)   
        Itemname = response.meta['itemname']
        # ItemPrice = response.meta['itemprice']
        product_price_json = None
        pricecontent  = response.xpath('//script[contains(., "window.asos.pdp.config.stockPriceResponse")]/text()').get()
        product_price_json_match = re.search(r'window\.asos\.pdp\.config\.stockPriceResponse = ({.*?});', pricecontent)
        if product_price_json_match:
            product_price_json = product_price_json_match.group(1)
            product_price_data = json.loads(product_price_json)
            product_price = product_price_data.get('productPrice', {}).get('current', {}).get('text')
            product_item['ItemPrice'] = re.sub(r'\s+', '', product_price)
        else:
            # Handle the case where the pattern is not found in pricecontent
            print("Pattern not found in pricecontent")
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
        
        productbrandName = product_data.get('brandName')
        product_item['ItemBrand'] = productbrandName
        producttype = product_data.get('productType', {}).get('name')
        product_item['ItemType'] = producttype
        # productvariants = product_data.get('variants', [])
        productimages= product_data.get('images', [])
        # product_item['Size'] = []
        
        # product_name = product_data.get('name')
            
        # for index, variant in enumerate(productvariants):
        #         # product_item['Size'].append(productsize)
        #     productsize = variant.get('size')
        #     size_key = f'Size{index + 1}'
        #         # Use the created item class
                
        #         # Set the metadata value in the item
        #     product_item[size_key] = re.sub(r'\s+', '', productsize)
        #     colour = variant.get('colour')
        #     product_item['ItemColour'] = re.sub(r'\s+', '', colour)
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
