#-*- coding:utf-8 -*-
from urllib.request import urlopen
from urllib.request import Request
import chardet
from lxml import etree
from choiceUAIP import ChoiceUAIP
import socket


timeout = 60
socket.setdefaulttimeout(timeout)

class ProcessSymptom(object):
    """docstring for ClassName"""
    def __init__(self, symptoms_url,complication_url):
        #super(ClassName, self).__init__()
        self.symptoms_url = symptoms_url
        self.complication_url = complication_url
        
    def process_symptom(self):
        header={'User-Agent':ChoiceUAIP().choice_ua()}    
        request = Request(self.symptoms_url,headers=header)
        opener = ChoiceUAIP().choice_proxy()
        response = opener.open(request).read()
        if response is None:pass
        allcontent = response.decode('gb2312')
        #print(chardet.detect(response))
        #print(urlopen(Request(url,headers=header)).read().decode('gb2312'))
        selector=etree.HTML(allcontent) #将源码转化为能被XPath匹配的格式 
        #/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[2]/text()
        symptoms_url = self.symptoms_url
        common_symptoms = selector.xpath('//div[@class="content clearfix"]//dl[@class="links"]/dd//text()')
        common_symptoms = '++'.join(common_symptoms)
        common_symptoms_str = ' '.join(common_symptoms.split()).replace('++','').split('相关症状：')
        print(common_symptoms_str)
        common_symptoms = common_symptoms_str[0]
        links_symptoms = common_symptoms_str[1]
        print(links_symptoms)

        symptoms = selector.xpath('//div[@class="content clearfix"]//div[@class="art-box"]/p//text()')
        symptoms = ' '.join(symptoms)
        print(str(symptoms))
        
        symptoms_updatetime = selector.xpath('//div[@class="content clearfix"]//dl[@class="intro"]/dd[@class="i3"]/span/text()')[0].replace('更新','')
        print(symptoms_updatetime)
        #//*[@id="s_browseCount"]
        browse_count = selector.xpath('//dd[@class="i3"]/span[2]/span/text()')[0]
        print(browse_count)
        #//*[@id="s_collectCount"] /html/body/section/div[3]/div[1]/div[1]/dl[1]/dd[2]/span[3]/text()
        collect_count = selector.xpath('//dd[@class="i3"]/span[3]/span/text()')[0]
        print(collect_count)
        
        keys_list = ['symptoms_url','common_symptoms','links_symptoms','symptoms','symptoms_updatetime','browse_count','collect_count']
        vals_list = [symptoms_url,common_symptoms,links_symptoms,symptoms,symptoms_updatetime,browse_count,collect_count]   
        check_dict = dict(zip(keys_list,vals_list))
        print(check_dict)
        return check_dict
 
    def process_complication(self):
        header={'User-Agent':ChoiceUAIP().choice_ua()}    
        request = Request(self.complication_url,headers=header)
        opener = ChoiceUAIP().choice_proxy()
        response = opener.open(request).read()
        if response is None:pass
        allcontent = response.decode('gb2312')
        #print(chardet.detect(response))
        #print(urlopen(Request(url,headers=header)).read().decode('gb2312'))
        selector=etree.HTML(allcontent) #将源码转化为能被XPath匹配的格式 
        #/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[2]/text()
        complication_url = self.complication_url
        common_complication = selector.xpath('//div[@class="content clearfix"]//dl[@class="links"]/dd//text()')
        #common_complication = ' '.join(common_complication)
        #print(common_complication)
        common_complication = '++'.join(common_complication)
        common_complication = ' '.join(common_complication.split()).replace('++','')
        print(common_complication)

        complication = selector.xpath('//div[@class="content clearfix"]//div[@class="art-box"]/p//text()')
        complication = ' '.join(complication)
        print(str(complication))
        
        complication_updatetime = selector.xpath('//div[@class="content clearfix"]//dl[@class="intro"]/dd[@class="i3"]/span/text()')[0].replace('更新','')
        print(complication_updatetime)
        #//*[@id="s_browseCount"]
        browse_count = selector.xpath('//dd[@class="i3"]/span[2]/span/text()')[0]
        print(browse_count)
        #//*[@id="s_collectCount"] /html/body/section/div[3]/div[1]/div[1]/dl[1]/dd[2]/span[3]/text()
        collect_count = selector.xpath('//dd[@class="i3"]/span[3]/span/text()')[0]
        print(collect_count)
        
        keys_list = ['complication_url','common_complication','complication','complication_updatetime','browse_count','collect_count']
        vals_list = [complication_url,common_complication,complication,complication_updatetime,browse_count,collect_count]   
        check_dict = dict(zip(keys_list,vals_list))
        print(check_dict)
        return check_dict       

def main():
    symptoms_url = 'http://jbk.39.net/gxy/zztz/'
    complication_url = 'http://jbk.39.net/gxy/bfbz/'
    ps = ProcessSymptom(symptoms_url,complication_url)
    ps.process_symptom()
    ps.process_complication()

if __name__ == '__main__':
    main()
