# -*- coding: utf-8 -*-

import os
import time
from logging import log
import json
from urllib import urlencode

import scrapy
from scrapy import Spider
from newbie.items import UserItem
from scrapy.selector import Selector
from scrapy.shell import inspect_response
import newbie.mongo as mongo

import pdb
link_coll = mongo.get_coll("subject")

def parse_text(extract):
    if len(extract) == 0 :
        return ""
    else:
        return extract[0]

class NewShares(Spider):
    name = 'newshares'
    domain = 'https://toutiao.io/latest'

    def start_requests(self):
        yield scrapy.Request(
            url=self.domain,
            callback=self.latest_page
        )

    def latest_page(self,response):
        sel = Selector(response)
        pagination = sel.xpath('//*[@id="main"]/div/div[2]/ul/li[8]/a')
        try:
            page = int(pagination.xpath("@href").extract()[0].split("=")[1])
        except:
            page = 1

        share_url = response._get_url()
        new_share_urls = []
        for i in range(page):
            new_share_urls.append(share_url + "?page=" + str(i + 1))
        print new_share_urls

        for new_url in new_share_urls:
            yield scrapy.Request(url=new_url, callback=self.newshares)

    def newshares(self,response):
        sel = Selector(response)
        shares = sel.xpath('//*[@id="main"]/div/div[1]/div[@class="post"]')
        coll = mongo.get_coll("newshares")
        for share in shares:
            item = {}
            title = share.xpath('div[2]/h3[@class="title"]/a/text()').extract()[0]
            href = "https://toutiao.io" + share.xpath('div[2]/h3[@class="title"]/a/@href').extract()[0]
            source = share.xpath('div[2]/div/text()').extract()[0].strip()

            item["title"] = title
            item["href"] = href
            item["source"] = source
            item["last_read_time"] = ""
            query_params = {
                "href": href,
            }
            if coll.find(query_params).count() > 0:
                coll.update({"href": href}, item)
                print "update:"
                print item
            else:
                coll.insert_one(item)
                print "create:"
                print item