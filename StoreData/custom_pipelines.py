

import scrapy
import os
from urllib.parse import urlparse
from scrapy.pipelines.images import ImagesPipeline
import logging
import hashlib
class CustomImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # print(item)
        for image_url in item['image_urls']:

            yield scrapy.Request(image_url )
        # meta={'category_title': item['CategoryTitle'], 'subcategoryTitle': item['subcategoryTitle'], 'productcolourID': item.get('ItemColour')}
    def process_item(self, item, spider):
        print(" I was here")
        logging.info(f"Item reached CustomImagesPipeline: {item}")
        return super().process_item(item, spider)
    # def request_image(self, url, item):
    #     # Log the URL being requested
    #     logging.debug(f"Requesting image: {url}")
    #     return scrapy.Request(url)
    def item_completed(self, results, item, info):
        # This method is called once the ImagesPipeline has processed the item
        print(" I may have gotten here")
        for ok, result in results:
            print("Processing item in CustomImagesPipeline")
            if not ok:
                # Log any errors encountered during image download
                logging.error(f"Error downloading image from {item['image_urls']}: {result}")
        return super().item_completed(results, item, info)
    def file_path(self, request, response=None, info=None, *, item=None):
        print("Processing item in CustomImagesPipeline")
        # category = request.meta.get('category_title', 'default_category')
        # subcategory = request.meta.get('subcategoryTitle', 'default_subcategory')
        # itemname = request.meta.get('ItemTitle')
        # productcolourID = request.meta.get('productcolourID', 'default_id')

    # Construct a more specific path using product or color information
    
        image_name = os.path.basename(urlparse(request.url).path)
    # Construct the path using category, subcategory, and original filename
        path = os.path.join('Dior',  image_name)
        print(f"Saving to path: {path}")
        return path
        # filename = f"{category}_{subcategory}.jpg"
        # print("done")
        # return filename