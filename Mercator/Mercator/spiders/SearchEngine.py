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
graph = {}

index_coll = mongo.get_coll("index")
graph_coll = mongo.get_coll("graph")
coll = mongo.get_coll("search_urls")

class SearchEngineSpider(scrapy.Spider):
    name = "SearchEngineURLExtractor"
    start_urls = (
        'https://udacity.com/cs101x/urank/index.html',
    )

    # ----------------------------web_crawl--------------------------------
    def parse(self, response):
        sel = Selector(response)
        links = sel.xpath("//a")
        for link in links:
            url = parse_text(link.xpath("@href").extract())
            self.addqueue(url)

        print "==========QueueSet.qsize()============", QueueSet.qsize()
        while QueueSet.qsize():
            url = QueueSet.get(block=0)
            yield scrapy.Request(
                url=url,
                callback=self.parse_new,
            )

    def parse_new(self, response):
        sel = Selector(response)

        p_url = response._get_url()
        content = sel.extract()
        self.add_page_to_index(index_coll, p_url, content)
        global graph
        graph_urls = graph[p_url] = []
        links = sel.xpath("//a")
        for link in links:
            url = parse_text(link.xpath("@href").extract())
            graph_urls.append(url)
            self.addqueue(url)

        graph_objs = graph_coll.find()
        if len(graph_objs) == 0:
            graph_coll.insert_one(graph)
        else:
            graph_obj = graph_objs[0]
            graph_coll.update(graph_obj,graph)

        print "==========QueueSet.qsize()============", QueueSet.qsize()
        while QueueSet.qsize():
            url = QueueSet.get(block=0)
            yield scrapy.Request(
                url=url,
                callback=self.parse_new,
            )

    def addqueue(self, url):
        if url.find("udacity.com") > 0 and (url.find("https://") == 0 or url.find("http://") == 0):
            if not coll.find_one({"url": url}):
                coll.insert_one({"url": url})
                print url
                QueueSet.put(url, block=0)

    # --------------------------------build_index-----------------------------------
    def add_page_to_index(self,index_coll, url, content):
        words = content.split()
        for word in words:
            self.add_to_index(index_coll, word, url)

    def add_to_index(self,index_coll, keyword, url):
        keyword = keyword.replace(".","")
        index_obj = index_coll.find_one({"type":"udacity_com"})
        if index_obj:
            index = index_obj.get("index",{})
            if keyword in index:
                index[keyword].append(url)
            else:
                index[keyword] = [url]
            index_coll.save(index_obj)
        else:
            index = {}
            if keyword in index:
                index[keyword].append(url)
            else:
                index[keyword] = [url]
            index_coll.insert_one({"type":"udacity_com","index":index})

    def lookup(self,index_coll, keyword):
        index_obj = index_coll.find_one({"type": "udacity_com"})
        if index_obj:
            index = index_obj.get("index", {})
        else:
            index = {}
        if keyword in index:
            return index[keyword]
        else:
            return None

    # ---------------------------------page_rank---------------------------------

    def compute_ranks(self,graph):
        d = 0.8  # damping factor
        numloops = 10

        ranks = {}
        npages = len(graph)
        for page in graph:
            ranks[page] = 1.0 / npages

        for i in range(0, numloops):
            newranks = {}
            for page in graph:
                newrank = (1 - d) / npages
                for node in graph:
                    if page in graph[node]:
                        newrank = newrank + d * (ranks[node] / len(graph[node]))
                newranks[page] = newrank
            ranks = newranks
        return ranks

    def quick_sort(self,url_lst, ranks):
        url_sorted_worse = []
        url_sorted_better = []
        if len(url_lst) <= 1:
            return url_lst
        pivot = url_lst[0]
        for url in url_lst[1:]:
            if ranks[url] <= ranks[pivot]:
                url_sorted_worse.append(url)
            else:
                url_sorted_better.append(url)
        return self.quick_sort(url_sorted_better, ranks) + [pivot] + self.quick_sort(url_sorted_worse, ranks)

    def ordered_search(self,index, ranks, keyword):
        if keyword in index:
            all_urls = index[keyword]
        else:
            return None
        return self.quick_sort(all_urls, ranks)

