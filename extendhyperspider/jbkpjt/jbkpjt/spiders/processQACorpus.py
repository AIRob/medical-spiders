#-*- coding:utf-8 -*-
from urllib.request import urlopen
from urllib.request import Request
from urllib import parse
import chardet
from lxml import etree
import time
from choiceUAIP import ChoiceUAIP


class ProcessQACorpus(object):
    """docstring for ClassName"""
    
    def __init__(self, url):
        #super(ClassName, self).__init__()
        self.url = url  
           
    def process_qa_corpus_detail(self):
        #druginfo_url = durgurl+'manual'
        header={'User-Agent':ChoiceUAIP().choice_ua()}    
        request = Request(self.url,headers=header)
        opener = ChoiceUAIP().choice_proxy()
        response = opener.open(request).read()            
        
        if response is None:pass
        allcontent = response.decode('gb2312','ignore')
        if allcontent is None:pass
        selector=etree.HTML(allcontent) #将源码转化为能被XPath匹配的格式
        #/html/body/section/div[3]/div[1]/div/div[1]/h4

        #/html/body/section/div[3]/div[1]/div/div[1]/h4
        qa_corpus = selector.xpath('//div[@class="content clearfix"]//div[@class="chi-exp-item "]//text()')
        #print(qa_corpus)
        qa_corpus = '++'.join(qa_corpus)
        #print(''.join(strs.split()).replace('++',''))
        qa_corpus = ' '.join(qa_corpus.split()).replace('++','')
        #print(qa_corpus)
        #question1 = selector.xpath('//div[@class="content clearfix"]//div[@class="chi-exp-item "]/h4/text()')
        #print(question1)
        return qa_corpus

def process_qa_corpus_main(disease_zh):
    #http://ypk.39.net/search/%E6%8A%91%E9%83%81%E7%97%87-p2/
    #disease = '抑郁症'    
    #http://ypk.39.net/search/%E9%AB%98%E8%A1%80%E5%8E%8B-p134/
    #disease = '高血压'

    drug_qa_corpus_list = []
    for i in range(7):
        print('processing ...... page {}'.format(i))
        url='http://jbk.39.net/{0}/zjzx_p{1}/'.format(disease_zh,i)
        print(url)
        pqac = ProcessQACorpus(url)
        qa_corpus = pqac.process_qa_corpus_detail()
        drug_qa_corpus_list.append(qa_corpus)
    print(drug_qa_corpus_list)
    return drug_qa_corpus_list        


if __name__ == '__main__':
    #disease = '高血压'
    disease_zh = 'gxy'
    process_qa_corpus_main(disease_zh)
