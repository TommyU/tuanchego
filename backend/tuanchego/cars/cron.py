# -*- coding:utf-8 -*-
from django_cron import CronJobBase, Schedule
import urllib2
from urlparse import urlparse
from pyquery import PyQuery as pq
from lxml.html import HtmlElement
from .models import Brand,Serie,Car
import traceback
import datetime
import time
import thread
import os
from os import makedirs
import threading
STATIC_DIR = os.path.dirname(os.path.dirname(__file__))
LOCK = threading.Lock()


def _get_page_dom_proxy(targetUrl):
    # 代理服务器
    proxyHost = "proxy.abuyun.com"
    proxyPort = "9020"

    # 代理隧道验证信息
    proxyUser = "HQ620C4CGV80G38D"
    proxyPass = "C0E29382DEB4F7F3"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
      "host" : proxyHost,
      "port" : proxyPort,
      "user" : proxyUser,
      "pass" : proxyPass,
    }

    proxy_handler = urllib2.ProxyHandler({
        "http"  : proxyMeta,
        "https" : proxyMeta,
    })

    opener = urllib2.build_opener(proxy_handler)

    #opener.addheaders = [("Proxy-Switch-Ip", "yes")]
    urllib2.install_opener(opener)
    return urllib2.urlopen(targetUrl)

def _get_page_dom(url, no_proxy=True):
    if no_proxy:
        req = urllib2.Request(url)
        req.add_header("Reffer","http://bzclk.baidu.com/adrc.php?t=06KL00c00fZ0gw60_wIm05-WcfahOeVm00000Ap-Gj300000Vs18-F.THLPkUrd1x60UWdBmy-bIfK15H9buj0YujKBnj0dnHfsuWc0IHYzwRP7n1c4nHf4fHckfRPAwW-KrDmLnHFDfYnzPWm4r0K95gTqFhdWpyfqnWbsPjRYPHDsriusThqbpyfqnHm0uHdCIZwsrBtEILILQMwdmy4WpAR8mvqV5vnqmhfsP7K7Hbn0mLFW5HmznjRd&tpl=tpl_10087_14396_1&l=1050977638&attach=location%3D%26linkName%3D%25E6%25A0%2587%25E9%25A2%2598%26linkText%3D%25E5%259B%25A2%25E8%25BD%25A6%25E7%25BD%2591-%25E4%25B8%25AD%25E5%259B%25BD%25E4%25B8%2593%25E4%25B8%259A%25E6%25B1%25BD%25E8%25BD%25A6%25E7%2594%25B5%25E5%2595%2586%25E5%25B9%25B3%25E5%258F%25B0%26xp%3Did(%2522m3ab65456%2522)%252FDIV%255B1%255D%252FDIV%255B1%255D%252FDIV%255B1%255D%252FH2%255B1%255D%252FA%255B1%255D%26linkType%3D%26checksum%3D95&ie=utf-8&f=8&tn=baidu&wd=%E5%9B%A2%E8%BD%A6&rqlang=cn&inputT=3713")
        req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0")
        resp = urllib2.urlopen(req)
    else:
        try:
            resp = _get_page_dom_proxy(url)
        except:
            print('proxy got some problem,maybe...,sleep 3 senconds...')
            time.sleep(3)
            resp = _get_page_dom_proxy(url)
    page_text_raw = resp.read()
    page_text_unicode = unicode(page_text_raw,'utf-8')
    return pq(page_text_unicode)

