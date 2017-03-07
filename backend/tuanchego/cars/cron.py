# -*- coding:utf-8 -*-
from django_cron import CronJobBase, Schedule
import urllib2
from pyquery import PyQuery as pq
from lxml.html import HtmlElement
from .models import Brand,Serie
import traceback
import datetime
import time

def _get_page_dom(url):
    req = urllib2.Request(url)
    req.add_header("Reffer","http://bzclk.baidu.com/adrc.php?t=06KL00c00fZ0gw60_wIm05-WcfahOeVm00000Ap-Gj300000Vs18-F.THLPkUrd1x60UWdBmy-bIfK15H9buj0YujKBnj0dnHfsuWc0IHYzwRP7n1c4nHf4fHckfRPAwW-KrDmLnHFDfYnzPWm4r0K95gTqFhdWpyfqnWbsPjRYPHDsriusThqbpyfqnHm0uHdCIZwsrBtEILILQMwdmy4WpAR8mvqV5vnqmhfsP7K7Hbn0mLFW5HmznjRd&tpl=tpl_10087_14396_1&l=1050977638&attach=location%3D%26linkName%3D%25E6%25A0%2587%25E9%25A2%2598%26linkText%3D%25E5%259B%25A2%25E8%25BD%25A6%25E7%25BD%2591-%25E4%25B8%25AD%25E5%259B%25BD%25E4%25B8%2593%25E4%25B8%259A%25E6%25B1%25BD%25E8%25BD%25A6%25E7%2594%25B5%25E5%2595%2586%25E5%25B9%25B3%25E5%258F%25B0%26xp%3Did(%2522m3ab65456%2522)%252FDIV%255B1%255D%252FDIV%255B1%255D%252FDIV%255B1%255D%252FH2%255B1%255D%252FA%255B1%255D%26linkType%3D%26checksum%3D95&ie=utf-8&f=8&tn=baidu&wd=%E5%9B%A2%E8%BD%A6&rqlang=cn&inputT=3713")
    req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0")
    resp = urllib2.urlopen(req)
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


class GetBrandSerieJob(CronJobBase):
    RUN_EVERY_MINS = 120 # every 2 hours
    #URL="http://www.tuanche.com/che/"
    SELECTOR=".searchListC"
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'cars.cron.GetBrandSerieJob'    # a unique code

    def do(self):
        """
        target DOM1:
            <div class="charactersSlidTwo">
                <div class="charactersSlidBox">  
                        <span>  <a class="styleName-in " href="/che31/">一汽奥迪</a></span>
                        <span>  <a class="styleName-in " href="/che193/">奥迪(进口)</a></span>
                        <span>  <a class="styleName-in " href="/che194/">奥迪RS</a></span>
                </div>
            </div>
        target DOM2:
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
        """
        try:
            print("[%s] looking for series data...."%(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            for brand in Brand.objects.all():
                time.sleep(1)
                print("processing brand:%s"%brand.name)
                if not brand.tc_url:
                    continue
                dom = _get_page_dom(brand.tc_url)
                print("data got!")

                #get all sub serie(target DOM1)
                sub_serie=[]
                import pdb
                pdb.set_trace()
                for div in dom(".charactersSlidTwo").items("div.charactersSlidBox"):
                    for span in pq(div)("span"):
                        for link in pq(span)("a.styleName-in"):
                            sub_serie.append({
                                    'href':link.get('href',''),
                                    'name':link.text
                                })

                #get all serie info by sub serie(target DOM2)
                for page in sub_serie:
                    uri,tag = page['href'],page['name']
                    if not uri:continue
                    time.sleep(1)
                    print('processing sub category: %s'%tag)
                    dom = _get_page_dom('http://www.tuanche.com'+uri)
                    print('data got!')
                    series = []
                    i=0
                    for li in dom(self.SELECTOR).items('li'):
                        img_url=''
                        description=''
                        name=''
                        for div in li(".imgBox"):
                            if i==0:
                                i=1
                                import pdb
                                #pdb.set_trace()
                            div = pq(div)
                            for img in div("img"):
                                if isinstance(img , HtmlElement):
                                    img_url = img.get("src","")
                                else:
                                    pass
                            for _div in div(".searchMaskText"):
                                description = _div.text

                        for div in li(".searchListText"):
                            div = pq(div)
                            for p in div("p"):
                                p=pq(p)
                                for span in p("span"):
                                    span = pq(span)
                                    for link in span("a"):
                                        name = link.text
                        series.append([img_url, description, name])


                    print("%d series found!"%len(series))
                    imported=0
                    for line in series:
                        img_url, description ,name=line
                        if not img_url:continue
                        try:
                            Serie.objects.get(brand=brand.id, name=name)
                        except:
                            imported+=1
                            Serie(brand=brand, name=name, img_url=img_url, tag=tag).save()
                    print("%d new series imported!"%imported)
        except:
            print(traceback.format_exc())