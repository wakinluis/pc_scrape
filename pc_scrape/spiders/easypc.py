import random
import scrapy
from scrapy_playwright.page import PageMethod


class EasypcSpider(scrapy.Spider):
    name = "easypc"

    def start_requests(self):
        yield scrapy.Request(
            url='https://easypc.com.ph/collections/graphic-card',
            callback=self.parse,
            meta={
                "playwright": True,
                "playwright_page_methods": [
                    PageMethod('wait_for_timeout', random.randint(1000, 3000)),
                    PageMethod('wait_for_selector', 'li.snize-product'),
                ],
            },
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.close()

        for product in response.css('li.snize-product'):
            yield {
                'product': product.css("span.snize-title::text").get(),
                'category': response.css("div.wrap-cata-title h2::text").get(),
                'price': product.css("span.snize-price::text").get()
            }

        next_page = response.css("a.snize-pagination-next::attr(href)").get()
        if next_page is not None:
            next_page_url = 'https://easypc.com.ph/collections/graphic-card' + next_page
            yield scrapy.Request(next_page_url, meta={
                "playwright": True,
                 "playwright_page_methods": [
                    PageMethod('wait_for_timeout', random.randint(1000, 3000)),
                    PageMethod('wait_for_selector', 'li.snize-product'),
                    ],
                },
            )