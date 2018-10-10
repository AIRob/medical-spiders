from urllib.request import urlopen
from urllib.request import Request
from urllib import parse
import chardet
from lxml import etree
import time
from choiceUAIP import ChoiceUAIP


class ProcessAskFamPagenum(object):
    def __init__(self,url_start_page):
        self.url_start_page = url_start_page[0]
   
    def get_pages(self):
        #//*[@id="anpSelectData_Settings"]/a[13]
        #http://ask.familydoctor.com.cn/jbk/d369?page=0&
        url_page = self.url_start_page + '?page=0&'
        header={'User-Agent':ChoiceUAIP().choice_ua()}    
        request = Request(url_page,headers=header)
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
        page_str = selector.xpath('//*[@id="anpSelectData_Settings"]/a[13]/@href')[0]
        page_num = page_str.replace('&','').split('=')[1]
        return page_num

