from scrapy.spiders import Spider
from scrapy.selector import Selector 


import pdb 

class TutorialSpider(Spider) : 
	name = "selector"
	allowed_domains = ["huanqiu.com"]
	start_urls = [
		"http://world.huanqiu.com/article/",
	]

	def parse(self, response):
		pdb.set_trace()
		filename = response.url.split("/")[-2]
		with open(filename, 'wb') as f:
			f.write(response.body)