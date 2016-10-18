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

import pdb

class UserSpider(Spider):
    name = 'users'
    domain = 'https://toutiao.io/ssignin'
    login_url = 'https://toutiao.io/auth/identity/callback'
    _xsrf = ''

    def __init__(self, url = None):
        self.user_url = url

    def start_requests(self):
        yield scrapy.Request(
            url = self.domain,
            callback = self.request_captcha
        )

    def request_captcha(self, response):
        # 获取_xsrf值
        self.authenticity_token = response.css('input[name="authenticity_token"]::attr(value)').extract()[0]
        yield scrapy.FormRequest(
            url = self.login_url,
            formdata = {
                'auth_key': '2547546731@qq.com',
                'password': '19922011nyf',
                'authenticity_token': self.authenticity_token,
            },
            callback = self.after_login
        )


    def after_login(self, response):
        sel = Selector(response)

        
