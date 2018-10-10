# -*- coding: utf-8 -*-
import scrapy
import hashlib
import time
from choiceUAIP import ChoiceUAIP
from urllib.request import urlopen
from urllib.request import Request
from urllib import parse
import chardet
from lxml import etree


class ProcessPages(object):
    def __init__(self):
        pass

    def process_page(self,keshi_name):
        #http://ypk.39.net/search/{0}-p{1}/
        all_page_url = 'http://jbk.39.net/bw/{0}_p0#ps'.format(keshi_name)
        #all_page_url = "http://ypk.39.net/search/all?k=".format(parse.quote(disease))
        header={'User-Agent':ChoiceUAIP().choice_ua()}       
        request = Request(all_page_url,headers=header)
        opener = ChoiceUAIP().choice_proxy()
        response = opener.open(request).read()
        if response is None:pass
        allcontent = response.decode('gb2312','ignore')
        selector=etree.HTML(allcontent) #将源码转化为能被XPath匹配的格式 
        print(selector)
        urlpage = selector.xpath('//*[@id="res_tab_1"]/div[@class="site-pages"]/a[@class="sp-a"]/@href')[1]
        #if urlpage is None:pass
        print('pages:{}'.format(urlpage))
        all_pages = urlpage.replace('#ps','').split('p')[-1]
        return int(all_pages)+1

if __name__ == '__main__':
    tx = ProcessPages()
    print('bbb')
    depart_list = ['neike','waike','erke','fuchanke','nanke','wuguanke',\
                   'pifuxingbing','shengzhijiankang','zhongxiyijieheke',\
                   'ganbing','jingshenxinlike','zhongliuke','chuanranke',\
                   'laonianke','tijianbaojianke','chengyinyixueke',\
                   'jizhenke','yingyangke'] 
    for i in range(len(depart_list)):
    	print(tx.process_page(str(depart_list[i])))