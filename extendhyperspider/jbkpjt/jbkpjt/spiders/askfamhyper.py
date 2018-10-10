# -*- coding: utf-8 -*-
import scrapy
from jbkpjt.items import JbkpjtItem
from .processAskFamPagenum import ProcessAskFamPagenum
import time

class AskfamhyperSpider(scrapy.Spider):
    name = 'askfamhyper'
    allowed_domains = ['ask.familydoctor.com.cn/jbk/d369']
    #start_urls = ['http://ask.familydoctor.com.cn/jbk/d369/']
    url_set = set()
    #pafp = ProcessAskFamPagenum(start_urls)
    #page_num = pafp.get_pages()
    page_num = 1861
    #page_num = 60
    print('page_num:{}'.format(page_num))
    
    start_urls = []   
    #depart_list = ['neike','waike'] 
    for i in range(page_num):
        #http://ask.familydoctor.com.cn/jbk/d369?page=10&
        start_urls.append('http://ask.familydoctor.com.cn/jbk/d369?page={0}&'.format(str(i)))
    

    def parse(self,response):
        for i in range(1,58):
            #/html/body/div[5]/div/div[1]/div[2]/div/div[2]/dl[1]/dd/p/a

            xpaths = '//div[@class="cont faq-list"]/dl['+str(i)+']/dd/p/a/@href'
            print(xpaths)
            urls = response.xpath(xpaths).extract()

            print('<...........................')
            print('processing urls:{0}'.format(urls))
            
            urls = urls
            for url in urls:
                print('processing old url:{0}'.format(url))
                #url = url + 'jbzs/'
                #print('processing new url:{0}'.format(url))
                if url in AskfamhyperSpider.url_set:
                    pass
                else:
                    AskfamhyperSpider.url_set.add(url)
                    #content_url = 'http://bbs.tianya.cn'+url
                    yield scrapy.Request(url=url,callback=self.parse_content,dont_filter=True)

    def parse_content(self, response):
    
        print(AskfamhyperSpider.start_urls)
        print(len(AskfamhyperSpider.start_urls))
        subSelector = response.xpath('//div[@class="layout ask-detail"]')
        print('.........................')
        print(subSelector)
        
        items = []
        for sub in subSelector:
            print('sub:{}'.format(sub))
            item = JbkpjtItem()
            url = response.url
            item['disease_name'] = "高血压"

            '''
            q_data = ""
            for q_data_temp in sub.xpath('//div[@class="cont"]/div[@class="illness-pics"]/p/text()').extract()[0].strip().replace(' ',',').split('\r\n'):
                q_data = q_data + q_data_temp
            '''
            q_data = ""
            for q_data_temp in sub.xpath('//div[@class="cont"]/div[@class="illness-pics"]/p//text()').extract()[0].strip().replace(' ',',').split('\r\n'):
                q_data += q_data_temp.strip()
            #/html/body/div[6]/div/div[1]/div[2]/ul/li[1]/div[2]/dl/dd/p/text()
            a_data = ""
            for a_data_temp in sub.xpath('//div[@class="main-sec"]//dl[@class="answer-info-cont"]//p[@class="answer-words"]//text()').extract()[0].strip().split('\n'):
                a_data += a_data_temp.strip()
            '''
            a_data = ""
            for a_data_temp in sub.xpath('//div[@class="main-sec"]//dl[@class="answer-info-cont"]//p[@class="answer-words"]/text()').extract()[0].strip().split('\n'):
                a_data = a_data + a_data_temp
            
            '''
            qadatas = '{0}\n{1}'.format(q_data,a_data)
            qadata = '{0}\n{1}\n{2}'.format(q_data,a_data,url)
            #print(qa)
            qa = {
               "question":q_data,
               "answer":a_data,
               "qa_url":url
            }
            
            def write_txt_data(filename,data):
                with open(filename, "a") as f:
                    #data = f.write(str(data))
                    data = f.write(str(data)+'\n')
            write_txt_data('question.txt',q_data)
            write_txt_data('answer.txt',a_data)
            write_txt_data('qadatas.txt',qadatas)
            write_txt_data('qadata.txt',qadata)
            item['qa_corpus'] = qa
            currenttime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
            item['create_time'] = currenttime
            item['update_time'] = currenttime
            item['source'] = 'ask.familydoctor.com.cn'
            items.append(item)
        return items      
