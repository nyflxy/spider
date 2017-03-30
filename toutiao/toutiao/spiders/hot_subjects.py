#coding=utf-8
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
from newbie.items import SubjectsItem
import newbie.mongo as mongo

import sys,pdb

subject_coll = mongo.get_coll("subject")

class MyShareSpider(Spider):
    name = "hot_subjects"
    allowed_domains = ["toutiao.io"]
    start_urls  = []
    accounts = []
    cr = subject_coll.find().sort("count",-1)[0:100]
    for account in cr:
        accounts.append(account["account"])
    for i in accounts:
        start_urls.append("http://toutiao.io/subjects/"+str(i))

    def parse(self, response):
        sel = Selector(response)
        subject_name = sel.xpath("//div[@class='text-center m-b']/h3/text()").extract()[0].strip()
        url = response.url
        subject = sel.xpath("//div[@class='wrapper bg-white b-b subject-nav-pills']/ul/li[1]")
        sub_subject = sel.xpath("//div[@class='wrapper bg-white b-b subject-nav-pills']/ul/li[2]")
        account = subject.xpath("a/@href").extract()[0].split("/subjects/")[1]
        count = subject.xpath("a/span[@class='count']/text()").extract()[0]
        sub_count = sub_subject.xpath("a/span[@class='count']/text()").extract()[0]

        item = SubjectsItem()
        item["account"] = account
        item["name"] = subject_name
        item["count"] = int(count)
        item["sub_count"] = int(sub_count)
        item["url"] = url
        query_params = {"name":item["name"]}
        if not subject_coll.find_one(query_params):
            subject_coll.save(item)
            item["_id"] = str(item["_id"])
        else:
            subject_coll.update(query_params,item)
        return item



