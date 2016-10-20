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
    name = 'users'
    domain = 'https://toutiao.io/ssignin'
    login_url = 'https://toutiao.io/auth/identity/callback'
    _xsrf = ''

    def __init__(self, url = None):
        self.account = 0

    def start_requests(self):
        yield scrapy.Request(
            url = self.domain,
            callback = self.request_captcha
        )

    def request_captcha(self, response):
        # 获取 authenticity_token 值
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
        name = parse_text(sel.xpath('//*[@id="top"]/div/nav/ul/li[7]/a/span/text()').extract())
        myshares_href = parse_text(sel.xpath('//*[@id="top"]/div/nav/ul/li[7]/ul/li[2]/a/@href').extract())
        self.name = self.name
        self.myshares_href = "https://toutiao" + myshares_href

        # 我的独家号
        yield scrapy.Request(
            url="https://toutiao.io/u/196700/subjects",
            callback=self.my_subject,
        )

    def my_subject(self,response):
        sel = Selector(response)
        subject_href = parse_text(sel.xpath('//*[@id="main"]/div[3]/ul[1]/li/h5/a/@href').extract())
        subject_id = subject_href.split("/subjects/")[1]
        self.account = int(subject_id)

        # 我的收藏
        yield scrapy.Request(
            url="https://toutiao.io/favorites",
            callback=self.favorite_page,
        )
        # 我的分享
        yield scrapy.Request(
            url="https://toutiao.io/u/196700",
            callback=self.myshares_page,
        )
        # 个人设置
        yield scrapy.Request(
            url="https://toutiao.io/account/settings",
            callback=self.account_settings
        )

    def favorite_page(self,response):
        sel = Selector(response)
        pagination = sel.xpath("//div[@class='text-center']/ul/li[@class='last']/a")
        try:
            page = int(pagination.xpath("@href").extract()[0].split("=")[1])
        except:
            page = 1

        favorite_url = response._get_url()
        new_favorite_urls = []
        for i in range(page):
            new_favorite_urls.append(favorite_url + "?page=" + str(i + 1))
        print new_favorite_urls

        for new_url in new_favorite_urls:
            yield scrapy.Request(url=new_url, callback=self.favorites)

    def favorites(self,response):
        sel = Selector(response)
        favorites = sel.xpath('//*[@id="main"]/div/div/div[@class="post"]')
        coll = mongo.get_coll("link")
        for favorite in favorites:
            item = {}
            title = favorite.xpath('div[2]/h3[@class="title"]/a/text()').extract()[0]
            href = "https://toutiao.io" + favorite.xpath('div[2]/h3[@class="title"]/a/@href').extract()[0]
            source = favorite.xpath('div[2]/div/text()').extract()[0].strip()
            account = self.account

            item["title"] = title
            item["href"] = href
            item["source"] = source
            item["account"] = account
            item["type"] = "toutiao.favorite"
            item["last_read_time"] = ""
            query_params = {
                "href": href,
                "account": account,
                "type":item["type"],
            }
            if coll.find(query_params).count() > 0:
                coll.update(query_params,item)
                print "update:"
                print item
            else:
                coll.save(item)
                print "create:"
                print item

    def myshares_page(self,response):
        sel = Selector(response)
        pagination = sel.xpath("//div[@class='text-center']/ul/li[@class='last']/a")
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
            yield scrapy.Request(url=new_url, callback=self.myshares)

    def myshares(self,response):
        sel = Selector(response)
        myshares = sel.xpath('//*[@id="main"]/div[3]/div[1]/div[@class="post"]')
        coll = mongo.get_coll("link")
        for share in myshares :
            item = {}
            title = share.xpath('div[2]/h3[@class="title"]/a/text()').extract()[0]
            href = "https://toutiao.io" + share.xpath('div[2]/h3[@class="title"]/a/@href').extract()[0]
            source = share.xpath('div[2]/div/text()').extract()[0].strip()
            account = self.account

            item["title"] = title
            item["href"] = href
            item["source"] = source
            item["account"] = account
            item["type"] = "toutiao.share"
            item["last_read_time"] = ""
            query_params = {
                "href": href,
                "account": account,
            }
            if coll.find(query_params).count() > 0:
                coll.update({"href":href,"account":account,"type":item["type"]},item)
                print "update:"
                print item
            else:
                coll.insert_one(item)
                print "create:"
                print item

    def account_settings(self,response):
        sel = Selector(response)
        user_avatar = parse_text(sel.xpath('//*[@id="edit_user_73244"]/div[1]/div/img/@src').extract())
        nickname = parse_text(sel.xpath('//*[@id="user_name"]/@value').extract())
        github = parse_text(sel.xpath('//*[@id="user_github"]/@value').extract())
        toutiaoblog = parse_text(sel.xpath('//*[@id="user_blog"]/@value').extract())
        description = parse_text(sel.xpath('//*[@id="user_bio"]/@value').extract())
        email = parse_text(sel.xpath('//*[@id="user_email"]/@value').extract())
        account = dict(
            user_avatar = user_avatar,
            nickname = nickname,
            github = github,
            toutiaoblog = toutiaoblog,
            description = description,
            email = email,
            account=self.account,
        )

        coll = mongo.get_coll('account')
        if coll.find({"email":email}).count() == 0:
            coll.insert_one(account)
            self.email = email
            print account
        else:
            coll.update({"email":email},account)


        
