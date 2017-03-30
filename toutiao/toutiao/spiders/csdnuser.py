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

def parse_text(extract):
    if len(extract) == 0 :
        return ""
    else:
        return extract[0]

class UserSpider(Spider):
    name = 'csdnusers'
    domain = 'https://passport.csdn.net/account/login'
    login_url = 'https://passport.csdn.net/account/login'

    def __init__(self, url = None):
        self.account = ""

    def start_requests(self):
        yield scrapy.Request(
            url = self.domain,
            callback = self.request_captcha
        )

    def request_captcha(self, response):
        # 获取 authenticity_token 值
        lt = response.css('input[name="lt"]::attr(value)').extract()[0]
        execution = response.css('input[name="execution"]::attr(value)').extract()[0]
        _eventId = response.css('input[name="_eventId"]::attr(value)').extract()[0]
        rememberMe = response.css('input[name="rememberMe"]::attr(value)').extract()[0]
        yield scrapy.FormRequest(
            url = self.login_url,
            formdata = {
                'username': '2547546731@qq.com',
                'password': '19922011nyf',
                'rememberMe':rememberMe,
                'lt': lt,
                'execution':execution,
                '_eventId':_eventId,
                'fdsf':"fsdf"
            },
            callback = self.after_login
        )

    def after_login(self, response):
        sel = Selector(response)
        print sel.extract()

class LoginSpider(scrapy.Spider):
    name = 'toutiaologin'
    start_urls = ['https://toutiao.io/ssignin']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'auth_key': '2547546731@qq.com',
                'password': '19922011nyf',
            },
            callback=self.after_login
        )

    def after_login(self, response):
        if "authentication failed" in response.body:
            self.logger.error("Login failed")
            print "Login failed"
            return
        else:
            print response.body

class LoginSpider(scrapy.Spider):
    name = 'doubanlogin'
    start_urls = ['https://www.douban.com/']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={
                'form_email': '2547546731@qq.com',
                'form_password': '19922011nyf',
                'source':"index_nav",
            },
            callback=self.after_login
        )

    def after_login(self, response):
        if "authentication failed" in response.body:
            self.logger.error("Login failed")
            print "Login failed"
            return
        else:
            print response.body