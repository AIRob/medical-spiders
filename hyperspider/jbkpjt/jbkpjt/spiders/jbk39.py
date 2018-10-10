# -*- coding: utf-8 -*-
import scrapy
from jbkpjt.items import JbkpjtItem
import hashlib
from .processSymptom import ProcessSymptom
from .processDrugInfo import ProcessDrug
import time


class Jbk39Spider(scrapy.Spider):
    name = "jbk39"
    allowed_domains = ["http://jbk.39.net/bw"]
    #start_urls = ['http://jbk.39.net/dxy/']
    start_urls = []
    url_set = set()
    
    for i in range(2):
        start_urls.append('http://jbk.39.net/bw_p'+str(i)+'#ps')
        #start_urls.append('http://jbk.39.net/bw_p'+str(i))
        #http://jbk.39.net/bw/neike_p3#ps
        #start_urls.append('http://jbk.39.net/bw/neike_p'+str(i)+'#ps')
    

    def parse(self,response):
        for i in range(1,11):
            xpaths = '//*[@id="res_tab_1"]/div['+str(i)+']/dl/dt/h3/a/@href'
            print(xpaths)
            urls = response.xpath(xpaths).extract()
            print('<...........................')
            print('processing urls:{0}'.format(urls))

            
            for url in urls:
                if url in Jbk39Spider.url_set:
                    pass
                else:
                    Jbk39Spider.url_set.add(url)
                    #content_url = 'http://bbs.tianya.cn'+url
                    yield scrapy.Request(url=url,callback=self.parse_content,dont_filter=True)

            
    def parse_content(self, response):
            #url = response.xpath('//*[@id="post_head"]/div[2]/@js_pageurl').extract()
            

        print(Jbk39Spider.start_urls)
        subSelector = response.xpath('//div[@class="content clearfix"]')
        print('.........................')
        print(subSelector)
        items = []
        for sub in subSelector:
            print('sub:{}'.format(sub))
            item = JbkpjtItem()
            url = response.url
            print(url)
            hash = hashlib.md5()
            hash.update(str(url).encode('utf-8'))
            #print(hash.hexdigest())
            md5file = hash.hexdigest()
            item['_id'] = md5file
            #/html/body/section[1]/div[3]/div[1]/div/div[1]/div/dl/dt
            #/html/body/section[1]/div[3]/div[1]/div/div[1]/div/dl/dt
            manbingName = sub.xpath('//dl/dt/text()').extract()
            item['manbingName'] = manbingName
            #/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[1]/i
            #/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[1]
            # //div[@class="info"]/ul[@class="clearfix"]//text()
            item['otherName'] = sub.xpath('//div[@class="info"]//li[1]/text()').extract()[0]
            #/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[8]
            item['treatmentCycle'] = sub.xpath('//div[@class="info"]//li[8]//text()').extract()[1]
            '''
            temps = ''
            for temp in sub.xpath('./ul/li[2]//text()').extract():
                temps += temp
            '''
            #/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[11]/cite/a
            #/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[11]/cite/a
            
            symptomURL = sub.xpath('//div[@class="info"]//li[11]/cite/a/@href').extract()
            item['symptomURL'] = symptomURL
            #/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[10]/cite/a
            print('symptomURL:{}'.format(symptomURL))
            #/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[11]/i
            #/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[11]
            #/html/body/section[1]/div[3]/div[1]/div/div[2]/ul/li[11]/a[1]
            item['symptom'] = sub.xpath('//div[@class="info"]//li[11]/text()').extract()
            #//div[@class="info"]//li[11]//text()
            temps = ''
            for temp in sub.xpath('//div[@class="info"]/ul[@class="clearfix"]//text()').extract():
                temps += temp
            item['manbingAll'] = temps
            #/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[1]/text()
            #item['symptomEarly'] = scrapy.Request(url=str(symptomURL),callback=self.process_symptom,dont_filter=True)
            #symptomEarlyContent = self.process_symptom(str(symptomURL[0]))
            prosym = ProcessSymptom(symptomURL[0])
            item['symptomAll'] = prosym.process_symptom()
            drugURL = 'http://ypk.39.net/search/' +str(manbingName[0])
            print('drug URL:{}'.format(drugURL))
            time.sleep(3)
            manbingDict = main(manbingName[0])
            item['manbingDict'] = manbingDict

            items.append(item)
        return items
    '''
    def process_symptom(self,response):
        #/html/body/section/div[3]/div[1]/div[1]/dl[2]
        subSelector =  response.xpath('//div[@class="content clearfix"]')
        print('subSelector:{}'.format(subSelector))
        contents = ''
        for sub in subSelector:
            temps = ''
            for temp in sub.xpath('//dl[@class="links"]//text()').extract():
                temps += temp
            contents.append(temps)
        return contents
    '''