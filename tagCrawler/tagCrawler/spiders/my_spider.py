from scrapy.spiders import BaseSpider
from scrapy import Request 
import pdb
class MySpider(BaseSpider):
    name = 'myspider'
    start_urls = [
        "http://www.csdn.net/tag/",
        ]
 
    def parse(self, response):
        pdb.set_trace()
        # collect `item_urls`
        for item_url in self.start_urls:
            yield Request(url=item_url, callback=self.parse_item)
 
    def parse_item(self, response):
        pdb.set_trace()
        # item = MyItem()
        # # populate `item` fields
        # yield Request(url=item_details_url, meta={'item': item},
        #     callback=self.parse_details)
 
    def parse_details(self, response):
        item = response.meta['item']
        # populate more `item` fields
        return item
