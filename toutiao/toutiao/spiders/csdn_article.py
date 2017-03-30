#coding=utf-8
from scrapy.spiders import Spider
from scrapy.selector import Selector 
from scrapy import Request

from newbie.items import TagcrawlerItem
from newbie.items import BlogItem

import pdb 

class TutorialSpider(Spider) : 
    name = "tag_articles"
    allowed_domains = ["csdn.net"]
    start_urls = [
        "http://www.csdn.net/tag/",
    ]

    #抓取标签
    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath("//div[@class='main clearfix tag_list']")
        items = []
        for site in sites : 
            tag_info_list = site.xpath("//li/div/div/a")
            for tag_info in tag_info_list : 
                item = TagcrawlerItem()
                item["tag"] = {}
                item["tag"]["name"] = tag_info.xpath("text()").extract()[0]
                item["tag"]["href"] = tag_info.xpath("@href").extract()[0]
                print item["tag"]["name"] , item["tag"]["href"]

                new_url = item["tag"]["href"]

                #通过标签抓取相关博客链接
                # yield Request(url=new_url, callback=self.parse_post)

                items.append(item)
                with open("~/develop/spider/newbie/tag.json") as f:
                    f.write(items)
 
    #抓取博客相关数据
    # def parse_post(self, response):
    #     sel = Selector(response)
    #     sites = sel.xpath("//div[@class='tag_blog']/ul/li")

    #     blog_items = {}
    #     blog_items["tag_href"] = response.url
    #     blog_items["tag_name"] = response.url.split("tag/")[1]
    #     blog_items["theme_description"] = sel.xpath("//div[@class='tag_blog']/ul/p/a/text()").extract()
    #     blog_items["blog"] = []
 
    #     for site in sites : 
    #         blog_item = BlogItem()
    #         blog_item["blog_href"] = site.xpath("div/a/@href").extract()[0]
    #         blog_item["blog_name"] = site.xpath("div/a/text()").extract()[0]

    #         blog_items["blog"].append(blog_item)
    #         try : 
    #             saveBlog(blog_item)
    #         except Exception , e : 
    #             print e 
    #     return blog_items