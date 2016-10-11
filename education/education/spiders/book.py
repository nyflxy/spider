#coding=utf-8
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
from education.items import BookItem
from education.libs import mongolib

import sys,pdb
import urllib
import urllib2
import cookielib
import bs4

book_coll = mongolib.get_coll("book")

#抓取教材
class UniversitySpider(Spider):
    name = "book"
    allowed_domains = ["edu.cn"]
    start_urls  = ["http://www.tbook.edu.cn/ListExamBook2.action"]

    def parse(self, response):
        inputData = {}
        desc_urls = []
        for i in range(0,106):
            inputData = {"pageNo": i}
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
            postdata = urllib.urlencode(inputData)
            result2 = opener.open("http://www.tbook.edu.cn/ListExamBook2.action", postdata)
            soup = bs4.BeautifulSoup(result2, "html.parser")
            trs = soup.find_all("tr")[2:]

            for tr in trs:
                try:
                    tds = tr.find_all("td")
                    book = BookItem()
                    book["name"] = tds[1].get_text()
                    book["author"] = tds[2].get_text()
                    book["company"] = tds[3].get_text()
                    book["publish_company"] = tds[4].get_text()
                    book["desc_url"] = "http://www.tbook.edu.cn" + tds[5].find("a").attrs["onclick"].split("'")[1]
                except Exception,e:
                    print e
                    continue

                desc_urls.append(book["desc_url"])

                query_params = {"name": book["name"]}
                if not book_coll.find_one(query_params):
                    book_coll.save(book)
                else:
                    book_coll.update(query_params, book)
                print book

        for desc_url in desc_urls:
            yield Request(url= desc_url,callback=self.parse_book)

    def parse_book(self,response):
        sel = Selector(response)
        name = sel.xpath('//*[@id="pagesRightSide"]/table/tr[1]/td[1]/text()').extract()[0]
        query_params = {"name":name}
        book = book_coll.find_one(query_params)
        if book:
            book["ISBN"] = sel.xpath('//*[@id="pagesRightSide"]/table/tr[1]/td[2]/text()').extract()[0].strip()
            book["publish_time"] = sel.xpath('//*[@id="pagesRightSide"]/table/tr[3]/td[2]').extract()[0].strip()
            book["size"] = sel.xpath('//*[@id="pagesRightSide"]/table/tr[3]/td[3]/text()').extract()[0].strip()
            book["subject"] = sel.xpath('//*[@id="pagesRightSide"]/table/tr[4]/td[1]/text()').extract()[0].strip()
            book["subject_type"] = sel.xpath('//*[@id="pagesRightSide"]/table/tr[4]/td[2]/text()').extract()[0].strip()
            book["price"] = sel.xpath('//*[@id="pagesRightSide"]/table/tr[4]/td[3]/text()').extract()[0].strip()
            book["range"] = sel.xpath('//*[@id="pagesRightSide"]/table/tr[5]/td/text()').extract()[0].strip()
            book_coll.update(query_params,book)
        print book