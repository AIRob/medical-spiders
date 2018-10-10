# -*- coding: utf-8 -*-
import scrapy
from jbkpjt.items import JbkpjtItem
import hashlib
from .processSymptom import ProcessSymptom
from .processDiseaseCheckDetail import ProcessDiseaseCheckDetail
from .processDiseaseCause import process_diseasecause_main
from .processDiseaseHowPrevent import process_disease_how_prevent_main
from .processDrugInfo import process_drug_main
from .processQACorpus import process_qa_corpus_main
import time
from .choiceUAIP import ChoiceUAIP
from .processPages import ProcessPages
from .processDiseaseWiki import process_disease_wiki_main


class JbkhyperSpider(scrapy.Spider):
    name = 'jbkallwiki'
    #http://jbk.39.net/gxb/
    allowed_domains = ["http://jbk.39.net/"]    
    url_set = set()
    
    start_urls = []
    #http://jbk.39.net/bw/waike_p9#ps
    #http://jbk.39.net/bw/yingyangke_p7#ps
    
    depart_list = ['neike','waike','erke','fuchanke','nanke','wuguanke',\
                   'pifuxingbing','shengzhijiankang','zhongxiyijieheke',\
                   'ganbing','jingshenxinlike','zhongliuke','chuanranke',\
                   'laonianke','tijianbaojianke','chengyinyixueke',\
                   'jizhenke','yingyangke'] 
    '''
    depart_list = ['waike','erke','fuchanke','nanke','wuguanke',\
                   'pifuxingbing','shengzhijiankang','zhongxiyijieheke',\
                   'ganbing','jingshenxinlike','zhongliuke','chuanranke',\
                   'laonianke','tijianbaojianke','chengyinyixueke',\
                   'jizhenke','yingyangke'] 
    '''
    #depart_list = ['neike','waike'] 
    for i in range(len(depart_list)):
        pps = ProcessPages()
        keshi_pages = pps.process_page(str(depart_list[i]))
        #keshi_pages = keshi_pages if keshi_pages < 10 else 10
        for j in range(int(keshi_pages)):
            start_urls.append('http://jbk.39.net/bw/{0}_p{1}#ps'.format(str(depart_list[i]),str(j)))

    def process_url_page(self,keshi_name):
        #http://ypk.39.net/search/{0}-p{1}/
        all_page_url = 'http://jbk.39.net/bw/{0}_p0#ps'.format(str(depart_list[i]))
        #all_page_url = "http://ypk.39.net/search/all?k=".format(parse.quote(disease))
        header={'User-Agent':ChoiceUAIP().choice_ua()}       
        request = Request(all_page_url,headers=header)
        opener = ChoiceUAIP().choice_proxy()
        response = opener.open(request).read()
        if response is None:pass
        allcontent = response.decode('gb2312','ignore')
        selector=etree.HTML(allcontent) #将源码转化为能被XPath匹配的格式 
        #//*[@id="res_tab_1"]/div[11]/a[11] 
        #//*[@id="res_tab_1"]/div[11]/a[11]
        urlpage = selector.xpath('//*[@id="res_tab_1"]/div[@class="site-pages"]/a[@class="sp-a"]/@href')[0]
        #pgleft
        #/html/body/div[8]/div[2]/div[4]/i
        #/html/body/div[8]/div[2]/span/span[1]/b
        #urlpage = selector.xpath('//div[@class="page"]//span[@class="pgleft"]/b/text()')
        print('pages:{}'.format(urlpage))
        if urlpage is None:pass
        return int(int(urlpage)/15+2)
    
    def parse(self,response):
        for i in range(1,11):
            #//*[@id="res_tab_1"]/div[1]/dl/dt/h3/a
            xpaths = '//*[@id="res_tab_1"]/div['+str(i)+']/dl/dt/h3/a/@href'
            print(xpaths)
            urls = response.xpath(xpaths).extract()

            print('<...........................')
            print('processing urls:{0}'.format(urls))

            urls = urls
            for url in urls:
                print('processing old url:{0}'.format(url))
                url = url + 'jbzs/'
                print('processing new url:{0}'.format(url))
                if url in JbkhyperSpider.url_set:
                    pass
                else:
                    JbkhyperSpider.url_set.add(url)
                    #content_url = 'http://bbs.tianya.cn'+url
                    yield scrapy.Request(url=url,callback=self.parse_content,dont_filter=True)
    

    def parse_content(self, response):
        print(JbkhyperSpider.start_urls)
        subSelector = response.xpath('//div[@class="content clearfix"]')
        print('.........................')
        print(subSelector)
        items = []
        for sub in subSelector:
            print('sub:{}'.format(sub))
            item = JbkpjtItem()
            url = response.url

            print(url)
            if url is None:pass         
            disease_name = sub.xpath('//dl[@class="intro"]/dt/text()').extract()[0].replace('简介','')
            hash = hashlib.md5()
            hash.update(str(disease_name).encode('utf-8'))
            #print(hash.hexdigest())
            md5file = hash.hexdigest()
            #0、疾病
            item['disease_id'] = md5file
            #item['disease_name'] = disease_name[0].split('简介')[0] #疾病名
            item['disease_name'] = disease_name
            print('慢病名称:{}'.format(disease_name))
            #print('慢病名称:{}'.format(disease_name)[0].replace('简介',''))
            #1、疾病简介
            '''
            disease_profile = sub.xpath('//dl[@class="intro"]/dd/text()').extract()
            item['disease_profile'] = disease_profile #疾病简介
            #2、#慢病基本知识{}
            disease_alias = sub.xpath('//dl[@class="info"]/dd[2]/text()').extract()[0]
            print('慢病别名:{}'.format(disease_alias))
            #/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[1]/a
            is_medical = sub.xpath('//dl[@class="info"]/dd[1]/a/text()').extract()[0]
            print('是否属于医保:{}'.format(is_medical))
            #/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[3]/a[1]
            #/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[3]/a[1]
            incidence_site = ''
            for incidence_site_temp in sub.xpath('//dl[@class="info"]/dd[3]/a/text()').extract():
                incidence_site = incidence_site + incidence_site_temp + ','
            print('发病部位:{}'.format(str(incidence_site)))
            contagious = sub.xpath('//dl[@class="info"]/dd[4]/text()').extract()[0]
            print('传染性:{}'.format(contagious))
            multiple_people = sub.xpath('//dl[@class="info"]/dd[5]/text()').extract()[0]
            print('多发人群:{}'.format(multiple_people))
            #/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[6]/a[1]

            typical_symptoms = ''
            for typical_symptoms_temp in sub.xpath('//dl[@class="info"][1]/dd[6]/a/text()').extract():
                typical_symptoms = typical_symptoms + typical_symptoms_temp + ','
            print('典型症状:{}'.format(typical_symptoms))

            complication = ''
            for complication_temp in sub.xpath('//dl[@class="info"][1]/dd[7]/a/text()').extract():
                complication = complication + complication_temp + ','
            print('并发症:{}'.format(complication))

            item['disease_base'] = {
                'disease_alias':disease_alias,      #别名
                'is_medical':is_medical,            #是否属于医保
                'incidence_site':incidence_site,    #发病部位
                'contagious':contagious,            #传染性
                'multiple_people':multiple_people,  #多发人群
                'typical_symptoms':typical_symptoms,#典型症状
                'complication':complication         #并发症
            } #慢病基本知识
            #3、疾病诊断
            #/html/body/section/div[3]/div[1]/div[1]/dl[4]/dd[1]/text()
            best_time = sub.xpath('//dl[@class="info"][3]/dd[1]/text()').extract()[1]
            duration_visit = sub.xpath('//dl[@class="info"][3]/dd[2]/text()').extract()[1]
            followup_freq = sub.xpath('//dl[@class="info"][3]/dd[3]/text()').extract()[1]
            pre_treat = sub.xpath('//dl[@class="info"][3]/dd[4]/text()').extract()[1]
            print('最佳就诊时间:{}'.format(best_time))
            print('就诊时长:{}'.format(duration_visit))
            print('复诊频率:{}'.format(followup_freq))
            print('就诊前准备:{}'.format(pre_treat))
            item['disease_diagnosis'] = {
                'best_time':best_time,
                'duration_visit':duration_visit,
                'followup_freq':followup_freq,
                'pre_treat':pre_treat
            }           
            #4、疾病检查
            disease_check_dict = 'null'
            check_url = sub.xpath('//dl[@class="info"][2]/dd[6]/a[@class="more"]/@href').extract()[0]
            pdsd = ProcessDiseaseCheckDetail(check_url)
            disease_check_dict = pdsd.process_disease_check_detail()
            item['disease_check'] = disease_check_dict
            print('疾病检查:{}'.format(disease_check_dict))            
            #5、疾病症状
            disease_symptoms = 'null'
            complication = 'null'

            try:
                symptoms_url = sub.xpath('//dl[@class="info"][1]/dd[6]/a[@class="more"]/@href').extract()[0]
                complication_url = sub.xpath('//dl[@class="info"][1]/dd[7]/a[@class="more"]/@href').extract()[0]
                print('symptoms_url:{}'.format(symptoms_url))
                print('complication_url:{}'.format(complication_url))
                ps = ProcessSymptom(symptoms_url,complication_url)
                disease_symptoms = ps.process_symptom()
                complication = ps.process_complication()
            except Exception as e:
                pass
            item['disease_symptoms'] = {
                'detail_symptom':disease_symptoms, #详细
                'complication':complication        #详细
            }
            
            #6、疾病病因
            #爬百科失败
            #爬wiki百科ok
            disease_cause = 'null'
            disease_cause = process_diseasecause_main(disease_name)
            item['disease_cause'] = disease_cause

            #7、疾病治疗
            visit_department = ''
            for visit_department_temp in sub.xpath('//dl[@class="info"][2]/dd[1]/a/text()').extract():
                visit_department = visit_department + visit_department_temp + ','
            #item['visit_department'] = visit_department
            print('就诊科室:{}'.format(visit_department))
            treat_method = ''
            for treat_method_temp in sub.xpath('//dl[@class="info"][2]/dd[5]/a/text()').extract():
                treat_method = treat_method + treat_method_temp + ','
            #item['treat_method'] = treat_method
            print('治疗方法:{}'.format(treat_method))

            treat_costs = sub.xpath('//dl[@class="info"][2]/dd[2]/text()').extract()[0]
            cure_rate = sub.xpath('//dl[@class="info"][2]/dd[3]/text()').extract()[0]
            treat_cycle = sub.xpath('//dl[@class="info"][2]/dd[4]/text()').extract()[0]
            print('治疗费用:{}'.format(treat_costs))
            print('治愈率:{}'.format(cure_rate))
            print('治疗周期:{}'.format(treat_cycle))

            common_drugs = ''
            for common_drugs_temp in sub.xpath('//dl[@class="info"][2]/dd[7]/a/text()').extract():
                common_drugs = common_drugs + common_drugs_temp + ','
            #item['common_drugs'] = common_drugs
            print('常用药品:{}'.format(common_drugs))

            item['disease_treat'] = {
                'treat_method':treat_method,
                'treat_costs':treat_costs,
                'cure_rate':cure_rate,
                'treat_cycle':treat_cycle,
                'common_drugs':common_drugs,
                'visit_department':visit_department
            }

            #8、药品
            #drugs_dict_list = process_drug_main(disease_name)
            #item['drugs'] = drugs_dict_list

            #9、如何预防
            how_prevent = 'null'
            how_prevent = process_disease_how_prevent_main(disease_name)
            item['how_prevent'] = how_prevent

            #10、问答预料
            qa_corpus = 'null'
            disease_zh = url.replace('/jbzs/','').split('/')[-1]
            print('disease_zh:{}'.format(disease_zh))
            qa_corpus = process_qa_corpus_main(disease_zh)
            item['qa_corpus'] = qa_corpus
            

            currenttime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
            item['create_time'] = currenttime
            item['update_time'] = currenttime
            item['source'] = 'jbk.39.net'
            '''
            #11、添加的wiki
            disease_wiki = process_disease_wiki_main(disease_name)
            item['wiki'] = disease_wiki
            items.append(item)
            time.sleep(3)
        return items

    
