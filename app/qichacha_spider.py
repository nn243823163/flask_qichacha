# -*- coding: utf-8 -*-
import requests
import sqlite3
import time
from my_function import *
from config import *
import json
import hashlib
import datetime
def qichacha_spider_list(keyword):
    global new_cookies
    headers = {'Host': 'www.qichacha.com',
               'Connection': 'keep-alive',
               'Accept': '*/*',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.9.1.1000 Chrome/39.0.2146.0 Safari/537.36',
               'DNT': '1',
               'Accept-Encoding': 'gzip,deflate',
               'Accept-Language': 'zh-CN'}
    data = {'t': '1467102926684'}
    url = r'http://www.qichacha.com/search_index?key=' + str(keyword) + r'&index=0&statusCode=&registCapiBegin=&registCapiEnd=&sortField=&isSortAsc=&province=&startDateBegin=&startDateEnd=&cityCode=&ajaxflag=true&p=1'
    r = requests.get(url, cookies=new_cookies,
                     headers=headers)
    html_doc = r.text
    #首先判断加载回来的网页是否正确  再选择是否进行清洗
    status = None
    #html_doc.find(u'查看更多信息')
    if html_doc=='':
        status = u'返回网页为空'
    elif html_doc.find(u'查看更多信息') >= 0 or html_doc.find(u'后可以查看更多数据') >= 0   or html_doc.find(u'请登录后再查询') >= 0 :
        status = u'错误信息：未成功登录企查查或cookie过期'
    elif html_doc.find(u'location.href = \'http://www.qichacha.com/index_verify?type=companysearch&back=/') >= 0:
        status = u'错误信息：列表操作过于频繁'
    elif html_doc.find(u'小查还没找到数据') >= 0:
        status = u'错误信息：没有查询到数据'
    elif html_doc.find(u'您的搜索词太宽泛') >= 0:
        status = u'错误信息：您的搜索词太宽泛，建议更换一下搜索词'


    if status != None:#表示查询出错  返回None 跟错误信息
        return None,status
    args_list = list()
    args_dict = dict()
    args_dict_tmp = dict()

    spider_list = re_spider_list(html_doc)
    if len(spider_list) > 0:  # 表示匹配到了股东信息
        for i in range(0, len(spider_list)):
            uid = data_sub(spider_list[i][1])
            name = data_sub(spider_list[i][2])
            area = data_sub(spider_list[i][0])
            args_dict_tmp = dict()
            args_dict_tmp['uid'] = uid
            args_dict_tmp['name'] = name
            args_dict_tmp['area'] = area
            #print (args_dict_tmp)
            args_list.append(args_dict_tmp)
        #print(args_list)
    else:
        status = u'错误信息：未知错误'
        return None, status
    args_dict['results'] = args_list
    args_dict['count'] = i+1
    args_dict['next'] = None
    args_dict['previous'] = None
    #print (args_dict)
    json_list = json.dumps(args_dict, ensure_ascii=False)#将清洗的数据转换成json格式
    return json_list,None
