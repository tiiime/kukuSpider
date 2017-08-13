import scrapy
from urllib.parse import urljoin
from scrapy.http import Request
import time
from scrapy.selector import HtmlXPathSelector
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from ComicsSpider.items import ComicsSpiderItem


class CategorySpider(scrapy.Spider):
    name = "category"
    allowed_domains = ["comic.kukudm.com"]
    home = "http://comic.kukudm.com"
    start_urls = [
        "http://comic.kukudm.com/comiclist/2044/index.htm"
    ]

    def __init__(self):
        chrome = r"C:\Users\SEELE\PycharmProjects\ComicsSpider\ComicsSpider\misc\chromedriver.exe"
        self.driver = webdriver.Chrome(executable_path=chrome)

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
        self.driver.get(response.url)

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

        print("path -->" + path)
        print("image -->" + image)

        if path.find(r"/exit/exit.htm") == -1:
            print("href ->" + href)
            yield Request(href, callback=self.chapter_parser)
            pass
        pass

        c = ComicsSpiderItem()
        c['image_urls'] = [image]
        yield c

    def download_image(self, response):
        print("download " + response.url)
        split = response.url.split("/")
        filename = split[-2] + "/" + split[-1]
        with open(filename, 'wb') as f:
            print("file->" + f)
            f.write(response.body)
