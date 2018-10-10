#-*- coding:utf-8 -*-
from urllib.request import urlopen
from urllib.request import Request
from urllib import parse
import chardet
from lxml import etree
import time
from choiceUAIP import ChoiceUAIP


class ProcessDiseaseHowPrevent(object):
    """docstring for ClassName"""
    
    def __init__(self, url):
        #super(ClassName, self).__init__()
        self.url = url
        
    def process_disease_how_prevent(self,disease):
        header={'User-Agent':ChoiceUAIP().choice_ua()}    
        request = Request(self.url,headers=header)
        opener = ChoiceUAIP().choice_proxy()
        response = opener.open(request).read()
        print(chardet.detect(response))     
        allcontent = response.decode('utf-8','ignore')
        #print(allcontent)
        if allcontent is None:pass
        selector=etree.HTML(allcontent) #将源码转化为能被XPath匹配的格式
        #//*[@id="content"]/p[4]
        #//*[@id="content"]/p[7]
        #//*[@id="content"]/p[4]
        disease_how_prevent_all_infos = selector.xpath('//*[@id="content"]//text()')
        #print(drugs_info)
        disease_how_prevent_all_info = ' '.join(disease_how_prevent_all_infos)
        #disease_all_info = '++'.join(disease_all_info)
        #disease_all_info = ' '.join(disease_all_info.split()).replace('++','')
        #print(disease_all_info)
        try:           
            first_split_str = "预防措施 /{}  编辑".format(disease)
            disease_how_prevent_first = disease_how_prevent_all_info.split(first_split_str)[1]
            print(len(disease_how_prevent_first))
            #print(disease_cause_first)
            sec_split_str = "常见误区 /{}  编辑".format(disease)
            disease_how_prevent = disease_how_prevent_first.split(sec_split_str)[0]
        except:
            disease_how_prevent = "null"
        return disease_how_prevent

 
def process_disease_how_prevent_main(disease):
    #disease = '抑郁症'    
    #http://www.baike.com/wiki/%E9%AB%98%E8%A1%80%E5%8E%8B
    #disease = '高血压'
    url='http://www.baike.com/wiki/{}'.format(parse.quote(disease))
    print(url)
    pdhp = ProcessDiseaseHowPrevent(url)
    disease_how_prevent = pdhp.process_disease_how_prevent(disease)
    print(disease_how_prevent)
    return disease_how_prevent  

if __name__ == '__main__':
    disease = '高血压'
    process_disease_how_prevent_main(disease)
