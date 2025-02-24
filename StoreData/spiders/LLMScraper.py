import scrapy
import json
import re
from scrapy_splash import SplashRequest 
from scrapegraphai.graphs import SmartScraperGraph
from scrapegraphai.utils import prettify_exec_info
from requests.exceptions import RequestException, HTTPError, ConnectionError, Timeout
import logging
import requests
# import scrapy
# from scrapy import Request



graph_config = {
   "llm": {
      "model": "ollama/llama3",
      "temperature": 1,
      "format": "json",  # Ollama needs the format to be specified explicitly
      "model_tokens": 3000, #  depending on the model set context length
       "base_url": "http://localhost:11434",  # set ollama URL of the local host (YOU CAN CHANGE IT, if you have a different endpoint
      
   },
   "embeddings": {
      "model": "ollama/nomic-embed-text",
      "temperature": 0,
      "base_url": "http://localhost:11434",  # set ollama URL
   }
}

# ************************************************
# Create the SmartScraperGraph instance and run it
# ************************************************

def fetch_page(url):
    customheaders = {
                'User-Agent': 'python-requests/2.31.0',
                'Accept-Encoding': 'gzip, deflate',
                'Accept': '*/*',
            }
    cookies = {
        'usn_visitor_id': '3d9b1702a4f601008b21bb66f50000003a280000',
        'OTGPPConsent': 'DBABLA~BVQqAAAACgA.QA',
        '_sharedid': 'f6c14874-c276-4fef-99e2-3dbdba4dbcd2',
        '_sharedid_cst': 'zix7LPQsHA%3D%3D',
        'usn_bot': 'ab986e8474d899cfd17743c422756311',
        'usn_session_id': '26752857852529728',
        'cogv': 'health',
        '_abck': '7FF34998C91CFE851B25E01E0C0CD333~-1~YAAQXZ42F7n23OCRAQAAP0fhDQypy2Il/R5Haq9RLLYjVoYLxJE3WB8ZhdP3LwPTBwAfAm740MZ2IN/stirb8J/BdIwS0NKD3aCIoZ9RUb2ht62r6TzWRshtXN4rgGH1wpVavyfC1gk4JH/9mYV9NkIBee/pOlPzSKmws3KUZeNE9II5GdwbMnWU5osoB8L8BgzCbdO41v5vkI3h82soJ24X1ZjQiP3//OKibrXXCvtoiAapWTEdLYXM7dTp3huwuwhL2JTHhtOTDMzNtSB1YmQQww4AYCWLdKOdZxhL+EJVA2jlsYKfcSWMAY4+bmqE8ZX/i50Vd3VuVi6rSAz31SrKopQkF+hVRQMrtxdmsfSNATUgJxk/mQnnunoUp4FblaLM4+K4Mr+0FA==~-1~-1~-1',
        'bm_mi': 'DDAE42EC37C8BE5F4114ACA15F0CF9B3~YAAQXZ42F3Av3eCRAQAAmlXnDRn86j58Lva7CYW4XfSORE1+1QWW1sI7kvGj0Qy5gOpVVzAiGq+zoP1xr9pW1Tlg7OcFWgwscEnZPEg1ribiSNZ8ux5zW7Yn0tCaQQ3UVWId2aVN0Syvcfpa6n5rynPPlDi4aS7XLsmqqKZ2xkAVwAKQ1ND6u9xLrnt23pd2sEljpYs0oa6PFqnYeaJujWMm7KhK/tUpW4t4qzZ+SL1F8JwestNB9SM+baCuCu1nbO9BPg1d2jsMxQozF2u+7uCYqJHRQF8WW93QOn0DpUn6EmptbMDFh60/LOwVpFHqzJiLZImBXow9EKo0AsY83EFM4JTs7mrLE9JY9aY=~1',
        'ak_bmsc': 'C049DDA613B0054695F78D1BA8167EF9~000000000000000000000000000000~YAAQU542F70iKe2RAQAA5lQPDhn077H6HhdKKix+pxM39UG3edEjIK4hEuOheDJInwtDWt7IXv9ui7O9FepFE2ATJF0cbuTBD6brO7kVrUvJnKv67BH/O8U4X4hJ0La9odxmkNLz42UozYxUMJV8e6XQ+90/oY7/iR0fo02aeQ6vnKeKSgZCE2CwT8xoiMbNYw0UwPm6StEUI+RqgNUQeB/TM+g+AWGBpRfOVFqcWwcBh6edrIW/ReBHishPxak3v+02QSPNQU40vy0i/IM5Rqpmdz/tMsEhXzvNe4HgODD2xxDClGIrGovldF9FB/VU31NrVm8popsylkOzToQYn4ImTrd3OKlQaa3J1CQSu/C/oB1EXXdjaADPjWRsx4IbmAmakKwaEtO0WuAG/plVCoEINUiz0H6REOxqlnZj5kpAVl1h2pV5IOISvoN5Lk4bcIBJhMgPHglce3Ialr+1X+s=',
        'SEARCH_SAMESITE':	'CgQIg5wB',	
'SID' :	'g.a000ngjnEnVvMP59S0ctW6TuPAqqK_Bex_BfEqR7MTZULYalqNj1em3xxCqEEaxvLQpewLxJ6gACgYKAQYSARESFQHGX2MiyT-I6-dRxvzblYMOwq1svBoVAUF8yKrXLOSHuCGAZHhMWUtItz2I0076',	
'SIDCC' :	'AKEyXzWFB86TX0Bg8vXSCu_4oPJ7w_I-HvvPMDHE1pbkZF8L9HjEJWedhqJ6QnKrfl3HM_uGeP8'	,
'SMSV' :	'ADHTe-C37StV7-3QVx78wI_E30I6f9hdkchN47J9MEPwWFMblFwSjRB4SlLOdjtvToH1QZTgAmmUzo4EP0S-CX97Y0ZsPF0XfmQWX7p9pcAqHKAC1rArY0k',	
'SSID' :	'AOcj_ApoeZxsc5A4O',			
'__Secure-1PAPISID':	'IejbwTEOdRkZt1hW/ASqtlUDidIGO56Tck',	
'__Secure-1PSID':	'g.a000ngjnEnVvMP59S0ctW6TuPAqqK_Bex_BfEqR7MTZULYalqNj1g9q32OlQrRgAofcNxSF1-gACgYKAcMSARESFQHGX2Mikf2MI2EbmA5DjwHrNLk2XBoVAUF8yKq97MjjFlHLTcRVDp2ZvHJX0076',	
'__Secure-1PSIDCC' :	'AKEyXzXVefKJPPeGGFiOqTDTqQacB-c6vK8YTkEm9VNPNPYIluXTcBVc8HbcSpqVVTA70akGvQ',
'__Secure-1PSIDTS' :	'sidts-CjEBQlrA-LapsRT0_1uDfTWmcqwB5p8iXrvypXvHSxH4dqcDcydbZxm6T4E0s4dFwd30EAA',		
'__Secure-3PAPISID' :	'IejbwTEOdRkZt1hW/ASqtlUDidIGO56Tck',
'usn_bot':	'c8379024141b5d6c256145540813d116',
'usn_bot':	'e0c911a05f9945af45cae7211bdeb439',		
'usn_bot' :	'ab986e8474d899cfd17743c422756311',	
'usn_session_id': 	'26752857852529728'	,
'usn_visitor_id' :	'3d9b1702a4f601008b21bb66f50000003a280000',		
'utag_main	v_id':'01914afb08f200028d2',
    }
    logging.info(f"Fetching page: {url}")
    try:
        response = requests.get(url, timeout=120, headers= customheaders, cookies=cookies)

        logging.info(f"Response Status Code: {response.status_code}")
        
        if response.status_code == 200:
            logging.debug("Page fetched successfully.")
            return response.text
        else:
            logging.error(f"Failed to fetch page. Status code: {response.status_code}")
            return None
    except requests.Timeout:
        logging.error("Request timed out while fetching the page.")
        return None
    except Exception as e:
        logging.error(f"Error fetching page: {e}")
        return None
    
