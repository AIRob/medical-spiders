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

class ProcessDrug(object):
    """docstring for ClassName"""
    
    def __init__(self, url):
        #super(ClassName, self).__init__()
        self.url = url

    def process_drug_url(self):
        header={'User-Agent':ChoiceUAIP().choice_ua()}       
        request = Request(self.url,headers=header)
        opener = ChoiceUAIP().choice_proxy()
        response = opener.open(request).read()
        if response is None:pass
        allcontent = response.decode('gb2312','ignore')
        selector=etree.HTML(allcontent) #将源码转化为能被XPath匹配的格式 
        #/html/body/div[8]/div[2]/ul/li[1]/div[1]/strong/a
        hrefs = selector.xpath('//div[@class="msgs"]/strong/a/@href')
        if hrefs is None:pass
        drughrefs = []
        for i in range(len(hrefs)):
            drughref = 'http://ypk.39.net{}manual'.format(hrefs[i])
            drughrefs.append(drughref)
        return drughrefs    
           
    def process_drugs_manual_detail(self,durgurl):
        druginfo_url = durgurl+'manual'
        header={'User-Agent':ChoiceUAIP().choice_ua()}    
        request = Request(druginfo_url,headers=header)
        opener = ChoiceUAIP().choice_proxy()
        try:       	
            response = opener.open(request).read()
            if response is None:pass
            allcontent = response.decode('gb2312','ignore')
            if allcontent is None:pass
            selector=etree.HTML(allcontent) #将源码转化为能被XPath匹配的格式
            drugs_info = selector.xpath('//div[@class="tab_box"]/div//text()')
            #print(drugs_info)
            strs = '++'.join(drugs_info)
            #print(''.join(strs.split()).replace('++',''))
            strs = ' '.join(strs.split()).replace('++','')
        except Exception as e:
            print('web null')
            pass
        return strs
        '''
        response = opener.open(request).read()            
        
        if response is None:pass
        allcontent = response.decode('gb2312','ignore')
        if allcontent is None:pass
        selector=etree.HTML(allcontent) #将源码转化为能被XPath匹配的格式
        
        #/html/body/div[9]/div[2]/div[3]/div/dl[1]/dd/p/text()[1]
        drugs_info = selector.xpath('//div[@class="tab_box"]/div//text()')
        #print(drugs_info)
        strs = '++'.join(drugs_info)
        #print(''.join(strs.split()).replace('++',''))
        strs = ' '.join(strs.split()).replace('++','')
        return strs
        ################################3
        drugs_dict = {
                'goods_id':goods_id,
                'goods_name':goods_name,
                'goods_common_name':goods_common_name,
                'goods_english_name':goods_english_name,
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
        drugs_res = {'drugs':drugs_list}
        return drugs_res
        '''

    def process_drugs_overview_detail(self,drugurl):
        '''
        药品概述详细信息
        '''
        print(drugurl)
        viewurl = drugurl.replace('manual','')
        print(viewurl)
        header={'User-Agent':ChoiceUAIP().choice_ua()}    
        request = Request(viewurl,headers=header)
        opener = ChoiceUAIP().choice_proxy()
        response = opener.open(request).read()            
        if response is None:pass
        allcontent = response.decode('gb2312','ignore')
        if allcontent is None:pass
        selector=etree.HTML(allcontent) #将源码转化为能被XPath匹配的格式
        if selector.xpath('//div[@class="gaisu"]//ul[@class="showlis"]/li[1]/text()') is None:
           drug_form = selector.xpath('//div[@class="gaisu"]//ul[@class="showlis"]/li[1]/text()')[0]
           print(drug_form)
    
           #/html/body/div[12]/div[2]/div[1]/div[1]/ul[2]/li[2]/text()
           drug_spec = selector.xpath('//div[@class="gaisu"]//ul[@class="showlis"]/li[2]/text()')[0]
           print(drug_spec)
        else:
            drug_form = 'null'
            drug_spec = 'null'

        therapeutic_diseases = selector.xpath('//div[@class="gs_right"]/ul[@class="whatsthis clearfix"]/li//text()')
        #therapeutic_diseases = ' '.join(therapeutic_diseases)
        print('治疗常用疾病:{}'.format(therapeutic_diseases))
        key_list = ['drug_form','drug_spec','therapeutic_diseases']
        val_list = [drug_form,drug_spec,therapeutic_diseases]

        '''
        vals_list = []
        keys_list = []

        keys_list.extend(key_list)
        vals_list.extend(val_list)
        #vals_list.append(drug_form)
        #vals_list.append(drug_spec)
        #vals_list.append(therapeutic_diseases)
        dict_test = dict(zip(keys_list,vals_list))
        print(dict_test)
        '''
        return key_list,val_list

    def key_value_map(self,strs,drugurl):

        mystrs = strs.split('【')
        key_list = []
        value_list = []
        for i in range(len(mystrs)):
            substrs = mystrs[i].split('】')
            key_list.append(substrs[0])
            value_list.append(substrs[-1])
        #print(value_list[1])

        
        namestr = value_list[1].split('：')
        keys_list,vals_list = self.handle_name(namestr)
        keys_list.extend(key_list[2:-1])
        vals_list.extend(value_list[2:-1])  
        manufacstr = value_list[-1].split('：')
        #print(manufacstr)
        #print(len(manufacstr))
        view_key_list,view_val_list = self.process_drugs_overview_detail(drugurl)
        keys_list.extend(view_key_list)
        vals_list.extend(view_val_list)
        man_keys_list,man_vals_list = self.handle_manufac(manufacstr)
        print(man_keys_list)
        print(man_vals_list)
        keys_list.extend(man_keys_list)
        vals_list.extend(man_vals_list)
        
        dict_test = dict(zip(keys_list,vals_list))
        #print(dict_test)
        dict_info = self.update_dictkey_ch_en(dict_test)
        if 'goods_common_name' in dict_info.keys():
            goods_common_name = dict_info['goods_common_name']
        else:
            goods_common_name = 'null'
        if 'approval_rum' in dict_info.keys():
            approval_rum = dict_info['approval_rum']
        else:
            approval_rum = 'null'
        import hashlib
        
        hash = hashlib.md5()
        hash.update(str(goods_common_name+approval_rum).encode('utf-8'))
        goods_id = hash.hexdigest()

        dict_info['goods_id'] = goods_id
        #print(dict_info)
        empty_dict = self.create_empty_dict()
        out_dict = self.merge_dict(dict_info,empty_dict)
        return out_dict
    
    def merge_dict(self,first_dict,sec_dict):
        '''
        OK
        '''
        res_dict = {}
        res_dict.update(sec_dict)
        res_dict.update(first_dict)
        return res_dict

    def handle_name(self,namestr):            
        keys_list = []
        vals_list = []
        print(namestr)

        #for i in range(len(namestr)):
        name_first_key = namestr[0].strip()
        #print(name_first_key)
        #namekv = namestr[1].split(' ')
        #['   通用名称', '全自动臂式电子血压计(商品名', '西铁城电子血压计)     ']
        if len(namestr) == 2:
            name_first_val = namestr[1]
            key_list = [name_first_key]
            val_list = [name_first_val]
            keys_list.extend(key_list)
            vals_list.extend(val_list)
        elif len(namestr) == 3:
            name_first_val = namestr[1].split(' ')[0]           
            print(name_first_val)
            if '(' in name_first_val:
                name_first_val = namestr[1].split(' ')[0].split('(')[0]
                name_sec_key = namestr[1].split(' ')[0].split('(')[1]
                name_sec_val = namestr[2].split(')')[0]
            else:
                name_sec_key = namestr[1].split(' ')[1].strip()
                name_sec_val = namestr[2]
            key_list = [name_first_key,name_sec_key]
            val_list = [name_first_val,name_sec_val]
            keys_list.extend(key_list)
            vals_list.extend(val_list)
        elif len(namestr) == 4:
            name_first_val = namestr[1].split(' ')[0]
            #print(name_first_val)
            name_sec_key = namestr[1].split(' ')[1].strip()            
            name_sec_val = namestr[2].split(' ')[0]
            name_th_key = namestr[2].split(' ')[1].strip()
            name_th_val = namestr[3]
            key_list = [name_first_key,name_sec_key,name_th_key]
            val_list = [name_first_val,name_sec_val,name_th_val]
            keys_list.extend(key_list)
            vals_list.extend(val_list)
        #特殊出口少数
        ##['   商品名称', '妙诊 通用名称', '全自动血压计(商品名', '妙诊) 英文名称', 'Electronic blood pressure monitors    ']
        elif len(namestr) == 5:
            name_first_val = namestr[1].split(' ')[0]
            #print(name_first_val)
            name_sec_key = namestr[1].split(' ')[1].strip()            
            name_sec_val = namestr[2].split('(')[0]
            name_th_key = namestr[2].split('(')[1].strip()
            name_th_val = namestr[3].split(')')[0]
            name_four_key = namestr[3].split(')')[1].strip()
            name_four_val = namestr[4]
            key_list = [name_first_key,name_sec_key,name_th_key,name_four_key]
            val_list = [name_first_val,name_sec_val,name_th_val,name_four_val]
            keys_list.extend(key_list)
            vals_list.extend(val_list)
        return  keys_list,vals_list   

    def handle_manufac(self,manufacstr):            
        keys_list = []
        vals_list = []
        print(manufacstr)
        #for i in range(len(manufacstr)):
        manufac_first_key = manufacstr[0].strip()
        #print(name_first_key)
        #namekv = namestr[1].split(' ')
        if "市场部" in manufacstr:manufacstr.remove("市场部")
        if "0311-86012404 客户服务热线" in manufacstr:manufacstr.remove("0311-86012404 客户服务热线")
        if '原料药（含头孢菌素类、含抗肿瘤类）、无菌原料药（含头孢菌素类）、精神药品,连云港经济技术开发区庐山路8号  ' in manufacstr:
            manufacstr.remove("0311-86012404 客户服务热线")
        if len(manufacstr) == 2:
            manufac_first_val = manufacstr[1]
            key_list = [manufac_first_key]
            val_list = [manufac_first_val]
            keys_list.extend(key_list)
            vals_list.extend(val_list) 
        #['  企业名称', '德国 保赫曼股份公司   生产地址', 'Paul-Hartmann-StraBe 12D-89522 Heidenheim  ']
        elif len(manufacstr) == 3:
            manufac_first_val = manufacstr[1].split('  ')[0]
            #print(name_first_val)
            manufac_sec_key = manufacstr[1].split('  ')[1].strip()
            manufac_sec_val = manufacstr[2]
            key_list = [manufac_first_key,manufac_sec_key]
            val_list = [manufac_first_val,manufac_sec_val]
            keys_list.extend(key_list)
            vals_list.extend(val_list)

        elif len(manufacstr) == 4:
            manufac_first_val = manufacstr[1].split('  ')[0]
            #print(name_first_val)
            manufac_sec_key = manufacstr[1].split('  ')[1].strip()           
            manufac_sec_val = manufacstr[2].split('  ')[0]
            manufac_th_key = manufacstr[2].split('  ')[1].strip()
            manufac_th_val = manufacstr[3]
            key_list = [manufac_first_key,manufac_sec_key,manufac_th_key]
            val_list = [manufac_first_val,manufac_sec_val,manufac_th_val]
            keys_list.extend(key_list)
            vals_list.extend(val_list)

        elif len(manufacstr) == 5:
            manufac_first_val = manufacstr[1].split('  ')[0]
            manufac_sec_key = manufacstr[1].split('  ')[1].strip()           
            manufac_sec_val = manufacstr[2].split('  ')[0]
            manufac_th_key = manufacstr[2].split('  ')[1].strip()
            manufac_th_val = manufacstr[3].split('  ')[0]            
            manufac_four_key = manufacstr[3].split('  ')[1].strip() or manufacstr[3].split(' ')[1].strip() or manufacstr[3].split('   ')[1].strip()
            #manufac_four_key = manufacstr[3].split(' ')[1].strip()
            manufac_four_val = manufacstr[4]
            key_list = [manufac_first_key,manufac_sec_key,manufac_th_key,manufac_four_key]
            val_list = [manufac_first_val,manufac_sec_val,manufac_th_val,manufac_four_val]
            keys_list.extend(key_list)
            vals_list.extend(val_list)
        else:
            pass
        return  keys_list,vals_list

    def update_dictkey_ch_en(self,drugs_dict):
        if "通用名称" in drugs_dict.keys():drugs_dict.update(goods_common_name = drugs_dict.pop("通用名称"))
        else:pass
        if "治疗病种" in drugs_dict.keys():drugs_dict.update(therapeutic_disease = drugs_dict.pop("治疗病种"))
        else:pass
        if "商品名称" in drugs_dict.keys():drugs_dict.update(goods_name = drugs_dict.pop("商品名称"))
        else:pass
        if "商品名" in drugs_dict.keys():drugs_dict.update(goods_name = drugs_dict.pop("商品名"))
        else:pass
        if "英文名称" in drugs_dict.keys():drugs_dict.update(english_name = drugs_dict.pop("英文名称"))
        else:pass
        if "药品价格" in drugs_dict.keys():drugs_dict.update(goods_price = drugs_dict.pop("药品价格"))
        else:pass
        if "批准文号" in drugs_dict.keys():drugs_dict.update(approval_rum = drugs_dict.pop("批准文号"))
        else:pass
        if "适应症" in drugs_dict.keys():drugs_dict.update(indication = drugs_dict.pop("适应症"))
        else:pass
        if "功能主治" in drugs_dict.keys():drugs_dict.update(functions = drugs_dict.pop("功能主治"))
        else:pass
        if "成份" in drugs_dict.keys():drugs_dict.update(ingredients = drugs_dict.pop("成份"))
        else:pass
        if "不良反应" in drugs_dict.keys():drugs_dict.update(adverse_reactions = drugs_dict.pop("不良反应"))
        else:pass
        if "注意事项" in drugs_dict.keys():drugs_dict.update(precautions = drugs_dict.pop("注意事项"))
        else:pass
        if "禁忌" in drugs_dict.keys():drugs_dict.update(taboo = drugs_dict.pop("禁忌"))
        else:pass
        if "药物相互作用" in drugs_dict.keys():drugs_dict.update(medicine_interactions = drugs_dict.pop("药物相互作用"))
        else:pass
        if "药理作用" in drugs_dict.keys():drugs_dict.update(pharmacological_action = drugs_dict.pop("药理作用"))
        else:pass  
        if "特殊人群用药" in drugs_dict.keys():drugs_dict.update(special_population = drugs_dict.pop("特殊人群用药"))
        else:pass
        if "用法用量" in drugs_dict.keys():drugs_dict.update(dosage = drugs_dict.pop("用法用量"))
        else:pass
        if "贮藏" in drugs_dict.keys():drugs_dict.update(storage = drugs_dict.pop("贮藏"))
        else:pass
        if "有效期" in drugs_dict.keys():drugs_dict.update(validity_period = drugs_dict.pop("有效期"))
        else:pass 
        if "剂型" in drugs_dict.keys():drugs_dict.update(drug_form = drugs_dict.pop("剂型"))
        else:pass
        if "规格" in drugs_dict.keys():drugs_dict.update(drug_spec = drugs_dict.pop("规格"))
        else:pass
        if "说明书修订日期" in drugs_dict.keys():drugs_dict.update(manual_revision_date = drugs_dict.pop("说明书修订日期"))
        else:pass
        if "企业名称" in drugs_dict.keys():drugs_dict.update(manufacturer = drugs_dict.pop("企业名称"))
        else:pass 
        if "企业简称" in drugs_dict.keys():drugs_dict.update(business_short_name = drugs_dict.pop("企业简称"))
        else:pass
        if "生产地址" in drugs_dict.keys():drugs_dict.update(production_address = drugs_dict.pop("生产地址"))
        else:pass
        if "联系电话" in drugs_dict.keys():drugs_dict.update(business_number = drugs_dict.pop("联系电话"))
        else:pass                                             
        #print(drugs_dict)
        return drugs_dict

    def create_empty_dict(self):
        goods_id = 'null'
        goods_name = 'null'
        goods_common_name = 'null'
        goods_english_name = 'null'
        goods_price = 0
        therapeutic_disease = 'null'
        approval_rum = 'null'
        indication = 'null'
        functions = 'null'
        #is_import = 'null'        
        ingredients = 'null'
        adverse_reactions = 'null'
        precautions = 'null'
        taboo = 'null'
        medicine_interactions = 'null'
        pharmacological_action = 'null'
        special_population = 'null'
        dosage = 'null'
        storage = 'null'
        validity_period = 'null'
        drug_form = 'null'
        drug_spec = 'null'
        manufacturer = 'null'
        manual_revision_date = 'null'
        business_short_name = 'null'
        production_address = 'null'
        business_number = 'null'
        drugs_empty_dict = {
                'goods_id':goods_id,
                'goods_name':goods_name,
                'goods_common_name':goods_common_name,
                'english_name':goods_english_name,
                'goods_price':goods_price,
                'therapeutic_disease':therapeutic_disease,

                'approval_rum':approval_rum,
                'indication':indication,
                'functions':functions,
                #'is_import':is_import,
                'ingredients':ingredients,
                'adverse_reactions':adverse_reactions,
                'precautions':precautions,
                'taboo':taboo,
                'medicine_interactions':medicine_interactions,
                'pharmacological_action':pharmacological_action,
                'special_population':special_population,
                'dosage':dosage,
                'storage':storage,
                'validity_period':validity_period,
                'drug_form':drug_form,
                'drug_spec':drug_spec,
                'manual_revision_date':manual_revision_date,
                'manufacturer':manufacturer,
                'business_short_name':business_short_name,
                'production_address':production_address,
                'business_number':business_number
        }
        return drugs_empty_dict

