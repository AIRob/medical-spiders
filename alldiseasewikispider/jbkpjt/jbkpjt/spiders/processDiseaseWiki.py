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

class ProcessDiseaseWiki(object):
    """docstring for ClassName"""
    
    def __init__(self, url):
        #super(ClassName, self).__init__()
        self.url = url
        
    def process_disease_wiki(self,disease):
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
        disease_wiki_all_infos = selector.xpath('//*[@id="content"]//text()')
        #print(drugs_info)
        disease_wiki_data = ' '.join(disease_wiki_all_infos)        
        return disease_wiki_data

def process_disease_wiki_main(disease):
    #disease = '抑郁症'    
    #http://www.baike.com/wiki/%E9%AB%98%E8%A1%80%E5%8E%8B
    #disease = '高血压'
    url='http://www.baike.com/wiki/{}'.format(parse.quote(disease))
    print(url)
    pdw = ProcessDiseaseWiki(url)
    disease_how_prevent = pdw.process_disease_wiki(disease)
    print(disease_how_prevent)
    write_txt_data('disease_wiki.txt',disease_how_prevent)
    return disease_how_prevent  

def write_txt_data(filename,data):
    with open(filename, "a",encoding='utf-8') as f:
        data = f.write(str(data)+'\n')

if __name__ == '__main__':
    disease = '高血压'
    process_disease_wiki_main(disease)
