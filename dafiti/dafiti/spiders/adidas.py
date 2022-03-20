from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from dafiti.items import DafitiItem, DafitiStockItem
from scrapy.loader import ItemLoader
from scrapy import Request
import datetime


class DafitiAdidasSpider(CrawlSpider):
    name = "dafiti-adidas"
    allowed_domains = ["www.dafiti.com.br"]
    start_urls = ["https://www.dafiti.com.br/calcados-masculinos/tenis/adidas/"]
    version = "0-1-2"
    product_details = LinkExtractor(
        restrict_xpaths=(
            "//div[normalize-space(@class) = 'product-box-image']/a",
            "//div[normalize-space(@class) = 'last product-box-image']/a",
        )
    )
    pagination = LinkExtractor(
        restrict_xpaths=(
            "//li[normalize-space(@class) = 'page']",
            "//li[normalize-space(@class) = 'page next']",
        )
    )

    rules = [
        Rule(product_details, callback="parse_products"),
        Rule(pagination, follow=True),
    ]

    def parse_products(self, response):
        if response.url in self.start_urls:
            return None
        else:
            product_container = response.xpath(
                "//div[normalize-space(@class) = 'container product-page']"
            )
            i = ItemLoader(item=DafitiItem(), selector=product_container)
            i.add_xpath("product", "//h1[normalize-space(@class) = 'product-name']")
            i.add_xpath(
                "seller_name", "//p[normalize-space(@class) = 'product-seller-name']/a"
            )
            i.add_xpath(
                "seller_url",
                "//p[normalize-space(@class) = 'product-seller-name']/a/@href",
            )
            i.add_xpath(
                "price",
                "//span[normalize-space(@class) = 'catalog-detail-price-value']/@content",
            )
            i.add_xpath("sku", "//td[normalize-space(@itemprop) = 'sku']")
            i.add_xpath("description", "//p[@class='product-information-description']")
            i.add_value("spider_version", self.version)
            yield i.load_item()
            sku = response.xpath(
                "//td[normalize-space(@itemprop) = 'sku']/text()"
            ).get()
            if sku:
                stock_request_url = (
                    f"https://www.dafiti.com.br/catalog/detailJson?sku={sku}"
                )
                headers = {
                    "authority": "www.dafiti.com.br",
                    "pragma": "no-cache",
                    "cache-control": "no-cache",
                    "accept": "*/*",
                    "x-requested-with": "XMLHttpRequest",
                    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
                    "sec-ch-ua": '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
                    "sec-fetch-site": "same-origin",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-dest": "empty",
                    "referer": response.url,
                    "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                }
                yield Request(
                    url=stock_request_url,
                    headers=headers,
                    method="GET",
                    dont_filter=True,
                    callback=self.parse_stock_info,
                    cb_kwargs={"sku": sku},
                )

    def parse_stock_info(self, response, sku):
        raw_stock_data = response.json()
        raw_stock_data["base_sku"] = sku
        raw_stock_data["spider"] = self.name
        raw_stock_data["spider_version"] = self.version
        raw_stock_data["timestamp"] = datetime.datetime.now().isoformat()
        stock_data = DafitiStockItem(**raw_stock_data)
        itemproc = self.crawler.engine.scraper.itemproc
        itemproc.process_item(stock_data, self)
