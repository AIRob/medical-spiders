#-*- coding:utf-8 -*-
from urllib.request import urlopen
from urllib.request import Request
import chardet
from lxml import etree
from choiceUAIP import ChoiceUAIP
import socket

timeout = 60
socket.setdefaulttimeout(timeout)

class ProcessDiseaseCheckDetail(object):
    """docstring for ClassName"""
    def __init__(self, url):
        #super(ClassName, self).__init__()
        self.url = url
        
    def process_disease_check_detail(self):
        header={'User-Agent':ChoiceUAIP().choice_ua()}    
        request = Request(self.url,headers=header)
        opener = ChoiceUAIP().choice_proxy()
        response = opener.open(request).read()
        if response is None:pass
        allcontent = response.decode('gb2312')
        #print(chardet.detect(response))
        #print(urlopen(Request(url,headers=header)).read().decode('gb2312'))
        selector=etree.HTML(allcontent) #将源码转化为能被XPath匹配的格式 
        #/html/body/section/div[3]/div[1]/div[1]/div[2]
        check_url = self.url
        common_check = selector.xpath('//div[@class="content clearfix"]//div[@class="chi-know chi-int"]/div[@class="checkbox"]/div//text()')
        #print(str(common_check).replace(' ',''))
        common_check = '++'.join(common_check)
        common_check = ' '.join(common_check.split()).replace('++','')
        print(common_check)
        checks = selector.xpath('//div[@class="content clearfix"]//div[@class="chi-know chi-int"]/div[@class="art-box"]/p//text()')
        checks = ' '.join(checks)
        print(str(checks))
        check_updatetime = selector.xpath('//div[@class="content clearfix"]//div[@class="chi-know chi-int"]/dl[@class="intro"]/dd[@class="i3"]/span/text()')[0].replace('更新','')
        print(check_updatetime)
        #//*[@id="s_browseCount"]
        browse_count = selector.xpath('//dd[@class="i3"]/span[2]/span/text()')[0]
        print(browse_count)
        #//*[@id="s_collectCount"]
        collect_count = selector.xpath('//dd[@class="i3"]/span[3]/span/text()')[0]
        print(collect_count)
        keys_list = ['check_url','common_check','checks','check_updatetime','browse_count','collect_count']
        vals_list = [check_url,common_check,checks,check_updatetime,browse_count,collect_count]   
        check_dict = dict(zip(keys_list,vals_list))
        print(check_dict)
        return check_dict

def main():
    url = 'http://jbk.39.net/gxy/jcjb/'
    ps = ProcessDiseaseCheckDetail(url)
    ps.process_disease_check_detail()

if __name__ == '__main__':
    main()
