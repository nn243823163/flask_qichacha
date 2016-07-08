# -*- coding: utf-8 -*-
import re
re_sub=re.compile(u'\s|<[^>]*>')
re_date=re.compile(u'\d{4}-\d{1,2}-\d{1,2}')
re_qichacha_content_err_exp =  re.compile(u'登录[^\u4E00-\u9FFF]{3,20}查看更多信息|请先登录或者您没有这个权限')
re_qichacha_content_name_exp =  re.compile('')#企查查正文人名检测
re_spider_list_exp = re.compile(u'href="/firm_([^_]{0,9})_([^"]{0,40}).shtml"[\s\S]{0,500}?<span class="name">([\s\S]{0,200}?)</span>')
re_content_exp = re.compile(u'<div id="qycg_show1[^>]{0,50}>([\s\S]*?)<div class="f_l bk2">')
#检测是否是登录状态
re_status_exp = re.compile(u'仅对会员开放|登录[</a> ]{0,10}查看')

#变更项目
re_ent_alt_exp=re.compile(u'变更项目：([\s\S]*?)</span>[\s\S]*?变更日期：([\s\S]*?)</span>[\s\S]*?变更前：([\s\S]*?)</span>[\s\S]*?变更后：([\s\S]*?)</span>[\s\S]*?')
''''''
#股东信息正则编译
#re_ent_shareholder_exp=re.compile(r'text-lg">([\s\S]{0,100}?)</a>[\s\S]*?m-b-xs">([\s\S]{1,150}?)</small>(?:[\s\S]{10,200}?<span class="black-6">([\s\S]{1,150}?)</small>)?')
re_ent_shareholder_exp=re.compile(u'(<div class="clear">[\s\S]{0,100}?href="/firm[\\_]{1,2}[a-zA-Z]{1,9}[\\_]{1,2}(\w{1,40})["\.][\s\S]{0,100}?)?text-lg">([\s\S]{0,100}?)</a>[\s\S]{0,350}?m-b-xs">([\s\S]{1,150}?)</small>(?:[\s\S]{0,350}?(?<=认缴出资额：)([\s\S]{0,350}?)</span>)?(?:[\s\S]{0,350}?(?<=认缴出资时间：)([\s\S]{0,350}?)</span>)?(?:[\s\S]{0,350}?(?<=实缴出资额：)([\s\S]{0,350}?)</span>)?(?:[\s\S]{0,350}?(?<=实缴出资时间：)([\s\S]{0,350}?)</span>)?')

#主要成员
re_ent_principal_exp=re.compile(u'class="text-lg">([\s\S]{1,100})</a>([\s\S]{1,100})</small>')

#分支机构
re_ent_branch_exp = re.compile(u'class="panel-body">[\s\S]{1,300}?alt="([\s\S]{0,200}?)">([\s\S]{1,300}href="/firm[\\_]{1,2}([a-zA-Z]{1,9})[\\_]{1,2}(\w{1,40})">)?')

#经营异常
re_ent_abnormity_exp = re.compile(u'列入日期：([\s\S]*?)</span>(?:[\s\S]*?(?<=移出日期：)([\s\S]*?)</span>)?(?:[\s\S]*?(?<=作出决定机关：)([\s\S]*?)</span>)(?:[\s\S]*?(?<=列入经营异常名录原因：)([\s\S]*?)</span>)(?:[\s\S]*?(?<=移出经营异常名录原因：)([\s\S]*?)</span>)?')


def re_deal(pattern,html_doc,status=1,date_type = False):
    #re_text = re.search(pattern,html_doc)
    #print(re_text)

    re_text = pattern.search(html_doc)
    if re_text ==None:
        return None
    else:
        re_text = re_sub.sub('', re_text.group(status))
        if re_text.find('null') > 0:
            return None
        elif re_text == '':
            return None
        if date_type :
            re_text = re.sub(r'[年月/]','-',re_text)
            re_text = re.sub(r'日', '', re_text)
            re_text = re_date.search(re_text)
            if re_text ==None:
                return re_text
            re_text=re_text.group(0)
        return re_text
def re_ent_alt(html_doc):#企业变更信息
    ent_alt_list = re_ent_alt_exp.findall(html_doc)
    return  ent_alt_list
def re_ent_shareholder(html_doc):#股东信息
    ent_shareholder_list = re_ent_shareholder_exp.findall(html_doc)
    return  ent_shareholder_list
def re_ent_principal(html_doc):#主要人员
    ent_principal_list = re_ent_principal_exp.findall(html_doc)
    return  ent_principal_list
def re_ent_branch(html_doc):#分支机构
    ent_branch_list = re_ent_branch_exp.findall(html_doc)
    return ent_branch_list
def re_ent_abnormity(html_doc):#经营异常
    ent_abnormity_list = re_ent_abnormity_exp.findall(html_doc)
    return ent_abnormity_list

def re_spider_list(html_doc):#处理采集列表页
    spider_list = re_spider_list_exp.findall(html_doc)
    return spider_list
def re_Purchase_id(html_doc):#处理采购编号
    #Purchase_id_list = re_Purchase_id_exp.findall(html_doc)
    re_text = re_Purchase_id_exp.search(html_doc)

    if re_text == None:
        return None
    else:
        re_text =re_text.group(6)
        #print(re_text)
        return re_text
def re_content(html_doc):#处理正文
    #print(html_doc)
    re_text = re_content_exp.search(html_doc)
    if re_text == None:
        return None
    else:
        re_text =re_text.group(1)
        return re_text
def re_status(html_doc):#检测是否是登录状态
    re_text = re_status_exp.search(html_doc)
    if re_text == None:
        return None
    else:
        re_text =re_text.group(0)
        return re_text
def data_sub(text):#去除文本中的换行符 与 html 标签
    if text==None:
        return None
    re_text = re_sub.sub('', text)
    if re_text.find('null') > 0:
        return None
    elif re_text=='':
        return None
    #print(re_text)
    return re_text
def get_text_right(keyword,text):#在text中  取出关键词 keyword 右边文本
    keyword_site=text.find(keyword)
    if keyword_site==-1:
        return None
    return text[len(keyword)+keyword_site:]
