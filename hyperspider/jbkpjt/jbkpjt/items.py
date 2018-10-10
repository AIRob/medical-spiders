# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JbkpjtItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    disease_id = scrapy.Field() #疾病id
    disease_name = scrapy.Field() #疾病名
    
    ##########################################
    disease_profile = scrapy.Field() #疾病简介

    ##########################################
    disease_base = scrapy.Field() #疾病基本知识
    disease_alias = scrapy.Field() #别名
    is_medical = scrapy.Field() #是否属于医保
    incidence_site = scrapy.Field() #发病部位
    contagious = scrapy.Field() #传染性
    multiple_people = scrapy.Field() #多发人群
    typical_symptoms = scrapy.Field() #典型症状
    complication = scrapy.Field() #并发症
    
    ##########################################
    disease_diagnosis = scrapy.Field() #疾病诊断
    best_time = scrapy.Field() #最佳就诊时间
    duration_visit = scrapy.Field() #就诊时长
    followup_freq = scrapy.Field() #复诊频率
    pre_treat = scrapy.Field() #就诊前准备

    ##########################################    
    disease_check = scrapy.Field() #临床检查

    ##########################################   
    disease_symptoms = scrapy.Field() #疾病症状
    related_symptoms = scrapy.Field() #相关症状

    ########################################## 
    disease_cause = scrapy.Field() #疾病病因

    ##########################################    
    disease_treat = scrapy.Field() #疾病治疗
    treat_method = scrapy.Field() #治疗方法
    treat_costs = scrapy.Field() #治疗费用
    cure_rate = scrapy.Field() #治愈率
    treat_cycle = scrapy.Field() #治疗周期
    common_drugs = scrapy.Field() #常用药品
    visit_department = scrapy.Field() #就诊科室

    ##########################################   
    drugs = scrapy.Field() #drugs info 字典
    goods_id = scrapy.Field() #"药品id":"md5(疾病+药品名)"
    goods_price = scrapy.Field() #价格
    goods_common_name = scrapy.Field() #药品通用名
    approval_rum = scrapy.Field() #批准文号
    indication = scrapy.Field() #适应症
    functions = scrapy.Field() #功能主治
    #is_import = scrapy.Field() #是否是进口药
    manufacturer = scrapy.Field() #生产企业
    ingredients = scrapy.Field() #成份
    adverse_reactions = scrapy.Field() #不良反应
    precautions = scrapy.Field() #注意事项
    taboo = scrapy.Field() #禁忌
    medicine_interactions = scrapy.Field() #药物相互作用
    pharmacological_action = scrapy.Field() #药理作用
    special_population = scrapy.Field() #特殊人群用药
    dosage = scrapy.Field() #用法用量
    drug_form = scrapy.Field() #剂型
    drug_spec = scrapy.Field() #规格

    ##########################################  
    how_prevent = scrapy.Field() #如何预防

    ##########################################  
    qa_corpus = scrapy.Field() #问答语料

    ##########################################  
    create_time = scrapy.Field() #入库时间
    update_time = scrapy.Field() #更新时间
    source = scrapy.Field() #来源

   