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

import pdb

class ContentseenSpider(scrapy.Spider):
    name = "ContentSeen"
    allowed_domains = ["https://toutiao.io/explore"]
    start_urls = (
        'https://toutiao.io/explore/',
    )

    def __init__(self):
        self.fingerprint = ""

    def parse(self, response):
        sel = Selector(response)
        content = sel.extract()
        content_base64 = base64.b64encode(content.encode("utf-8"))
        fingerprint = hashlib.sha1(content_base64).hexdigest()
        self.fingerprint = fingerprint
        yield scrapy.Request(
            url=response._get_url(),
            callback=self.contentseen,
        )

    def contentseen(self,response):
        sel = Selector(response)