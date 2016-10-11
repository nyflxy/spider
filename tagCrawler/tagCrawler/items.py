# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

#主题相关链接抓取
class TagcrawlerItem(Item):
	tag = Field()

#博客链接
class BlogItem(Item):
	blog_href = Field()
	blog_name = Field()

