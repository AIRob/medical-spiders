#-*- coding:utf-8 -*-
from urllib.request import urlopen
from urllib.request import Request
from urllib import parse
import chardet
from lxml import etree
import time
from choiceUAIP import ChoiceUAIP
import socket


timeout = 60
socket.setdefaulttimeout(timeout)

class ProcessDiseaseCause(object):
    """docstring for ClassName"""
    
    def __init__(self, url):
        #super(ClassName, self).__init__()
        self.url = url
        
    def process_disease_cause(self,disease):
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
        disease_all_infos = selector.xpath('//*[@id="content"]//text()')
        print(disease_all_infos)
        disease_all_info = ' '.join(disease_all_infos)
        #disease_all_info = '++'.join(disease_all_info)
        #disease_all_info = ' '.join(disease_all_info.split()).replace('++','')
        #print(disease_all_info)
        '''
        try:
            first_split_str = "病因详情 /{}  编辑".format(disease)
            disease_cause_first = disease_all_info.split(first_split_str)[1]
            #print(len(disease_cause_first))
            #print(disease_cause_first)
            sec_split_str = "症状 /{}  编辑".format(disease)
            disease_cause = disease_cause_first.split(sec_split_str)[0]

        except:
            first_split_str = "主要病因 /{}  编辑".format(disease)
            disease_cause_first = disease_all_info.split(first_split_str)[1]
            #print(len(disease_cause_first))
            #print(disease_cause_first)
            sec_split_str = "主要症状 /{}  编辑".format(disease)
            disease_cause = disease_cause_first.split(sec_split_str)[0] 

        else:
            print('ok')
        finally:
            disease_cause = 'null'
        '''
        try:
            first_split_str = "病因详情 /{}  编辑".format(disease)
            disease_cause_first = disease_all_info.split(first_split_str)[1]
            #print(len(disease_cause_first))
            #print(disease_cause_first)
            sec_split_str = "症状 /{}  编辑".format(disease)
            disease_cause = disease_cause_first.split(sec_split_str)[0]

        except:
            disease_cause = 'null'        
        #print(disease_cause)
        return disease_cause


 
def process_diseasecause_main(disease):
    #disease = '抑郁症'    
    #http://www.baike.com/wiki/%E9%AB%98%E8%A1%80%E5%8E%8B
    #disease = '高血压'
    url='http://www.baike.com/wiki/{}'.format(parse.quote(disease))
    print(url)
    ps = ProcessDiseaseCause(url)
    disease_cause = ps.process_disease_cause(disease)
    print(disease_cause)
    return disease_cause  


if __name__ == '__main__':
    disease = '高血压'
    process_diseasecause_main(disease)
