# -*- coding: utf-8 -*-
import re
re_reg_code = re.compile(u'[^()（）]{1,2}注册号：([\s\S]{0,30}?)</li>')
re_org_code=re.compile(u'[^()（）]{1,2}组织机构代码：([\s\S]{0,60}?)</li>')
re_uniform_code=re.compile(u'[^()（）]{1,2}统一社会信用代码：([\s\S]{0,60}?)</li>')
#机构名称  不存在
re_org_type=re.compile(u'[^()（）]{1,2}公司类型：([\s\S]{0,60}?)</li>')
#机构类型
re_est_date=re.compile(u'[^()（）]{1,2}成立日期：(\d{4}年\d{1,2}月\d{1,2}日|[\s\S]{0,50}?</li>)')
#注册日期 不存在
re_issue_date=re.compile(u'[^()（）]{1,2}发照日期：([\s\S]{0,50}?)</li>')
#approve_date 核准日期不存在
re_op_from=re.compile(u'[^()（）]{1,2}营业期限：([\s\S]{0,50}?)(?=至)')
#营业期限自
re_op_to=re.compile(u'[^()（）]{1,2}营业期限：[\s\S]{0,50}?至([\s\S]{0,50}?)</li>')
#营业期限至

#cancel_date作废日期不存在
re_corp_rpt=re.compile(u'[^()（）]{1,2}法定代表：([\s\S]{0,200}?)(?=</a>)')
#法定代表人
re_reg_cap=re.compile(u'[^()（）]{1,2}注册资本：([\s\S]{0,60}?)(?=</li>)')
re_reg_state=re.compile(u'[^()（）]{1,2}经营状态：([\s\S]{0,60}?)(?=</li>)')
#reg_state
re_reg_org=re.compile(u'[^()（）]{1,2}登记机关：([\s\S]{0,100}?)(?=</li>)')
#工商登记机关 reg_org

#authority 组代颁证机构  不存在
re_address=re.compile(u'[^()（）]{1,2}企业地址：([\s\S]{1,300}?)((?=查看地图)|</li>)')
re_address_1=re.compile(u'[^()（）]{1,2}企业地址：([\s\S]{1,300}?)(?=查看地图)')
re_op_scope=re.compile(u'[^()（）]{1,2}经营范围：([\s\S]*?)(?=</section>)')

re_org_english_name=re.compile(u'[^()（）]{1,2}英\s?文\s?名：([\s\S]{0,200}?)(?=</li>)')
re_industry=re.compile(u'[^()（）]{1,2}所属行业：([\s\S]{0,100}?)(?=</li>)')
re_org_scale=re.compile(u'[^()（）]{1,2}公司规模：([\s\S]{0,100}?)(?=</li>)')
re_org_detail=re.compile(u'[^()（）]{1,2}公司简介：([\s\S]*?)(?=</section>)')
#source  来源  不存在
#location  地区不存在
#reg_cap_type  资本类型  不存在
#investor  投资人不存在
#revoke_date  吊销时间不存在
















location_mapping = {
    u'FJ': '350000',
    u'YN': '530000',
    u'HUB': '420000',
    u'SH': '310000',
    u'HEN': '410000',
    u'NX': '640000',
    u'SD': '370000',
    u'JL': '220000',
    u'HLJ': '230000',
    u'GD': '440000',
    u'TJ': '120000',
    u'HB': '130000',
    u'SC': '510000',
    u'SAX': '610000',
    u'NMG': '150000',
    u'XZ': '540000',
    u'QH': '630000',
    u'LN': '210000',
    u'SX': '140000',
    u'ZJ': '330000',
    u'BJ': '110000',
    u'GS': '620000',
    u'GZ': '520000',
    u'JX': '360000',
    u'AH': '340000',
    # u'国家工商行政管理总局': '100000',
    u'JS': '320000',
    u'HUN': '430000',
    u'XJ': '650000',
    u'HAIN': '460000',
    u'CQ': '500000',
    u'CN': '990000',
    u'GX': '450000'}
