#coding=utf-8
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
from education.items import SubjectsItem
from education.libs import mongolib

import sys,pdb

subject_coll = mongolib.get_coll("subject")

class MyShareSpider(Spider):
    name = "subjects"
    allowed_domains = ["*"]
    start_urls  = ["http://127.0.0.1/subject.htm"]

    def parse(self, response):
        sel = Selector(response)
        tables = sel.xpath("//table")

        items = []
        for table in tables:
            trs = table.xpath("tr")[1:]
            for tr in trs:

                item = SubjectsItem()
                item["category"] = ""
                item["first_level"] = {}
                item["second_level"] = []

                tds = tr.xpath("td")

                subject_category = tds[0].xpath("text()").extract()[0]
                item["category"] = subject_category

                first_level_discipline = tds[1].xpath("text()").extract()[0]
                item["first_level"] = dict(
                    code = first_level_discipline.split(" ")[0],
                    name = first_level_discipline.split(" ")[1],
                )

                divs = tds[2].xpath("div")
                for div in divs:
                    second_level_disciplines = div.xpath("text()").extract()[0]
                    try:
                        code = second_level_disciplines.split(" ")[0]
                        name = second_level_disciplines.split(" ")[1]
                    except Exception,e:
                        print second_level_disciplines
                        code = ""
                        name = second_level_disciplines

                    item["second_level"].append(dict(
                        code=code,
                        name=name,
                    ))

                query_params = {"category":item["category"],'first_level':item["first_level"]}
                if not subject_coll.find_one(query_params):
                    subject_coll.save(item)
                else:
                    subject_coll.update(query_params,item)
                items.append(item)
        return items



