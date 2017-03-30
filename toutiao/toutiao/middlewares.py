#coding=utf-8
import pdb
import scrapy
import scrapy.downloadermiddlewares


class NewbieDownloaderMiddleware(scrapy.downloadermiddlewares):

    def process_request(self,request,spider):
        pdb.set_trace()
        return request

    def process_response(self,request,response,spider):
        return response

    def process_exception(self,request,exception,spider):
        return None