logging.basicConfig(level=logging.INFO)

# Create the SmartScraperGraph instance and log the URL
# logging.info(f"Scraping URL: {graph_config['llm']['base_url']}")

# page_content = fetch_page(graph_config['llm']['base_url'])


logging.debug("Page content fetched successfully. Proceeding with scraping...")

    # Initialize SmartScraperGraph with the fetched page content

def arse_specialty_details(self, response):
    print(response.url)
    

    # try:
    #     # Define custom headers
    #     with requests.Session() as session:
    #         session.headers.update({
    #             'User-Agent': 'python-requests/2.31.0',
    #             'Accept-Encoding': 'gzip, deflate',
    #             'Accept': '*/*',
    #             'Connection': 'close',  # Explicitly closing connection
    #         })
    #         response = session.get(specialty_url, timeout=10000)
    #         print(f"Following is the response URL: {response.url}")
    #         return response
    
    # except RequestException as e:
    #     # Handle any request exceptions
    #     print(f"Request failed: {e}")
    #     return None
def process_specialty_url():
    # print(f"Processing specialty URL: {full_url}")
    # response = requests.get(full_url)
    # print(response.url)
    smart_scraper_graph = SmartScraperGraph(
    prompt= """
    Extract the names of all specialties and their respective 'href' attributes under the <ul> element with the attribute 'data-test-id="CommonSpecialties"' in the HTML.

    Instructions:
    1. Locate the <ul> element with the 'data-test-id="CommonSpecialties"' attribute.
    2. Inside this <ul> element, find all <li> elements and extract the <a> tag inside each <li>.
    3. From each <a> tag, extract:
    - The text content as the exact name of the specialty (do not infer the name from the 'href' attribute).
    - The exact 'href' attribute **without modifying it** in any way.
    4. Ensure that the 'href' value is extracted directly from the HTML and is not changed or reconstructed.
    5. Do not add or replace any part of the `href` or infer any values for the name from the `href`.
    6. Return the results as a list of dictionaries, where each dictionary contains:
    - 'name': the exact text content of the <a> tag (specialty name).
    - 'href': the original `href` value as it appears in the HTML.

    Example:
    If the specialty name is 'Cardiology', and the `href` is `/doctors/cardiologists`, return:
    {'name': 'Cardiology', 'href': '/doctors/cardiologists'}
    """,
    source="https://health.usnews.com/doctors",  # Pass the raw HTML here
    config=graph_config

        )
    result = smart_scraper_graph.run()
    print(result)
    if 'specialties' in result:
        specialties = result['specialties']
        
        # Iterate through each specialty
        for specialty in specialties:
            name = specialty['name']
            relative_url = specialty['href']
            
            # Construct the full URL by combining base URL and the relative path (href)
            full_url = f"{base_url}{relative_url}"
            
            # Print the full URL and specialty name for debugging
            yield SplashRequest(full_url, arse_specialty_details)
            # if specialty_page:
            #     arse_specialty_details(name, full_url, specialty_page)

    else:
        print("No specialties found in the result.")




process_specialty_url()

    # Run the scraper and track progress
# def run_scraper():
#     try:
#         logging.info("Executing scraper...")

#         # Track the graph execution step-by-step
#         result = smart_scraper_graph.run()

#         logging.info("Scraper execution completed.")
#         logging.debug(f"Raw result: {result}")

#             # Log each scraped item
#         if isinstance(result, dict) and "items" in result:
#             for idx, item in enumerate(result["items"]):
#                 logging.debug(f"Processing item {idx + 1}: {item}")
            
#         return result
#     except Exception as e:
#         logging.error(f"Error occurred during scraping: {e}", exc_info=True)
#         return None

#     # Run the scraper and get the results
# scraper_result = run_scraper()

#     # If you need to prettify the output
# if scraper_result:
#     prettified_result = prettify_exec_info(scraper_result)
#     print(prettified_result)

# else:
#     logging.error("Failed to retrieve page content. Aborting scraping.")