# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Request
from scrapy.pipelines.images import ImagesPipeline
from urllib.parse import unquote


class ComicsSpiderPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        item = request.meta['item_name']
        url = request.url
        url_split = url.split('/')
        name = 'full/%s/%s' % (unquote(url_split[-2]), str(item))
        return name


    def get_media_requests(self, item, info):
        # yield Request(item['images']) # Adding meta. Dunno how to put it in one line :-)
        r = Request(item['image_url'], priority=100)
        r.meta['item_name'] = item["name"]
        return r
