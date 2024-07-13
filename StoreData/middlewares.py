# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import time
from scrapy.exceptions import IgnoreRequest
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class StoredataSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class StoredataDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)

class Retry429Middleware:
    def __init__(self, crawler):
        self.retry_times = crawler.settings.getint('RETRY_TIMES', 10)
        self.retry_http_codes = set(int(x) for x in crawler.settings.getlist('RETRY_HTTP_CODES', []))
        self.retry_http_codes.add(429)
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls(crawler)
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        return middleware

    def spider_opened(self, spider):
        self.max_retry_times = self.retry_times

    def process_response(self, request, response, spider):
        if response.status in self.retry_http_codes:
            retries = request.meta.get('retry_times', 0) + 1

            if retries <= self.max_retry_times:
                wait_time = 40 + retries % 3  # Wait between 5 to 7 seconds
                spider.logger.info(f"Retrying {request.url} (failed {retries} times) in {wait_time} seconds due to status {response.status}")
                time.sleep(wait_time)

                retry_req = request.copy()
                retry_req.meta['retry_times'] = retries
                retry_req.dont_filter = True

                return retry_req
            else:
                spider.logger.info(f"Gave up retrying {request.url} (failed {retries} times) due to status {response.status}")
                raise IgnoreRequest(f"Retries exceeded for {request.url}")

        return response
