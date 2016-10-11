# coding=utf-8
import urllib
import urllib2
import cookielib
import bs4
import pdb

pdb.set_trace()
result = urllib2.urlopen("http://www.tbook.edu.cn/ListExamBook2.action")
soup = bs4.BeautifulSoup(result, "html.parser")

# PagNavForm = soup.find("form", attrs={"name": "pag_nav_form"})
# Allinput = PagNavForm.findAll("input")
inputData = {}
inputData = {"pageNo":1}
# for oneinput in Allinput:
#     if oneinput.has_attr('name'):
#         if oneinput.has_attr('value'):
#             inputData[oneinput['name']] = oneinput['value']
#         else:
#             inputData[oneinput['name']] = ""

filename = 'cookie.txt'
# 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
cookie = cookielib.MozillaCookieJar(filename)
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
postdata = urllib.urlencode(inputData)
result2 = opener.open("http://www.tbook.edu.cn/ListExamBook2.action", postdata)
soup = bs4.BeautifulSoup(result2, "html.parser")