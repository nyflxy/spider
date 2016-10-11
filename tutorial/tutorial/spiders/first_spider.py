from scrapy.spiders import Spider
from scrapy.selector import Selector 

from tutorial.items import TutorialItem

import pdb 

class TutorialSpider(Spider) : 
	name = "tutorial"
	allowed_domains = ["huanqiu.com"]
	start_urls = [
		"http://world.huanqiu.com/article/",
	]

	def parse(self, response):
		sel = Selector(response)
		sites = sel.xpath("//a")
		items = []
		for site in sites : 
		 	item = TutorialItem()
		 	item["href"] = site.xpath("//a/@href").extract()
		 	items.append(item)
		return items 
