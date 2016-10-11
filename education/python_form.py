#coding=utf-8
import urllib  
import urllib2  
import cookielib  
import bs4  
import pdb
result = urllib2.urlopen("http://222.200.122.171:7771/login.aspx")
soup = bs4.BeautifulSoup(result, "html.parser")  
  
logindiv = soup.find("form", attrs={"name": "aspnetForm"})
Allinput = logindiv.findAll("input")  
inputData = {}  
for oneinput in Allinput:  
    if oneinput.has_attr('name'):  
        if oneinput.has_attr('value'):  
            inputData[oneinput['name']] = oneinput['value']  
        else:  
            inputData[oneinput['name']] = ""
inputData['ctl00$ContentPlaceHolder1$txtPas_Lib'] = '*****'
inputData['ctl00$ContentPlaceHolder1$txtUsername_Lib'] = '*******'
inputData["ctl00$ContentPlaceHolder1$btnLogin_Lib"] = inputData["ctl00$ContentPlaceHolder1$btnLogin_Lib"].encode("utf-8")
filename = 'cookie.txt'
# 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件  
cookie = cookielib.MozillaCookieJar(filename)  
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
postdata = urllib.urlencode(inputData)  
result2 = opener.open("http://222.200.122.171:7771/login.aspx", postdata)
cookie.save(ignore_discard=True, ignore_expires=True)  
#登录后 要访问的url  
bookUrl = "http://222.200.122.171:7771/user/userinfo.aspx"  
result=opener.open(bookUrl)  
print result.read()  