def qichacha_deal_data(Uid,Area,Companyname,html_doc):
    alt_list = list()
    shareholder_list = list()
    principal_list = list()
    abnormity_list = list()
    branch_list = list()
    args_dict = dict()
    json_dict = dict()
    uuid = hashlib.md5(str(Uid).encode('utf-8')).hexdigest()
    # print(uuid)
    reg_code = re_deal(re_reg_code, html_doc)
    # 注册号：
    org_code = re_deal(re_org_code, html_doc)
    # 组织机构代码：
    uniform_code = re_deal(re_uniform_code, html_doc)
    # 统一社会信用代码：
    org_type = re_deal(re_org_type, html_doc)
    # 公司类型：
    est_date = re_deal(re_est_date, html_doc, 1, True)
    # 成立日期：
    issue_date = re_deal(re_issue_date, html_doc, 1, True)
    # 发照日期：
    op_from = re_deal(re_op_from, html_doc, 1, True)
    # 营业期限自
    op_to = re_deal(re_op_to, html_doc, 1, True)
    # 营业期限至     1表示去正则分组1   无固定期限
    if op_to != None:
        if op_to.find(u'固') > 0:
            op_to = '9999-12-31'
    corp_rpt = re_deal(re_corp_rpt, html_doc)
    # 法定代表人
    reg_cap = re_deal(re_reg_cap, html_doc)
    # 注册资本    需要添加字典值
    if reg_cap == None:
        reg_cap_type = 'Y00001'
    else:
        if reg_cap.find(u'美') > 0:
            reg_cap_type = 'Y00002'
        else:
            reg_cap_type = 'Y00001'
        reg_cap = reg_cap[0:reg_cap.find(u'万')]
        reg_cap = reg_cap.replace(',', '')
        reg_cap = reg_cap.replace(r'#& nbsp;', '')
        reg_cap = reg_cap.replace(r'&nbsp;', '')
        reg_cap = reg_cap.replace(r')', '')
        if reg_cap.replace(' ', '') == '' or reg_cap.find('null') > 0:
            reg_cap = None
        elif reg_cap.find(u'人民币') > 0:  # 表示以元为单位
            reg_cap = reg_cap[0:reg_cap.find(u'人民币')]
            reg_cap = float(reg_cap) / 10000
        else:
            try:
                # print(reg_cap, uid)
                reg_cap = float(reg_cap)
            except ValueError as e:
                #print(reg_cap, e)
                reg_cap = None
    reg_state = re_deal(re_reg_state, html_doc)
    # 经营状态：
    reg_org = re_deal(re_reg_org, html_doc)
    # 工商登记机关
    address = re_deal(re_address, html_doc)
    # 企业地址：
    op_scope = re_deal(re_op_scope, html_doc)
    # 经营范围：
    org_english_name = re_deal(re_org_english_name, html_doc)
    # 英\s?文\s?名：
    industry = re_deal(re_industry, html_doc)
    # 所属行业：
    org_scale = re_deal(re_org_scale, html_doc)
    # 公司规模：
    org_detail = re_deal(re_org_detail, html_doc)
    # 公司简介：
    org_name = Companyname
    # 公司名称
    location = location_mapping.get(Area)
    args_dict['org_id'] = uuid
    args_dict['reg_code'] = reg_code    # 注册号
    args_dict['org_code'] = org_code    # 组织机构代码
    args_dict['uniform_code'] = uniform_code    # 统一社会信用代码
    args_dict['org_type'] = org_type    # 公司类型
    args_dict['est_date'] = est_date    # 成立日期
    args_dict['issue_date'] = issue_date    # 发照日期
    args_dict['op_from'] = op_from  # 营业期限自
    args_dict['op_to'] = op_to    # 营业期限至
    args_dict['corp_rpt'] = corp_rpt    # 法定代表人
    args_dict['reg_cap'] = reg_cap    # 注册资本    需要添加字典值
    args_dict['reg_state'] = reg_state    # 经营状态：
    args_dict['reg_org'] = reg_org    # 工商登记机关
    args_dict['address'] = address    # 企业地址
    args_dict['op_scope'] = op_scope    # 经营范围
    args_dict['org_english_name'] = org_english_name    # 英\s?文\s?名
    args_dict['industry'] = industry   # 所属行业
    args_dict['org_scale'] = org_scale    # 公司规模
    args_dict['org_detail'] = org_detail    # 公司简介
    args_dict['org_name'] = org_name       # 公司名称
    args_dict['location'] = location    # Area
    #######################################################
    ########################################################企业变更信息
    text_right = get_text_right(u'变更记录', html_doc)
    if text_right != None:  # 返回的数据不为空 表示存在股东信息
        ent_alt_list = re_ent_alt(text_right)
        if len(ent_alt_list) > 0:  # 表示匹配到了变更公告
            for i in range(0, len(ent_alt_list)):
                # data_sub() 去除空格与html 标签    ent_alt_list   生成变更公告列表
                alt_dict = dict()
                approve_date = data_sub(ent_alt_list[i][1])
                alt_item = data_sub(ent_alt_list[i][0])
                alt_item_en_h = data_sub(ent_alt_list[i][3])
                alt_item_en_q = data_sub(ent_alt_list[i][2])
                alt_dict['approve_date'] = approve_date
                alt_dict['alt_item'] = alt_item
                alt_dict['alt_item_en_h'] = alt_item_en_h
                alt_dict['alt_item_en_q'] = alt_item_en_q
                alt_dict['ent_pk'] = uuid

                alt_list.append(alt_dict)
    if len(alt_list) == 0:
        alt_list = None


    #####################################################################################股东信息
    text_right = get_text_right(u'股东信息', html_doc)
    if text_right != None:  # 返回的数据不为空 表示存在股东信息
        ent_shareholder_list = re_ent_shareholder(text_right)
        if len(ent_shareholder_list) > 0:  # 表示匹配到了股东信息
            for i in range(0, len(ent_shareholder_list)):
                shareholder_dict = dict()
                shareh_pk = data_sub(ent_shareholder_list[i][1])
                if shareh_pk != None:
                    shareh_pk = hashlib.md5(str(shareh_pk).encode('utf-8')).hexdigest()
                else:
                    shareh_pk = None
                shareholder = data_sub(ent_shareholder_list[i][2])
                shareh_type = data_sub(ent_shareholder_list[i][3])
                subscribe_invest_amount = data_sub(ent_shareholder_list[i][4])
                subscribe_invest_date = data_sub(ent_shareholder_list[i][5])
                invest_amount = data_sub(ent_shareholder_list[i][6])
                invest_date = data_sub(ent_shareholder_list[i][7])
                if shareholder != None:
                    shareholder_dict['shareh_pk'] = shareh_pk
                    shareholder_dict['shareholder'] = shareholder
                    shareholder_dict['shareh_type'] = shareh_type
                    shareholder_dict['subscribe_invest_amount'] = subscribe_invest_amount
                    shareholder_dict['subscribe_invest_date'] = subscribe_invest_date
                    shareholder_dict['invest_amount'] = invest_amount
                    shareholder_dict['invest_date'] = invest_date
                    shareholder_dict['ent_pk'] = uuid
                    shareholder_list.append(shareholder_dict)
    if len(shareholder_list) == 0:
        shareholder_list = None

    # 企业地址：
    ################################################################企业主要人员
    text_right = get_text_right(u'主要人员', html_doc)
    if text_right != None:  # 返回的数据不为空 表示存在股东信息
        ent_principal_list = re_ent_principal(text_right)
        if len(ent_principal_list) > 0:  # 表示匹配到了股东信息
            for i in range(0, len(ent_principal_list)):
                principal_dict = dict()
                ent_name = data_sub(ent_principal_list[i][0])
                ent_position = data_sub(ent_principal_list[i][1])
                if ent_name != None:
                    principal_dict['ent_name'] = ent_name
                    principal_dict['ent_position'] = ent_position
                    principal_dict['ent_pk'] = uuid
                    principal_dict['order_code'] = i+1
                    principal_list.append(principal_dict)
    if len(principal_list) == 0:
        principal_list = None

    ####################################################################################################################企业分支机构
    text_right = get_text_right(u'分支机构', html_doc)
    if text_right != None:  # 返回的数据不为空 表示存在分支机构
        ent_branch_list = re_ent_branch(text_right)
        if len(ent_branch_list) > 0:  # 表示匹配到了
            for i in range(0, len(ent_branch_list)):
                branch_dict = dict()
                # data_sub() 去除空格与html 标签    ent_branch_list   生成分支机构列表
                branch_name = data_sub(ent_branch_list[i][0])
                ent_uid = data_sub(ent_branch_list[i][3])
                ent_area = data_sub(ent_branch_list[i][2])
                if ent_uid != None:
                    branch_pk = hashlib.md5(str(ent_uid).encode('utf-8')).hexdigest()
                else:
                    branch_pk = None
                if branch_name != None:
                    branch_dict['branch_pk'] = branch_pk
                    branch_dict['branch_name'] = branch_name
                    branch_dict['ent_uid'] = ent_uid
                    branch_dict['ent_area'] = ent_area
                    branch_dict['order_code'] = i+1
                    branch_dict['ent_pk'] = uuid
                    branch_list.append(branch_dict)
    if len(branch_list) == 0:
        branch_list = None
    #################################################################################经营异常
    text_right = get_text_right(u'经营异常', html_doc)
    if text_right != None:  # 返回的数据不为空 表示存在
        ent_abnormity_list = re_ent_abnormity(text_right)
        if len(ent_abnormity_list) > 0:  # 表示匹配到了股东信息
            for i in range(0, len(ent_abnormity_list)):
                abnormity_dict = dict()
                record_date = data_sub(ent_abnormity_list[i][0])  # 列入日期
                removal_date = data_sub(ent_abnormity_list[i][1])  # 移出日期
                decision_org = data_sub(ent_abnormity_list[i][2])  # 做出决定机关
                record_reason = data_sub(ent_abnormity_list[i][3])  # 列入经营异常名录原因
                removal_reason = data_sub(ent_abnormity_list[i][4])  # 移出经营异常名录原因

                abnormity_dict['record_date'] = record_date
                abnormity_dict['removal_date'] = removal_date
                abnormity_dict['removal_reason'] = removal_reason
                abnormity_dict['decision_org'] = decision_org
                abnormity_dict['record_reason'] = record_reason
                abnormity_dict['ent_pk'] = uuid
                abnormity_dict['order_code'] = i+1
                abnormity_list.append( abnormity_dict)
    if len(abnormity_list) == 0:
        abnormity_list = None








    #print(args_dict)
    json_dict['org_info'] = args_dict
    json_dict['ent_alt'] = alt_list
    json_dict['ent_shareholder'] = shareholder_list
    json_dict['ent_principal'] = principal_list
    json_dict['ent_branch'] = branch_list
    json_dict['ent_abnormity'] = abnormity_list
    json_list = json.dumps(json_dict)  # 将清洗的数据转换成json格式
    return json_list