class GetBrandJob(CronJobBase):
    RUN_EVERY_MINS = 120 # every 2 hours
    URL="http://www.tuanche.com/che/"
    SELECTOR=".charactersSlidBox"
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'cars.cron.GetBrandJob'    # a unique code

    def do(self):
        """
        target DOM:
        <div class="charactersSlidBox">
            <span class=""><a rel="A" data-hot="0" class="styleName " href="http://www.tuanche.com/chef25/">奥迪</a></span>
            <span class="hide"><a rel="A" data-hot="" class="styleName " href="http://www.tuanche.com/chef63/">阿斯顿·马丁</a></span>
            ...
        </div>
        """
        try:
            print("[%s] looking for brands data...."%(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            dom = _get_page_dom(self.URL)
            print("data got!")
            brands = []
            
            for span in dom(self.SELECTOR).items('span'):
                for link in span("a"):
                    if isinstance(link , HtmlElement):
                        rel = link.get("rel","")
                        name = link.text
                        tc_url = link.get("href","")
                        brands.append([rel, name, tc_url])
                    else:
                        pass
            print("%d brands found!"%len(brands))
            imported=0
            for line in brands:
                rel,name, tc_url=line
                if not rel:continue
                try:
                    Brand.objects.get(initial=rel, name=name)
                except:
                    imported+=1
                    Brand(initial=rel, name=name, tc_url=tc_url).save()
            print("%d new Brand imported!"%imported)
        except:
            print(traceback.format_exc())


class GetCarJob(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 hours
    #URL="http://www.tuanche.com/che/"
    SELECTOR=".searchListC"
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'cars.cron.GetCarJob'    # a unique code

    def do(self):
        """
        target DOM1(for tag):
            <div class="charactersSlidTwo">
                <div class="charactersSlidBox">  
                        <span>  <a class="styleName-in " href="/che31/">一汽奥迪</a></span>
                        <span>  <a class="styleName-in " href="/che193/">奥迪(进口)</a></span>
                        <span>  <a class="styleName-in " href="/che194/">奥迪RS</a></span>
                </div>
            </div>
        target DOM2(for car):
        <div class="searchNoinfo">
            <p>
                <em></em>
                <span>未找到符合条件的车型，请修改已选条件！</span>
            </p>
        </div>
        ----or -----
        <div class="searchList">
            <ul class="searchListC">
               <li>
                        <div class="imgBox">
                            
                                <a href="http://sz.tuanche.com/c60/tuan/" target="_blank">
                            

                                <img src="http://pic.tuanche.com/car/20160321/1458531404258278_o.jpg" alt="">
                                
                                    <div class="searchMask"></div>
                                    <div class="searchMaskText">
                                        <p>车型概述</p>
                                        <p>1.外形改变意在展现时尚</p>
                                        <p>2.内部空间没变依旧宽敞</p>
                                        <p>3.取消顶配车型价格亲民</p>
                                    </div>
                                
                                <div class="caricoBox"><img src="http://pic.tuanche.com/car/20170222/14877499257433743_s.jpg" alt=""></div>
                            
                                </a>
                            
                        </div>
                        <div class="searchListText">
                            <p>
                                <span> <a href="http://sz.tuanche.com/c60/tuan/" target="_blank">雅阁</a></span>
                                <samp>累计报名<i>13991</i>人</samp>
                            </p>
                            
                                <a class="goin" href="http://sz.tuanche.com/c60/tuan/">团购报名 </a>
                            
                        </div>
               </li>
               <li></li>
               ...
            </ul>
        </div>
        """
        time.sleep(1)
        try:
            print("[%s] looking for cars data...."%(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            for brand in Brand.objects.all():
                time.sleep(1)
                print("processing brand:%s"%brand.name)
                if not brand.tc_url:
                    continue
                dom = _get_page_dom(brand.tc_url)
                print("data got!")

                #get all sub serie(target DOM1)
                sub_serie=[]
                
                for div in dom(".charactersSlidTwo").items("div.charactersSlidBox"):
                    for span in pq(div)("span"):
                        for link in pq(span)("a.styleName-in"):
                            sub_serie.append({
                                    'href':link.get('href',''),
                                    'name':link.text
                                })

                #get all car info by sub serie(target DOM2)
                for page in sub_serie:
                    uri,tag = page['href'],page['name']
                    if not uri:continue
                    time.sleep(1)
                    print('processing sub category: %s'%tag)
                    dom = _get_page_dom('http://www.tuanche.com'+uri)
                    print('data got!')
                    cars = []
                    i=0
                    #check whether no result
                    if [x for x in dom("div.searchNoinfo")]:
                        print('no data for sub category:%s, continue....'%tag)
                        continue
                    for li in dom(self.SELECTOR).items('li'):
                        img_url=''
                        logo_url=''
                        description=''
                        name=''
                        for div in li(".imgBox"):
                            if i==0:
                                i=1
                                import pdb
                                #pdb.set_trace()
                            div = pq(div)
                            for img in div("img"):
                                if isinstance(img , HtmlElement):#get car img
                                    img_url = img.get("src","")
                                    break
                                else:
                                    pass
                            for _div in div(".searchMaskText"):#get car decription
                                description ="\n".join([x.text() for x in pq(_div).items("p")])
                                #import pdb
                                #pdb.set_trace()
                            for _logo_div in div(".caricoBox"):#get car logo
                                for logo_img in pq(_logo_div)("img"):
                                    logo_url = logo_img.get("src","")
                                #import pdb
                                #pdb.set_trace()



                        for div in li(".searchListText"):#get car name
                            div = pq(div)
                            for p in div("p"):
                                p=pq(p)
                                for span in p("span"):
                                    span = pq(span)
                                    for link in span("a"):
                                        name = link.text
                        cars.append([img_url, logo_url, description, name])


                    print("%d cars found!"%len(cars))
                    imported=0
                    for line in cars:
                        img_url, logo_url, description ,name=line
                        if not img_url:continue
                        try:
                            Car.objects.get(brand=brand.id, name=name)
                        except:
                            imported+=1
                            Car(brand=brand, 
                                name=name, 
                                img_path=img_url, 
                                tag=tag,
                                logo_url=logo_url,
                                description = description).save()
                    print("%d new cars imported!"%imported)
        except:
            print(traceback.format_exc())

class RefreshCarAttrJob(CronJobBase):
    #URL="http://www.tuanche.com/che/"
    SELECTOR=".searchListC"
    
    #abstract attributes
    RUN_EVERY_MINS = 1 # every 2 hours
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'cars.cron.RefreshCarPriceJob'    # a unique code
    JOB_CODE='price'
    target_list=[]
    target_name_list=[]

    def update_car(car_obj, list_index):
        """
        set car_obj attrbutes according to list_index of target_list
        """
        raise Exception("update car not implemented!")

    def do(self):
        """
        <div class="searchNoinfo">
            <p>
                <em></em>
                <span>未找到符合条件的车型，请修改已选条件！</span>
            </p>
        </div>
        ----or -----
        <div class="searchList">
            <ul class="searchListC">
               <li>
                        <div class="imgBox">
                            
                                <a href="http://sz.tuanche.com/c60/tuan/" target="_blank">
                            

                                <img src="http://pic.tuanche.com/car/20160321/1458531404258278_o.jpg" alt="">
                                
                                    <div class="searchMask"></div>
                                    <div class="searchMaskText">
                                        <p>车型概述</p>
                                        <p>1.外形改变意在展现时尚</p>
                                        <p>2.内部空间没变依旧宽敞</p>
                                        <p>3.取消顶配车型价格亲民</p>
                                    </div>
                                
                                <div class="caricoBox"><img src="http://pic.tuanche.com/car/20170222/14877499257433743_s.jpg" alt=""></div>
                            
                                </a>
                            
                        </div>
                        <div class="searchListText">
                            <p>
                                <span> <a href="http://sz.tuanche.com/c60/tuan/" target="_blank">雅阁</a></span>
                                <samp>累计报名<i>13991</i>人</samp>
                            </p>
                            
                                <a class="goin" href="http://sz.tuanche.com/c60/tuan/">团购报名 </a>
                            
                        </div>
               </li>
               <li></li>
               ...
            </ul>
        </div>
        """
        time.sleep(1)
        taget_list =self.target_list #['http://www.tuanche.com/chep%d'%i for i in range(1,7)]
        taget_names =self.target_name_list# ['5万以下','5-10万','10-15万','15-20万','20-30万','30万以上']
        try:
            print("[%s] looking for cars %s data...."%(
                datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                self.JOB_CODE#abstract attribute
                ))
            for i in range(len(taget_list)):
                print("processing %s:%s"%(self.JOB_CODE , taget_names[i]))
                #if i>0:break#for debug
                if not taget_list[i]:
                    continue
                url = taget_list[i]
                #get all sub serie(target DOM1)
                for pi in range(1,101):
                    #if pi>2:break#for debug
                    hasNextPage = True
                    if pi!=1:
                        url = taget_list[i] + 'n'+str(pi)
                    print("processing page %d, url:%s..."%(pi,url))
                    dom = _get_page_dom(url)
                    time.sleep(1)
                    print('data got...')

                    #check whether no result
                    if [x for x in dom("div.searchNoinfo")]:
                        print('no data for page %d, continue to next %s level....'%(pi,self.JOB_CODE))
                        break

                    cars=[]
                    for li in dom(self.SELECTOR).items('li'):
                        img_url=''
                        logo_url=''
                        description=''
                        name=''
                        for div in li(".imgBox"):
                            div = pq(div)
                            for img in div("img"):#get car img
                                if isinstance(img , HtmlElement):
                                    img_url = img.get("src","")
                                    break
                                else:
                                    pass
                            for _logo_div in div(".caricoBox"):#get car logo
                                for logo_img in pq(_logo_div)("img"):
                                    logo_url = logo_img.get("src","")
                                    break

                        for div in li(".searchListText"):#get car name
                            div = pq(div)
                            for p in div("p"):
                                p=pq(p)
                                for span in p("span"):
                                    span = pq(span)
                                    for link in span("a"):
                                        name = link.text
                                        break

                        cars.append([img_url, logo_url, description, name])

                    print("%d cars found!"%len(cars))
                    updated=0
                    for line in cars:
                        img_url, logo_url, description ,name=line
                        if not name:continue
                        try:
                            car_obj = Car.objects.get(logo_url=logo_url, name=name, img_path=img_url)
                            self.update_car(car_obj, i+1)#abstract method
                            car_obj.save()
                            updated+=1
                            if 0 and pi>1:
                                print('car %s updated to %s: %s'%(name, self.JOB_CODE, car_obj.price_level))
                        except Car.DoesNotExist,ex:
                            print('car %s not in db, page is %s'%(name, url))
                            with open('lost', 'a') as f:
                                f.write('car:%s   page:%s\r\n'%(name, url))
                            #print(traceback.format_exc())
                        except:
                            print(traceback.format_exc())
                    print("%d cars updated!"%updated)


                    #next page existing checking
                    for li in dom('.tc_page_list')('li'):
                        import pdb
                        #pdb.set_trace()
                        if pq(li).text().replace(' ','')==str(i+1):
                            hasNextPage=True
                            break
                        if hasNextPage:break
                    if not hasNextPage:
                        break

        except:
            print(traceback.format_exc())

class RefreshCarPriceJob_OLD(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 hours
    #URL="http://www.tuanche.com/che/"
    SELECTOR=".searchListC"
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'cars.cron.RefreshCarPriceJob_OLD'    # a unique code

    def do(self):
        """
        <div class="searchNoinfo">
            <p>
                <em></em>
                <span>未找到符合条件的车型，请修改已选条件！</span>
            </p>
        </div>
        ----or -----
        <div class="searchList">
            <ul class="searchListC">
               <li>
                        <div class="imgBox">
                            
                                <a href="http://sz.tuanche.com/c60/tuan/" target="_blank">
                            

                                <img src="http://pic.tuanche.com/car/20160321/1458531404258278_o.jpg" alt="">
                                
                                    <div class="searchMask"></div>
                                    <div class="searchMaskText">
                                        <p>车型概述</p>
                                        <p>1.外形改变意在展现时尚</p>
                                        <p>2.内部空间没变依旧宽敞</p>
                                        <p>3.取消顶配车型价格亲民</p>
                                    </div>
                                
                                <div class="caricoBox"><img src="http://pic.tuanche.com/car/20170222/14877499257433743_s.jpg" alt=""></div>
                            
                                </a>
                            
                        </div>
                        <div class="searchListText">
                            <p>
                                <span> <a href="http://sz.tuanche.com/c60/tuan/" target="_blank">雅阁</a></span>
                                <samp>累计报名<i>13991</i>人</samp>
                            </p>
                            
                                <a class="goin" href="http://sz.tuanche.com/c60/tuan/">团购报名 </a>
                            
                        </div>
               </li>
               <li></li>
               ...
            </ul>
        </div>
        """
        time.sleep(1)
        taget_list = ['http://www.tuanche.com/chep%d'%i for i in range(1,7)]
        taget_names = ['5万以下','5-10万','10-15万','15-20万','20-30万','30万以上']
        try:
            print("[%s] looking for cars price data...."%(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            for i in range(6):
                print("processing price:%s"%taget_names[i])
                #if i>0:break#for debug
                if not taget_list[i]:
                    continue
                url = taget_list[i]
                #get all sub serie(target DOM1)
                for pi in range(1,101):
                    #if pi>2:break#for debug
                    hasNextPage = False
                    if pi!=1:
                        url = taget_list[i] + 'n'+str(pi)
                    print("processing page %d, url:%s..."%(pi,url))
                    dom = _get_page_dom(url)
                    time.sleep(1)
                    print('data got...')

                    #check whether no result
                    if [x for x in dom("div.searchNoinfo")]:
                        print('no data for page %d, continue to next price level....'%pi)
                        break

                    cars=[]
                    for li in dom(self.SELECTOR).items('li'):
                        img_url=''
                        logo_url=''
                        description=''
                        name=''
                        for div in li(".imgBox"):
                            div = pq(div)
                            for img in div("img"):#get car img
                                if isinstance(img , HtmlElement):
                                    img_url = img.get("src","")
                                    break
                                else:
                                    pass
                            for _logo_div in div(".caricoBox"):#get car logo
                                for logo_img in pq(_logo_div)("img"):
                                    logo_url = logo_img.get("src","")
                                    break

                        for div in li(".searchListText"):#get car name
                            div = pq(div)
                            for p in div("p"):
                                p=pq(p)
                                for span in p("span"):
                                    span = pq(span)
                                    for link in span("a"):
                                        name = link.text
                                        break

                        cars.append([img_url, logo_url, description, name])

                    print("%d cars found!"%len(cars))
                    updated=0
                    for line in cars:
                        img_url, logo_url, description ,name=line
                        if not name:continue
                        try:
                            car_obj = Car.objects.get(logo_url=logo_url, name=name, img_path=img_url)
                            car_obj.price_level = {
                            1:'0,5',
                            2:'5,10',
                            3:'10,15',
                            4:'15,20',
                            5:'20,30',
                            6:'30,9999'}.get(i+1,'unknown')
                            car_obj.save()
                            updated+=1
                            if 0 and pi>1:
                                print('car %s updated to price: %s'%(name, car_obj.price_level))
                        except:
                            print('car %s not in db, page is %s'%(name, url))
                            with open('lost', 'a') as f:
                                f.write('car:%s   page:%s\r\n'%(name, url))
                            print(traceback.format_exc())
                    print("%d cars updated!"%updated)


                    #next page existing checking
                    for li in dom('.tc_page_list')('li'):
                        import pdb
                        #pdb.set_trace()
                        if pq(li).text().replace(' ','')==str(i+1):
                            hasNextPage=True
                            break
                        if hasNextPage:break
                    if not hasNextPage:
                        break

        except:
            print(traceback.format_exc())

class RefreshCarPriceJob(RefreshCarAttrJob):
    RUN_EVERY_MINS = 1 # every 2 hours
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'cars.cron.RefreshCarPriceJob'    # a unique code
    JOB_CODE='价位'
    target_list=['http://www.tuanche.com/chep%d'%i for i in range(1,7)]
    target_name_list=['5万以下','5-10万','10-15万','15-20万','20-30万','30万以上']

    def update_car(self, car_obj, list_index):
        """
        car_obj, instance of Car;
        lis_index, 1 ~ len(self.target_list)
        """
        car_obj.price_level = str(list_index-1)

class RefreshCarSizeJob(RefreshCarAttrJob):
    RUN_EVERY_MINS = 1 # every 2 hours
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'cars.cron.RefreshCarSizeJob'    # a unique code
    JOB_CODE='size'
    target_list=['http://www.tuanche.com/%s/'%_size for _size in ('chexinnengyuan','cheweixing','chexiaoxing','chejincou','chezhongji','chehaohua','chesuv','chempv','chepaoche')]
    target_name_list=['新能源汽车','微型车','小型车','紧凑型车','中级车','豪华车','suv','MPV','跑车']

    def update_car(self, car_obj, list_index):
        """
        car_obj, instance of Car;
        lis_index, 1 ~ len(self.target_list)
        """
        car_obj.size = str(list_index-1)

class RefreshCarGearboxJob(RefreshCarAttrJob):
    RUN_EVERY_MINS = 1 # every 2 hours
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'cars.cron.RefreshCarGearboxJob'    # a unique code
    JOB_CODE='变速箱'
    target_list=['http://www.tuanche.com/%s'%_size for _size in ('cheg7','cheg6','cheg1','cheg2','cheg4')]
    target_name_list=[ '手动',' 自动',' 无极变速',' 手自一体',' 双离合']

    def update_car(self, car_obj, list_index):
        """
        car_obj, instance of Car;
        lis_index, 1 ~ len(self.target_list)
        """
        car_obj.gearbox = str(list_index-1)

class RefreshCarDispatchJob(RefreshCarAttrJob):
    RUN_EVERY_MINS = 1 # every 2 hours
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'cars.cron.RefreshCarDispatchJob'    # a unique code
    JOB_CODE='排量(L)'
    target_list=['http://www.tuanche.com/%s'%_size for _size in ('chel1','chel2','chel3','chel4','chel5','chel6','chel7','chel8','chel9')]
    target_name_list=[ '<1.3','1.3','1.4','1.5','1.6','1.8','2.0','2.4','>2.4L']

    def update_car(self, car_obj, list_index):
        """
        car_obj, instance of Car;
        lis_index, 1 ~ len(self.target_list)
        """
        car_obj.displacement = str(list_index)

class RefreshCarOriginJob(RefreshCarAttrJob):
    RUN_EVERY_MINS = 1 # every 2 hours
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'cars.cron.RefreshCarOriginJob'    # a unique code
    JOB_CODE='国别'
    target_list=['http://www.tuanche.com/%s'%_size for _size in ('ches1','ches2','ches3','ches4','ches5','ches6','ches8','ches9')]
    target_name_list=[ '美系','德系','进口','日系','合资','国产','韩系','欧系']

    def update_car(self, car_obj, list_index):
        """
        car_obj, instance of Car;
        lis_index, 1 ~ len(self.target_list)
        """
        car_obj.origin = str(list_index-1)

class DownloadCarImgs(CronJobBase):
    RUN_EVERY_MINS = 1 # every 2 hours
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'cars.cron.DownloadCarImgs'    # a unique code

    def download_imgs(self, _img_list, name='thread1'):
        """
        _img_list: [(logo_url, img_url, car_obj),(....)...]
        download to the static file dir
        """
        def _ensure_dir(full_path):
            """
            确保路径存在，无则建立
            """
            p = full_path[:full_path.rfind('/')]
            with LOCK:
                if not os.path.exists(p):
                    makedirs(p)

        def _download_resource(url):
            """
            url: http://pic.tuanche.com/car/20160607/14652910143466292_o.jpg
            """
            full_path = os.path.join(STATIC_DIR, 'static')+urlparse(url).path
            _ensure_dir(full_path)
            req = urllib2.Request(url)
            req.add_header('Referer','http://www.tuanche.com/')
            req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0')
            resp = urllib2.urlopen(req)
            content = resp.read()
            with open(full_path, 'wb') as f:
                f.write(content)

        def _dispatch_download(_img_list,name):
            """
            http://pic.tuanche.com/car/20160607/14652910143466292_o.jpg
            """
            print('thread [%s] started! %d logo&imgs to download'%(name,len(_img_list)))
            i=0
            try:
                for logo,img,car_obj in _img_list:
                    try:
                        _download_resource(logo)
                        print('\tdownloaded logo from url:%s'%logo)
                        car_obj.logo_url = '/static'+urlparse(logo).path
                        _download_resource(img)
                        car_obj.img_path = '/static'+urlparse(img).path
                        print('\tdownloaded img from url:%s'%img)
                        car_obj.save()
                        i+=1
                    except:
                        print(traceback.format_exc())
                        #exit(0)
                        print('\tdownload failed!(logo:%s , img:%s'%(logo,img))
            except:
                print(traceback.format_exc())

            print('thread [%s] ended! %d img&logo downloaded!'%(name, i))

        _dispatch_download(_img_list,name)
        #th = thread.start_new_thread(_dispatch_download, (_img_list,name))

    def do(self):
        """
        download imgs(logo/car img) from location specified by Car.logo_url and Car.img_path
        """
        try:
            print("[%s] looking for cars whoes images not downloaded...."%(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            cars =  Car.objects.filter(logo_url__startswith='http://pic.tuanche.com')
            img_list=[(x.logo_url, x.img_path, x) for x in cars]
            count = len(img_list)
            if count:
                self.download_imgs(img_list[0:count/2])
                self.download_imgs(img_list[count/2:], 'thread2')
        except:
            print(traceback.format_exc())