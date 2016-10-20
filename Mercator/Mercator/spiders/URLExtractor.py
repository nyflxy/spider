# -*- coding: utf-8 -*-

import os
import time
import hashlib,base64
import logging
from logging import log
import json
from urllib import urlencode

import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from scrapy.shell import inspect_response
import Mercator.mongo as mongo
import re
import pdb
import datetime

def parse_text(extract):
    if len(extract) == 0 :
        return ""
    else:
        return extract[0]

def get_new_url():
    return ""

import Queue
QueueSet = Queue.Queue()

coll = mongo.get_coll("urls")

class UrlextractorSpider(scrapy.Spider):
    name = "URLExtractor"
    start_urls = (
        'http://bbs.tianya.cn',
    )

    def parse(self, response):
        sel = Selector(response)
        url = response._get_url()
        print url
        links = sel.xpath("//a")
        for link in links:
            url = parse_text(link.xpath("@href").extract())
            if url.find("tianya.cn") > 0 and (url.find("https://") == 0 or url.find("http://") == 0):
                QueueSet.put(url,block=0)

        print "======================", QueueSet.qsize(), "========================="
        while QueueSet.qsize():
            url = QueueSet.get(block=False)
            yield scrapy.Request(
                url=url,
                callback=self.parse_new,
            )

    def parse_new(self,response):
        sel = Selector(response)
        url = response._get_url()
        print url
        links = sel.xpath("//a")
        for link in links:
            url = parse_text(link.xpath("@href").extract())
            if url.find("tianya.cn") > 0 and (url.find("https://") == 0 or url.find("http://") == 0):
                if not coll.find_one({"url": url}):
                    coll.insert_one({"url": url})
                    QueueSet.put(url, block=0)

        print "======================",QueueSet.qsize(),"========================="
        while QueueSet.qsize():
            url = QueueSet.get(block=False)
            yield scrapy.Request(
                url=url,
                callback=self.parse_new,
            )
