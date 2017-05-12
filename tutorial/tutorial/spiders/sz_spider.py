import scrapy


class SzSpider(scrapy.Spider):
    name = "sz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "http://site.6park.com/gz2/index.php?app=forum&act=gold"
    ]

    def parse(self, response):
        for sel in response.xpath('//td/center'):
            link = sel.xpath('a/@href').extract()
            desc = sel.xpath('text()').extract()
            print(link + "===" + desc)