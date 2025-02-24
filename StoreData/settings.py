# # Scrapy settings for StoreData project
# #
# # For simplicity, this file contains only settings considered important or
# # commonly used. You can find more settings consulting the documentation:
# #
# #     https://docs.scrapy.org/en/latest/topics/settings.html
# #     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# #     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

# BOT_NAME = "StoreData"

SPIDER_MODULES = ["StoreData.spiders"]
# NEWSPIDER_MODULE = "StoreData.spiders"


# # Crawl responsibly by identifying yourself (and your website) on the user-agent
# #USER_AGENT = "StoreData (+http://www.yourdomain.com)"

# # Obey robots.txt rules
ROBOTSTXT_OBEY = True

# # Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 64

# # Configure a delay for requests for the same website (default: 0)
# # See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# # See also autothrottle settings and docs
# #DOWNLOAD_DELAY = 3
# # The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 64
# #CONCURRENT_REQUESTS_PER_IP = 16

# # Disable cookies (enabled by default)
COOKIES_ENABLED = False

# # Disable Telnet Console (enabled by default)
# #TELNETCONSOLE_ENABLED = False
# # Splash Server Endpoint
SPLASH_URL = 'http://localhost:8050'
# # Override the default request headers:
# #DEFAULT_REQUEST_HEADERS = {
# #    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
# #    "Accept-Language": "en",
# #}

# # Enable or disable spider middlewares
# # See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
   "StoreData.middlewares.StoredataSpiderMiddleware": 543,
}

# # Enable or disable downloader middlewares
# # See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    "StoreData.middlewares.StoredataDownloaderMiddleware": 543,
#    'scrapy_splash.SplashCookiesMiddleware': 723,
#    'scrapy_splash.SplashMiddleware': 725,
#    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
# }
# # IMAGE_PIPELINES = {
# #     'StoreData.pipelines.imagesPipeline': 1
# # }
# # ITEM_PIPELINES = {'StoreData.custom_pipelines.CustomImagesPipeline': 1}

ITEM_PIPELINES = {'StoreData.custom_pipelines.CustomImagesPipeline': 1}
# C:\Users\Felicia\Desktop\storedatascrape\storedatascraping\StoreData\images
IMAGES_STORE = 'C:/Users/Felicia/Desktop/storedatascrape/storedatascraping/StoreData/images'
DOWNLOAD_FAIL_ON_DATALOSS = False

# /home/s/Desktop/store-data-scraping-main/Images
# C:\Users\User\Desktop\Store Data Scraping\store-data-scraping-main\Images
# # Enable or disable extensions
# # See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    # "scrapy.extensions.telnet.TelnetConsole": None,
#    'scrapy.extensions.closespider.CloseSpider': None,  # Disable the built-in CloseSpider
#    'StoreData.Custom_close_spider.CustomCloseSpider': 1

# }

# # Configure item pipelines
# # See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# #ITEM_PIPELINES = {1144
# #    "StoreData.pipelines.StoredataPipeline": 300,
# #}

# # Enable and configure the AutoThrottle extension (disabled by default)
# # See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# #AUTOTHROTTLE_ENABLED = True
# # The initial download delay
# #AUTOTHROTTLE_START_DELAY = 5
# # The maximum download delay to be set in case of high latencies
# #AUTOTHROTTLE_MAX_DELAY = 60
# # The average number of requests Scrapy should be sending in parallel to
# # each remote server
# #AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# # Enable showing throttling stats for every response received:
# #AUTOTHROTTLE_DEBUG = False

# # Enable and configure HTTP caching (disabled by default)
# # See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# #HTTPCACHE_ENABLED = True
# #HTTPCACHE_EXPIRATION_SECS = 0
# #HTTPCACHE_DIR = "httpcache"
# #HTTPCACHE_IGNORE_HTTP_CODES = []
# #HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"
# DOWNLOAD_DELAY = 30
# DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'

# # Set settings whose default value is deprecated to a future-proof value
# REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
# TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
# FEED_EXPORT_ENCODING = "utf-8"

 # Scrapy settings for StoreData project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
BOT_NAME = "StoreData"
SPIDER_MODULES = ["StoreData.spiders"]
NEWSPIDER_MODULE = "StoreData.spiders"
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "StoreData (+http://www.yourdomain.com)"
# Obey robots.txt rules
ROBOTSTXT_OBEY = False
# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32
# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 32
CONCURRENT_REQUESTS_PER_IP = 16
# Disable cookies (enabled by default)
#COOKIES_ENABLED = False
# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False
# Splash Server Endpoint
PUPPETEER_SERVICE_URL = 'http://localhost:3000'
SPLASH_URL = 'http://localhost:8050'
# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}
DOWNLOAD_TIMEOUT = 30
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 403]
# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
   "StoreData.middlewares.StoredataSpiderMiddleware": 543,
}
# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   "StoreData.middlewares.StoredataDownloaderMiddleware": 543,
   'scrapypuppeteer.middleware.PuppeteerServiceDownloaderMiddleware': 1042,
   'scrapy_splash.SplashCookiesMiddleware': 723,
   'scrapy_splash.SplashMiddleware': 725,
   'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
   'StoreData.middlewares.Retry429Middleware': 543,
   'scrapy.downloadermiddlerwares.offsite.OffsiteMiddleware': None,
   # 'StoreData.ProxyRotationMiddleware.ProxyRotationMiddleware': 100,
   # 'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 1,
   # StoreData\ProxyRotationMiddleware.py
}
SELENIUM_DRIVER_NAME = 'chrome'
# SELENIUM_DRIVER_EXECUTABLE_PATH = 'C:/chromedriver_win32'
SELENIUM_DRIVER_ARGUMENTS=['--headless']
RETRY_TIMES = 10  # Number of times to retry a request
RETRY_HTTP_CODES = [429]  # HTTP codes to retry

# HTTP_PROXY = '92.119.177.20:443'
# 45.150.5.3
# If you need to use SOCKS proxy, you can configure it as well
# SOCKS proxy provided by Psiphon
# SOCKS_PROXY = 'socks5://localhost:51533/'
# custom_settings = {
#     'HTTP_PROXY': 'http://127.0.0.1:8118',
# }
# IMAGE_PIPELINES = {
#     'StoreData.pipelines.imagesPipeline': 1
# }
# ITEM_PIPELINES = {'StoreData.custom_pipelines.CustomImagesPipeline': 1}
# IMAGES_STORE = 'C:/Users/Hassan Ajmal/Desktop/Veeve data scraping/store-data-scraping/Images'
# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
   # "scrapy.extensions.telnet.TelnetConsole": None,
   'scrapy.extensions.closespider.CloseSpider': None,  # Disable the built-in CloseSpider
   'StoreData.Custom_close_spider.CustomCloseSpider': 1
}
#        forward-socks5    /        127.0.0.1:9050 .
# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {1144
#    "StoreData.pipelines.StoredataPipeline": 300,
#}
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False
# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"
DOWNLOAD_DELAY = 1
# DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
DUPEFILTER_CLASS = 'scrapy.dupefilters.BaseDupeFilter'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"