def qichacha_spider_content(Uid,Area,Companyname):
    global new_cookies
    headers = {'Host': 'www.qichacha.com',
               'Connection': 'keep-alive',
               'Accept': '*/*',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.9.1.1000 Chrome/39.0.2146.0 Safari/537.36',
               'DNT': '1',
               'Accept-Encoding': 'gzip,deflate',
               'Accept-Language': 'zh-CN'}

    index_url = 'http://www.qichacha.com/firm_'+Area+'_'+Uid

    url_base = r'http://www.qichacha.com/company_getinfos?unique='+Uid+'&companyname='+Companyname+'&tab=base'
    r = requests.get(url_base, cookies=new_cookies,headers=headers)
    html_doc = r.text
    #首先判断加载回来的网页是否正确  再选择是否进行清洗
    status = None
    #html_doc.find(u'查看更多信息')
    if html_doc=='':
        status = u'返回网页为空'
    elif re_qichacha_content_err_exp.search(html_doc)!=None:#正则匹配到  说明未成功登录
        status = u'错误信息：未成功登录企查查或cookie过期'
    elif html_doc.find(u'location.href=\'http://www.qichacha.com/index_verify?type=companyview') >= 0:
        status = u'错误信息：列表操作过于频繁'
    elif html_doc.find(u'小查还没找到数据') >= 0:
        status = u'错误信息：没有查询到数据'
    if status != None:#表示查询出错  返回None 跟错误信息
        return None,status
    json_list = qichacha_deal_data(Uid,Area,Companyname,html_doc)
    return json_list,None
##############################################################################################
new_cookies = {'CNZZDATA1254842228':'1599666056-1466385351-http%253A%252F%252Fwww.baidu.com%252F%7C1468286470',
'gr_user_id':'364935ce-956e-4ccd-9b17-c21ad3b123f9',
'PHPSESSID':'mk4kpf1uvm5bahf0tn40u24pn1',
'gr_session_id_9c1eb7420511f8b2':'5a71a8c5-0880-41ec-8b4b-f16323ffd1b7'}
#new_cookies = {}

#new_cookies = {}
# json_list, status = qichacha_spider_list('法人')
json_list , status= qichacha_spider_content('177a6596027d4ecc21c47d06162c080c','ZJ',u'嘉善三信酒庄')
print (json_list)
print (status)