# -*- coding: utf-8 -*-
#http://www.jianshu.com/p/135393181bf3
import urllib2
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
url = "http://www.ip181.com/"
proxy_support = urllib2.ProxyHandler({'http':'121.40.108.76'})
#参数是一个字典{'类型':'代理ip:端口号'}
opener = urllib2.build_opener(proxy_support)
#定制opener
opener.add_handler=[('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36')]
#add_handler给加上伪装
urllib2.install_opener(opener)
response = urllib2.urlopen(url)

print response.read().decode('gbk')