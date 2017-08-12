import scrapy

class ChapterSpider(scrapy.Spider):
    name = "chapter"
    allowed_domains = ["comic.kukudm.com"]
    start_urls = [
        "http://comic.kukudm.com/comiclist/2044/index.htm"
    ]

    def parse(self, response):

        for it in response.css('#comiclistn > dd'):
            print(it.xpath('a/@href').extract_first())
            print("\n")
            pass
        pass