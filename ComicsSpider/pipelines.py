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
        # item=request.meta['item'] # Like this you can use all from item, not just url.
        split = request.url.split('/')
        return 'full/%s/%s' % (unquote(split[-2]), split[-1])

    def get_media_requests(self, item, info):
        # yield Request(item['images']) # Adding meta. Dunno how to put it in one line :-)
        for image in item['image_urls']:
            yield Request(image)