def process_drug_main(disease):
    #http://ypk.39.net/search/%E6%8A%91%E9%83%81%E7%97%87-p2/
    #disease = '抑郁症'    
    #http://ypk.39.net/search/%E9%AB%98%E8%A1%80%E5%8E%8B-p134/
    #disease = '高血压'

    drug_dict_list = []
    for i in range(1,135):
        print('processing ...... page {}'.format(i))
        url='http://ypk.39.net/search/{0}-p{1}/'.format(parse.quote(disease),i)
        print(url)
        ps = ProcessDrug(url)

        mulurl = ps.process_drug_url()
        print(mulurl)
        if mulurl is None:
            print('process web ... false')
            break
        sleep_time = [19,20,25,10,30,22,16,18,24,33,24,31]
        from random import choice 
        time.sleep(choice(sleep_time))
        for j in range(15):
            print('processing {} row goods .......'.format(j))
            #drugurl = mulurl[j]
            try:
                drugurl = mulurl[j]
                if drugurl is None:pass
                print(drugurl)
                #time.sleep(3)
                #if i == 27 and j == 10:pass

                drug_dict_str = ps.process_drugs_manual_detail(drugurl)
                #ps.process_drugs_overview_detail(drugurl)
            
                drug_dict_temp = ps.key_value_map(drug_dict_str,drugurl)
                #dict_res = ps.update_dictkey_ch_en(drug_dict_temp)
                drug_dict_list.append(drug_dict_temp)
                #drug_dict_list.append(dict_res)
            except Exception as e:
                print('page {0} row {1}'.format(i,j))
                pass
            '''
            drugurl = mulurl[j]
            if drugurl is None:pass
            print(drugurl)
            #time.sleep(3)
            #if i == 27 and j == 10:pass
            drug_dict_str = ps.process_drugs_manual_detail(drugurl)
            #ps.process_drugs_overview_detail(drugurl)
            
            drug_dict_temp = ps.key_value_map(drug_dict_str,drugurl)
            #dict_res = ps.update_dictkey_ch_en(drug_dict_temp)
            drug_dict_list.append(drug_dict_temp)
            #drug_dict_list.append(dict_res)
            '''
    print(drug_dict_list)
    return drug_dict_list        
    '''
    res = {'drugs':drug_dict_list}
    import json
    with open('./xxxxxxxxxx.json', 'w') as file_obj:
        #写入json文件
        json.dump(res, file_obj)
    return res
    '''

if __name__ == '__main__':
    disease = '高血压'
    process_drug_main(disease)
