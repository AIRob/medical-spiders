# -*- coding: utf-8 -*-
import scrapy
from jbkpjt.items import JbkpjtItem
import hashlib
from .processSymptom import ProcessSymptom
from .processDrugInfo import ProcessDrug
from .processDiseaseCheckDetail import ProcessDiseaseCheckDetail
from .processDiseaseCause import process_diseasecause_main
from .processDiseaseHowPrevent import process_disease_how_prevent_main
from .processDrugInfo import process_drug_main
from .processQACorpus import process_qa_corpus_main
import time


class JbkhyperSpider(scrapy.Spider):
    name = 'jbkhyper'
    allowed_domains = ["http://jbk.39.net/gxy/"]
    start_urls = ['http://jbk.39.net/gxy/jbzs/']
    '''
    url_set = set()
    
    start_urls = [] 
    for i in range(2):
        start_urls.append('http://jbk.39.net/bw_p'+str(i)+'#ps')
    
    def parse(self,response):
        for i in range(1,11):
            xpaths = '//*[@id="res_tab_1"]/div['+str(i)+']/dl/dt/h3/a/@href'
            print(xpaths)
            urls = response.xpath(xpaths).extract()
            print('<...........................')
            print('processing urls:{0}'.format(urls))

            
            for url in urls:
                if url in JbkhyperSpider.url_set:
                    pass
                else:
                    JbkhyperSpider.url_set.add(url)
                    #content_url = 'http://bbs.tianya.cn'+url
                    yield scrapy.Request(url=url,callback=self.parse_content,dont_filter=True)
    '''

    def parse(self, response):
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
            disease_profile = sub.xpath('//dl[@class="intro"]/dd/text()').extract()[0]
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
            #/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[6]/a[6]
            symptoms_url = sub.xpath('//dl[@class="info"][1]/dd[6]/a[@class="more"]/@href').extract()[0]
            #/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[7]/a[6]
            #/html/body/section/div[3]/div[1]/div[1]/dl[3]/dd[6]/a[6]
            #/html/body/section/div[3]/div[1]/div[1]/dl[2]/dd[7]/a[6]
            complication_url = sub.xpath('//dl[@class="info"][1]/dd[7]/a[@class="more"]/@href').extract()[0]
            print('symptoms_url:{}'.format(symptoms_url))
            print('complication_url:{}'.format(complication_url))
            
            ps = ProcessSymptom(symptoms_url,complication_url)
            disease_symptoms = ps.process_symptom()
            complication = ps.process_complication()
            
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
            '''
            goods_common_name = 'null'
            goods_price = 'null'
            approval_rum = 'null'
            indication = 'null'
            functions = 'null'
            #is_import = 'null'
            manufacturer = 'null'
            ingredients = 'null'
            adverse_reactions = 'null'
            precautions = 'null'
            taboo = 'null'
            medicine_interactions = 'null'
            pharmacological_action = 'null'
            special_population = 'null'
            dosage = 'null'
            drug_form = 'null'
            drug_spec = 'null'
            
            drugs_dict = {
                'goods_common_name':goods_common_name,
                'goods_price':goods_price,
                'approval_rum':approval_rum,
                'indication':indication,
                'functions':functions,
                #'is_import':is_import,
                'manufacturer':manufacturer,
                'ingredients':ingredients,
                'adverse_reactions':adverse_reactions,
                'precautions':precautions,
                'taboo':taboo,
                'medicine_interactions':medicine_interactions,
                'pharmacological_action':pharmacological_action,
                'special_population':special_population,
                'dosage':dosage,
                'drug_form':drug_form,
                'drug_spec':drug_spec
            }
            drugs_list = []
            drugs_list.append(drugs_dict)
            item_drug = {'drugs':drugs_list}
            '''
            drugs_dict_list = process_drug_main(disease_name)
            item['drugs'] = drugs_dict_list
            #9、如何预防
            how_prevent = 'null'
            how_prevent = process_disease_how_prevent_main(disease_name)
            item['how_prevent'] = how_prevent

            #10、问答预料
            qa_corpus = 'null'
            qa_corpus = process_qa_corpus_main()
            item['qa_corpus'] = qa_corpus
            
            currenttime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
            item['create_time'] = currenttime
            item['update_time'] = currenttime
            item['source'] = 'jbk.39.net'

            items.append(item)
        return items

    
