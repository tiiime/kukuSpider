import scrapy
from urllib.parse import urljoin
from scrapy.http import Request
import time
from scrapy.selector import HtmlXPathSelector


class CategorySpider(scrapy.Spider):
    name = "category"
    allowed_domains = ["comic.kukudm.com"]
    home = "http://comic.kukudm.com"
    start_urls = [
        "http://comic.kukudm.com/comiclist/2044/index.htm"
    ]

    def parse(self, response):
        for it in response.css('#comiclistn > dd'):
            print("\n----------- chapter -----------\n")
            print(self.home + it.xpath('a/@href').extract_first())
            yield Request(
                urljoin(response.url, self.home + it.xpath('a/@href').extract_first()),
                callback=self.chapter_parser)
            pass
        pass

    def chapter_parser(self, response):
        print("chapter_parser")
        path = response.xpath('/html/body/table[2]/tr/td/a[2]/@href').extract_first()

        if not path:
            path = response.xpath('/html/body/table[2]/tr/td/a[1]/@href').extract_first()

        print("path  --> " + path)

        href = self.home + path
        image = response.xpath('/html/body/table[2]/tr/td/img[1]/@src').extract_first()
        yield Request(urljoin(response.url, image), callback=self.download_image)

        print("image+" + image + "\n")
        if not path == "/exit/exit.htm":
            print("href ->" + href)
            yield Request(urljoin(response.url, href), callback=self.chapter_parser)
            pass
        pass

    def download_image(self, response):
        split = response.url.split("/")
        filename = split[-2] + "/" + split[-1]
        with open(filename, 'wb') as f:
            f.write(response.body)
