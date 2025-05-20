import scrapy


class WindnetpcSpider(scrapy.Spider):
    name = "windnetpc"
    allowed_domains = ["windnetpc.com"]
    start_urls = [
        "https://windnetpc.com/c/compnents/graphics-card/",     #GPU
        "https://windnetpc.com/c/compnents/processor/",         #CPU
        "https://windnetpc.com/c/compnents/motherboard/",       #mobo
        "https://windnetpc.com/c/compnents/graphics-ram/",      #ram
        "https://windnetpc.com/c/monitor/",                     #monitor

        ]

    def parse(self, response):
        for product in response.css("li.product"):
            price = product.css("span.woocommerce-Price-amount.amount bdi::text").get()

            if not price:
                continue

            yield {
                "category": response.css("h1.page-title::text").get(),
                "product": product.css("h2.woocommerce-loop-product__title::text").get(),
                "price": price,
            }

        next_page = response.css("a.next.page-numbers::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)