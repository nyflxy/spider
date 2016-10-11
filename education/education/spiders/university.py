#coding=utf-8
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy import Request
from education.items import UniversityItem
from education.libs import mongolib

import sys,pdb

university_coll = mongolib.get_coll("university")

#抓取中国高校名单
class UniversitySpider(Spider):
    name = "university"
    allowed_domains = ["*"]
    start_urls  = ["http://www.chinadegrees.cn/xwyyjsjyxx/xwsytjxx/qgptgxmd/qgptgxmd.html"] #普通高校名单（截至2013年6月21日）

    def parse(self, response):
        sel = Selector(response)
        tbody = sel.xpath("//table[1]/tbody")
        trs = tbody.xpath("tr")

        items = []
        for tr in trs[3:]:
            tds = tr.xpath("td")
            if len(tds) == 1:
                print tds[0].xpath("strong/text()").extract()[0]
            else:
                item = UniversityItem()
                item["name"] = tds[1].xpath("text()").extract()[0]
                item["department"] = tds[2].xpath("text()").extract()[0]
                item["city"] = tds[3].xpath("text()").extract()[0]
                item["level"] = tds[4].xpath("text()").extract()[0]
                query_params = {"name":item["name"]}
                if not university_coll.find_one(query_params):
                    university_coll.save(item)
                else:
                    university_coll.update(query_params,item)
                items.append(item)
        return items

#抓取中国高校院校等级相关信息
class University1Spider(Spider):
    name = "university1"
    allowed_domains = ["chinadegrees.cn"]
    start_urls  = ["http://www.chinadegrees.cn/xwyyjsjyxx/xwsytjxx/274346.shtml",
                            "http://www.chinadegrees.cn/xwyyjsjyxx/xwsytjxx/274346_2.shtml",
                            "http://www.chinadegrees.cn/xwyyjsjyxx/xwsytjxx/274346_3.shtml"]

    def parse(self, response):
        sel = Selector(response)
        tbody = sel.xpath("//table[1]/tbody")
        trs = tbody.xpath("tr")

        items = []
        for tr in trs[1:]:
            tds = tr.xpath("td")
            try:
                name = tds[0].xpath("p/span/text()").extract()[0]
            except:
                continue
            query_params = {"name":name}
            university = university_coll.find_one(query_params)
            if university :
                university["type"] = tds[1].xpath("p/span/text()").extract()[0]
                if tds[4].xpath("p/span/text()") == []:
                    university["is_211"] = False
                else:
                    university["is_211"] = True

                if tds[5].xpath("p/span/text()") == []:
                    university["is_985"] = False
                else:
                    university["is_985"] = True

                if tds[6].xpath("p/span/text()") == []:
                    university["has_graduate_school"] = False
                else:
                    university["has_graduate_school"] = True
                university_coll.save(university)
        return items

#抓取中国高校本科招生网站链接
class University2Spider(Spider):
    name = "university2"
    allowed_domains = ["gk114.com"]
    start_urls  = ["http://www.gk114.com/"]

    def parse(self, response):
        sel = Selector(response)
        trs = sel.xpath("/html/body/table[12]/tr/td[1]/table/tr/td/table/tr[2]/td/table/tr")

        new_urls = []
        for tr in trs:
            tds = tr.xpath("td")
            for td in tds:
                new_url = "http://www.gk114.com/" + td.xpath("a/@href").extract()[0]
                new_urls.append(new_url)

        print new_urls
        for new_url in new_urls:
            yield Request(url=new_url, callback=self.parse_post)

    def parse_post(self, response):
        sel = Selector(response)
        lis = sel.xpath("//ul/li")
        items = []
        for li in lis:
            try:
                name = li.xpath("a/font/text()").extract()[0]
            except:
                name = li.xpath("a/text()").extract()[0]

            zhaosheng_url = li.xpath("a/@href").extract()[0]
            query_params = {
                "name":name,
            }
            university = university_coll.find_one(query_params)
            if university:
                university["zhaosheng_url"] = zhaosheng_url
                university_coll.save(university)

            print name,zhaosheng_url

# 搜狐大学信息库 http://daxue.learning.sohu.com/college/index-htm-page-1.html

