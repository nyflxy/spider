# -*- coding: utf-8 -*-

import os
import time
from logging import log
import json
from urllib import urlencode

import scrapy
from scrapy import Spider
from scrapy.selector import Selector
from scrapy.shell import inspect_response

import pdb

class UserSpider(Spider):
    name = 'zhihuusers'
    domain = 'https://www.zhihu.com'
    login_url = 'https://www.zhihu.com/login/email'
    _xsrf = ''

    def start_requests(self):
        yield scrapy.Request(
            url = self.domain,
            callback = self.request_captcha
        )

    def request_captcha(self, response):
        # 获取_xsrf值
        self._xsrf = response.css('input[name="_xsrf"]::attr(value)').extract()[0]
        # 获取验证码地址
        t = str(int(time.time()*1000))
        captcha_url = 'http://www.zhihu.com/captcha.gif?r=' + t + '&type=login'

        # 准备下载验证码
        yield scrapy.Request(
            url = captcha_url,
            meta = {
                '_xsrf': self._xsrf
            },
            callback = self.download_captcha
        )

    def download_captcha(self, response):
        # 下载验证码
        with open('captcha.gif', 'wb') as fp:
            fp.write(response.body)
        # 用软件打开验证码图片
        # os.system('open captcha.gif')
        os.system('eog captcha.gif') #Ubuntu
        # 输入验证码
        captcha = raw_input('Please enter captcha: ')
        yield scrapy.FormRequest(
            url = self.login_url,
            formdata = {
                'account': '15996458299',
                'password': '19922011nyf',
                '_xsrf': self._xsrf,
                'remember_me': 'true',
                'captcha': captcha
            },
            callback = self.after_login
        )


    def after_login(self, response):
        pdb.set_trace()
        sel = Selector(response)
        print sel.extract()
