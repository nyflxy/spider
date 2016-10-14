#coding=utf-8
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
from newbie.items import SharesItem
import newbie.mongo as mongo

import sys,pdb

subject_coll = mongo.get_coll("subject")

class MyShareSpider(Spider):
    name = "shares"
    allowed_domains = ["toutiao.io"]
    subjects = subject_coll.find()
    start_urls  = []
    for subject in subjects:
        start_urls.append("http://toutiao.io/subjects/"+str(subject['account']))

    def parse(self, response):
        sel = Selector(response)
        pagination = sel.xpath("//div[@class='text-center']/ul/li[@class='last']/a")
        try:
            page = int(pagination.xpath("@href").extract()[0].split("=")[1])
        except:
            page = 1

        share_url = response._get_url()
        new_share_urls = []
        for i in range(page):
            new_share_urls.append(share_url + "?page=" + str(i+1))
        print new_share_urls

        for new_url in new_share_urls:
            yield Request(url=new_url, callback=self.parse_post)

    def parse_post(self,response):
        sel = Selector(response)
        posts = sel.xpath("//div[@class='posts']/div[@class='post']")
        items = []
        coll = mongo.get_coll("link")
        url = response._get_url()
        account = int(url.split("?")[0].split("subjects/")[1])
        for post in posts:
            articel = post.xpath("div[@class='content']")
            title = articel.xpath("h3/a/text()").extract()[0].strip()
            href= articel.xpath("h3/a[@href]").xpath("@href").extract()[0].strip()
            source =  articel.xpath("div[@class='meta']/text()").extract()[0].strip()
            item = SharesItem()
            item["title"] = title
            item["href"] = href
            item["source"] = source
            item["account"] = account
            item["type"] = "toutiao.share"
            item["last_read_time"] = ""
            items.append(item)
            query_params = {
                "href":href,
                "account":account,
            }
            if coll.find(query_params).count()>0:
                continue
            else:
                coll.save(item)
        return items

class MyShareSpider(Spider):
    name = "myshares"
    allowed_domains = ["toutiao.io"]
    start_urls  = []
    start_urls.append("http://toutiao.io/subjects/"+str(73104))

    def parse(self, response):
        sel = Selector(response)
        pagination = sel.xpath("//div[@class='text-center']/ul/li[@class='last']/a")
        try:
            page = int(pagination.xpath("@href").extract()[0].split("=")[1])
        except:
            page = 1

        share_url = response._get_url()
        new_share_urls = []
        for i in range(page):
            new_share_urls.append(share_url + "?page=" + str(i+1))
        print new_share_urls

        for new_url in new_share_urls:
            yield Request(url=new_url, callback=self.parse_post)

    def parse_post(self,response):
        sel = Selector(response)
        posts = sel.xpath("//div[@class='posts']/div[@class='post']")
        items = []
        coll = mongo.get_coll("link")
        url = response._get_url()
        account = int(url.split("?")[0].split("subjects/")[1])
        for post in posts:
            articel = post.xpath("div[@class='content']")
            title = articel.xpath("h3/a/text()").extract()[0].strip()
            href= "https://toutiao.io" + articel.xpath("h3/a[@href]").xpath("@href").extract()[0].strip()
            source =  articel.xpath("div[@class='meta']/text()").extract()[0].strip()
            item = SharesItem()
            item["title"] = title
            item["href"] = href
            item["source"] = source
            item["account"] = account
            item["type"] = "toutiao.share"
            item["last_read_time"] = ""
            items.append(item)
            query_params = {
                "href":href,
                "account":account,
            }
            if coll.find(query_params).count()>0:
                continue
            else:
                coll.save(item)
        return items

