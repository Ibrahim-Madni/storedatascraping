

import scrapy
import os
from urllib.parse import urlparse
from scrapy.pipelines.images import ImagesPipeline
import logging
import hashlib
class CustomImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        print("    \n"*4)
        print(item)
        # This method is called for each item with 'image_urls' field
        # print(f"my image url: {item['categoryImage']}")
        # subcategory_title = item['Subcategories'][0]['subcategoryTitle']
        # yield scrapy.Request(item['categoryImage'],  self.process_item, meta={'category_title': item['CategoryTitle'], 'subcategoryTitle': subcategory_title})
        # For the image_urls inside productItems
        if 'image_urls' in item:
            for image_url in item['image_urls']:
        # for product in item['ProductItem']:
            # image_url = product['image_urls']
                print(f"my image url: {image_url}")
                yield scrapy.Request(image_url , meta={'category_title': item['categoryName'], 'subcategoryTitle': item['SubcategoryName']})
                # meta={'category_title': item['categoryName'], 'subcategoryTitle': item['SubcategoryName']}
                # ,meta={'category_title': item['categoryName'], 'subcategoryTitle': item['SubcategoryName']}
                # yield scrapy.Request(image_url,meta={'ItemTitle': item['ItemTitle']} )
        else:
            print("no imageurl found")
        # Need this code later <> Original Code
        # if 'image_urls' in item:
        #     print(" I was here")
        #     for image_url in item['image_urls']:
        #         print(f"my image url:{image_url}")
        #         subcategory_title = item['Subcategories'][0]['subcategoryTitle']
        #         # print(subcategory_title)
        #         yield scrapy.Request(image_url, meta={'category_title': item['CategoryTitle'], 'subcategoryTitle': subcategory_title})
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
        category = request.meta.get('category_title', 'default_category')
        subcategory = request.meta.get('subcategoryTitle', 'default_subcategory')
        # itemname = request.meta.get('ItemTitle')
        # Construct the filename using category and subcategory
        image_name = os.path.basename(urlparse(request.url).path)
    # Construct the path using category, subcategory, and original filename
        path = os.path.join(category, subcategory,  image_name)
        print(f"Saving to path: {path}")
        return path
        # filename = f"{category}_{subcategory}.jpg"
        # print("done")
        # return filename