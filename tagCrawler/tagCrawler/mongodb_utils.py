#-*- coding: utf-8 -*-
import pymongo , hashlib
import pdb

# 定义连接池
CONNECTION_POOL = []
MIN_CONNECTION = 10
MAX_CONNECTION = 50
MONGO_HOST = "127.0.0.1"
MONGO_PORT = 27017

# 初始化连接池
def initConnectionPool():
    if len(CONNECTION_POOL) < MAX_CONNECTION :
        client = pymongo.MongoClient(MONGO_HOST,int(MONGO_PORT))
        CONNECTION_POOL.append(client)
        initConnectionPool()
    else:
        print "初始化连接池完毕，当前连接数"+str(MIN_CONNECTION)+","

# 建立连接的函数
def getConnection():
    if len(CONNECTION_POOL) == 0:
        initConnectionPool()

    # 从连接池中取得连接
    conn = CONNECTION_POOL.pop()
    return conn

# 回收连接到连接池
def closeConnection(conn):
    if len(CONNECTION_POOL) < MAX_CONNECTION:
        CONNECTION_POOL.append(conn)

# 配置数据库信息
def configDB(db_name,table_name):
    # 获取操作mongo的连接
    conn = getConnection()

    # 查询数据库
    db = conn[db_name]
    table = db[table_name]

    return conn,table

# 保存用户信息的接口
def saveUserInfo(user):
    # 配置查询数据库
    conn,userinfo = configDB('teamup','USER')
    usersha1 = user["usersha1"]
    # 查询记录的数量
    count =userinfo.find({'usersha1':usersha1}).count()
    if count :
        userinfo.update({'usersha1':usersha1},{'$set':user})
    else:
        userinfo.save(user)

    # 释放连接到连接池
    closeConnection(conn)

# 获取用户信息的接口
def getUserInfo(usersha1):
    # 配置查询数据库
    conn,userinfo = configDB('teamup','USER')
    user =userinfo.find_one({'usersha1':usersha1})
    # 释放连接到连接池
    closeConnection(conn)

    return user

# 删除用户的信息
def deleteUserInfo(usersha1):
    # 配置查询数据库
    conn,userinfo = configDB('teamup','USER')
    userinfo.remove({'usersha1':usersha1})
    # 释放连接到连接池
    closeConnection(conn)

#保存抓取的标签数据
def saveTag(tag) : 
    # 配置查询数据库
    conn,taginfo = configDB('code','tag')
    name = tag["tag"]["name"]
    href = tag["tag"]["href"]
    sha1 = hashlib.sha1()
    sha1.update(href)
    tag_sha1 = sha1.hexdigest()

    tag_obj = { "tag_sha1" : tag_sha1,"name":name,"href":href }
    # 查询记录的数量
    count =taginfo.find({'tag_sha1':tag_sha1}).count()
    if count :
        taginfo.update({'tag_sha1':tag_sha1},{'$set':tag_info})
    else:
        taginfo.save(tag_obj)

#保存博客
def saveBlog(blog_item) : 
    # 配置查询数据库
    conn,bloginfo = configDB('code','blog')
    blog_href = blog_item["blog_href"] 
    count = bloginfo.find({"blog_href":blog_href}).count()
    blog_obj = {}
    blog_obj["blog_href"] = blog_item["blog_href"]
    blog_obj["blog_name"] = blog_item["blog_name"]

    if count :
        bloginfo.update({'blog_href':blog_href},{'$set':blog_obj})
    else:
        bloginfo.save(blog_obj)

    # 释放连接到连接池
    closeConnection(conn)