#抓取中国高校概况网页链接
class University3Spider(Spider):
    name = "university3"
    allowed_domains = ["sohu.com"]
    start_urls  = ["http://daxue.learning.sohu.com/college/index-htm-page-1.html"]

    def parse(self,response):
        sel = Selector(response)
        page_str = sel.xpath("/html/body/div[7]/div/div[2]/div[2]/cite/text()").extract()[0]
        page_str = page_str.encode("utf-8")
        page = int(page_str.split("共")[1].split("条")[0])
        new_urls = []
        for i in range(1,page+1):
            new_url = "http://daxue.learning.sohu.com/college/index-htm-page-%s.html"%i
            new_urls.append(new_url)

        for new_url in new_urls:
            yield Request(url=new_url, callback=self.parse_sohu_url)

    def parse_sohu_url(self, response):
        sel = Selector(response)
        trs = sel.xpath("/html/body/div[7]/div/div[2]/div[1]/table[1]/tbody/tr")[1:]

        new_urls = []
        for tr in trs:
            name = tr.xpath("td[1]/a/text()").extract()[0]
            new_url = tr.xpath("td[1]/a/@href").extract()[0]

            query_params = {
                "name":name,
            }
            university = university_coll.find_one(query_params)
            if university :
                university["souhu_url"] = "http://daxue.learning.sohu.com" + new_url + "introduction.html"
                university_coll.save(university)
                new_urls.append(university["souhu_url"])
            else:
                print name,"找不到该高校"

        print new_urls
        for new_url in new_urls:
            yield Request(url=new_url, callback=self.parse_post)

    # 学校概况信息和学校简介
    def parse_post(self, response):
        sel = Selector(response)
        name = sel.xpath("/html/body/div[4]/h3/a/text()").extract()[0]
        query_params = {
            "name": name,
        }
        university = university_coll.find_one(query_params)
        if university:
            ps = sel.xpath("/html/body/div[5]/div[1]/div[1]/div/p")[1:7]
            key_subject_count = ps[1].xpath("span[1]/text()").extract()[0]
            academician_count = ps[1].xpath("span[2]/text()").extract()[0]
            Doctor_point_count = ps[1].xpath("span[3]/text()").extract()[0]
            Master_Degree_count = ps[1].xpath("span[4]/text()").extract()[0]
            address = ps[3].xpath("text()").extract()[0]
            phone = ps[4].xpath("text()").extract()[0]
            website = ps[5].xpath("a/@href").extract()[0]
            description = sel.xpath("/html/body/div[5]/div[1]/div[2]/div/p/text()").extract()[0].encode("utf-8").strip()
            image = sel.xpath("/html/body/div[5]/div[1]/div[1]/dl/dt/img/@src").extract()[0]
            major_url = "http://daxue.learning.sohu.com" + sel.xpath("/html/body/div[5]/div[1]/div[1]/div/p[13]/span[2]/a/@href").extract()[0]

            university.update(dict(
                key_subject_count = key_subject_count,
                academician_count = academician_count,
                Doctor_point_count = Doctor_point_count,
                Master_Degree_count = Master_Degree_count,
                address = address,
                phone = phone,
                website = website,
                description = description,
                image = image,
                major_url = major_url,
            ))
            university_coll.save(university)

            yield Request(url=major_url,callback=self.parse_majors)

    # 学校专业设置
    def parse_majors(self,response):
        sel = Selector(response)
        name = sel.xpath("/html/body/div[4]/h3/a/text()").extract()[0]
        query_params = {
            "name": name,
        }
        university = university_coll.find_one(query_params)
        majors = []
        if university:
            majorsetting = sel.xpath("/html/body/div[5]/div[1]/div[2]/div/div/table").extract()[0]
            trs = sel.xpath("/html/body/div[5]/div[1]/div[2]/div/div/table/tr")[1:]
            for tr in trs:
                major = {}
                first_level_name = tr.xpath("td[1]/text()").extract()[0].encode("utf-8")
                second_level_name = tr.xpath("td[2]/a/text()").extract()[0].encode("utf-8")
                second_level_url = tr.xpath("td[2]/a/@href").extract()[0]
                major["first_level"]  = {
                    "name": first_level_name,
                }
                major["second_level"] = {
                    "name": second_level_name,
                    "url": second_level_url,
                }

                majors.append(major)

                yield Request(url=second_level_url, callback=self.parse_subject_desc)

            university["majors"] = majors
            university_coll.save(university)

    def parse_subject_desc(self,response):
        sel = Selector(response)
        name = sel.xpath("/html/body/div[4]/h3/a/text()").extract()[0]
        query_params = {
            "name": name,
        }
        university = university_coll.find_one(query_params)
        if university:
            subject_name = sel.xpath("/html/body/div[5]/div[1]/div[2]/a/h4/text()").extract()[0].encode("utf-8").split("专业介绍")[0]
            subject_intro_html = sel.xpath("/html/body/div[5]/div[1]/div[2]/div/p").extract()[0]
            subject_intro = sel.xpath("/html/body/div[5]/div[1]/div[2]/div/p/text()").extract()[0].encode("utf-8").strip()
            desc = {}
            desc.update(dict(
                intro_html = subject_intro_html,
                intro = subject_intro,
            ))
            for major in university["majors"]:
                if major.get("second_level",{}).get("name","").encode("utf-8") == subject_name:
                    major["second_level"]["desc"] = desc
            university_coll.save(university)
            print university



