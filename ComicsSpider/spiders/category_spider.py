import re

import scrapy
from urllib.parse import urljoin
from scrapy.http import Request
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import unquote

from ComicsSpider.items import ComicsSpiderItem

class CategorySpider(scrapy.Spider):
    name = "category"
    num = re.compile(r"[+-]?\d+(?:\.\d+)?")
    allowed_domains = ["comic.kukudm.com"]
    home = "http://comic.kukudm.com"
    start_urls = [
        "http://comic.kukudm.com/comiclist/2044/index.htm"
    ]

    def __init__(self):
        chrome = r"/Users/kang/play/ComicsSpider/ComicsSpider/misc/chromedriver"
        self.driver = webdriver.Chrome(executable_path=chrome)

    def parse(self, response):
        for index, it in enumerate(response.css('#comiclistn > dd')):
            print("\n----------- chapter -----------\n")
            print(self.home + it.xpath('a/@href').extract_first())
            yield Request(
                urljoin(response.url, self.home + it.xpath('a/@href').extract_first()),
                callback=self.chapter_parser,
                priority=100 - index)

    def chapter_parser(self, response):
        index = response.url.split('/')[-1].split('.')[0]
        self.driver.get(response.url)

        print(unquote(response.url))

        try:
            title = self.driver.title
            print("title->" + title)
            titleIndex = 100 - int(self.num.search(title).group(0))
        except AttributeError:
            titleIndex = 0

        try:
            ele = self.driver.find_element_by_css_selector(
                'body > table:nth-child(2) > tbody > tr > td > a:nth-child(15)')
        except NoSuchElementException:
            ele = self.driver.find_element_by_css_selector(
                'body > table:nth-child(2) > tbody > tr > td > a:nth-child(15)')

        path = ele.get_attribute('href')
        # href = self.home + path
        href = path

        image = self.driver.find_element_by_css_selector(
            "body > table:nth-child(2) > tbody > tr > td > img").get_attribute('src')

        if path.find(r"/exit/exit.htm") == -1:
            yield Request(href, callback=self.chapter_parser, priority=titleIndex)
            pass
        pass

        c = ComicsSpiderItem()
        c['image_url'] = image
        c['name'] = index.zfill(2) + ".jpg"
        yield c
