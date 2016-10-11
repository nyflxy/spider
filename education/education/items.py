# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SubjectsItem(scrapy.Item):

    _id = scrapy.Field()

    #学科门类
    category= scrapy.Field()

    #一级学科
    first_level = scrapy.Field()

    #二级学科
    second_level = scrapy.Field()

class UniversityItem(scrapy.Item):

    _id = scrapy.Field()

    # university spider
    #学校名称
    name = scrapy.Field()

    #主管部门
    department = scrapy.Field()

    #所在地
    city = scrapy.Field()

    #办学层次
    level = scrapy.Field()

    # university1 spider 中国高校院校等级
    #类别
    type = scrapy.Field()

    #是否是211
    is_211 = scrapy.Field()

    #是否是985
    is_985 = scrapy.Field()

    # 是否拥有研究生院
    has_graduate_school = scrapy.Field()

    #university2 spider 高校本科招生信息网站
    zhaosheng_url = scrapy.Field()

    #university3 spider souhu url 搜狐大学信息链接
    souhu_url = scrapy.Field()

    # 重点学科
    key_subject_count = scrapy.Field()

    # 院士
    academician_count = scrapy.Field()

    # 博士点
    Doctor_point_count = scrapy.Field()

    # 硕士点
    Master_Degree_count = scrapy.Field()

    # 高校地点
    address = scrapy.Field()

    # 咨询电话
    phone = scrapy.Field()

    # 高校网站
    website = scrapy.Field()

    # 学校简介
    description = scrapy.Field()

    # 图片
    image = scrapy.Field()

    # 专业设置url
    major_url = scrapy.Field()

    # 专业设置html
    majorsetting = scrapy.Field()

    # 专业设置
    majors = scrapy.Field()

class BookItem(scrapy.Item):

    _id = scrapy.Field()

    # 书名
    name = scrapy.Field()

    # 主要作者
    author = scrapy.Field()

    # 第一作者单位
    company = scrapy.Field()

    # 出版社
    publish_company = scrapy.Field()

    # 详细信息url
    desc_url = scrapy.Field()

    # 书号
    ISBN = scrapy.Field()

    # 出版时间
    publish_time = scrapy.Field()

    #开本
    size = scrapy.Field()

    # 学科
    subject = scrapy.Field()

    # 课程类型
    subject_type = scrapy.Field()

    # 定价
    price = scrapy.Field()

    # 适用范围
    range = scrapy.Field()



