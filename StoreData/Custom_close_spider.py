from scrapy.exceptions import NotConfigured
from scrapy.extensions.closespider import CloseSpider

class CustomCloseSpider(CloseSpider):

    def __init__(self, crawler):
        super().__init__(crawler)
        self.downloader = crawler.engine.downloader

    def spider_idle(self, spider):
        # Check if there are outstanding requests in the downloader's queue
        if len(self.downloader.active) > 0:
            spider.log("Delaying spider closure. Waiting for image downloads to complete.")
            return

        # If no outstanding requests, close the spider
        super().spider_idle(spider)