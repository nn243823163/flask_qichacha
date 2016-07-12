# -*- coding: utf-8 -*-
from flask import *
from .models import *
from werkzeug.routing import BaseConverter
from qichacha_spider import qichacha_spider_list,qichacha_spider_content

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

class RegexConverter(BaseConverter):
    def __init__(self,url_map,*items):
        super(RegexConverter,self).__init__(url_map)
        self.regex = items[0]

def init_views(app):
    app.url_map.converters['regex'] = RegexConverter

    # @app.route('/user/<regex("[a-z]{3}"):user_id>')
    # def user(user_id):
    #     return 'user id is %s ' %user_id

    @app.route('/',methods=['GET','POST'])
    def login():
        from .forms import LoginForm
        form =  LoginForm()
        info_from_db = u'等待查询'
        info_from_spider = u'等待查询'
        status = u'等待查询'
        name = u'请输入要查询内容'

        if request.method=='POST':
            #清空缓存表
            # query = Tweet.delete().where(Tweet.creation_date < one_year_ago)
            # query.execute()
            try:
                query = OrgInfo2.delete().where(OrgInfo2.tag<3)
                query.execute()
            except:
                print(u'没有数据')

            #查询企业基本信息

            name = form.username.data
            json_list, status = qichacha_spider_list(name)
            if status == None:
                status = u'查询成功'
            #转码并提出主要信息
            try:
                json_list = json_list.encode("utf-8")
                json_list = json.loads(json_list)
                json_list = json_list['results']
            except:
                print('查找失败')
                status = u'查找失败'
                return render_template('login.html',form = form ,info_from_spider=info_from_spider, select_name=name,info_from_db=info_from_db,status=status)


            print json_list
            import hashlib
            for json_info in json_list:
                #uid转化为MD5并进行查询
                uid = json_info['uid']
                uid = hashlib.md5(str(uid).encode('utf-8')).hexdigest()
                #org_info中进行查询，有信息返回表中信息，没有信息则调用爬虫函数
                try:
                    org_info = OrgInfo.get(OrgInfo.org_id==uid)
                    tag = 1
                    #存入缓存库，org_info2用来缓存数据，向页面显示
                    org_info2 = OrgInfo2(org_id=uid,tag=tag,org_name=org_info.org_name,address=org_info.address)
                    org_info2.save(force_insert=True)
                    # org_info.delete_instance()
                except Exception as a:
                    tag = 2

                    #从爬虫抓取信息
                    json_list1 , status= qichacha_spider_content(json_info['uid'],json_info['area'],json_info['name'])
                    if status == None:
                        status = u'查询成功'
                    json_list1 = json.loads(json_list1)
                    json_list2 = json_list1['org_info']
                    print '222222222',json_list1
                    #存入缓存库
                    org_info2 = OrgInfo2(org_id=uid,tag=2,org_name=json_list2['org_name'],address=json_list2['address'])
                    org_info2.save(force_insert=True)
                    print('33333333')
                    #入库
                    try:
                        ent_branch_json = json_list1['ent_branch']
                        print '1',ent_branch_json
                        if ent_branch_json != None:
                            for ent_branch_json1 in ent_branch_json:
                                ent_branch = EntBranch(ent_pk=ent_branch_json1['ent_pk'],branch_pk=ent_branch_json1['branch_pk'],ent_area=ent_branch_json1['ent_area'],branch_name=ent_branch_json1['branch_name'],ent_uid=ent_branch_json1['ent_uid'],order_code=ent_branch_json1['order_code'])
                                ent_branch.save()
                                print '1,succed'
                        ent_principal_json = json_list1['ent_principal']
                        print '2',ent_principal_json
                        if ent_principal_json != None:
                            for ent_principal_json1 in ent_principal_json:
                                ent_principal = EntPrincipal(ent_pk=ent_principal_json1['ent_pk'],name=ent_principal_json1['ent_name'],position=ent_principal_json1['ent_position'],order_code=ent_principal_json1['order_code'])
                                ent_principal.save()
                                print '2,succed'
                        ent_abnormity_json = json_list1['ent_abnormity']
                        print '3',ent_abnormity_json
                        if ent_abnormity_json != None:
                            for ent_abnormity_json1 in ent_abnormity_json:
                                ent_abnormity = EntAbnormity(record_date=ent_abnormity_json1['record_date'], removal_date=ent_abnormity_json1['removal_date'],  removal_reason=ent_abnormity_json1['removal_reason'], decision_org=ent_abnormity_json1['decision_org'], record_reason=ent_abnormity_json1['record_reason'], ent_pk=ent_abnormity_json1['ent_pk'], order_code=ent_abnormity_json1['order_code'] )
                                ent_abnormity.save()
                                print '3,succed'
                        ent_alt_json = json_list1['ent_alt']
                        print '4',ent_alt_json
                        if ent_alt_json != None:
                            for ent_alt_json1 in ent_alt_json:
                                ent_alt = EntAlt(approve_date=ent_alt_json1['approve_date'],alt_item=ent_alt_json1['alt_item'],alt_item_en_h=ent_alt_json1['alt_item_en_h'],alt_item_en_q=ent_alt_json1['alt_item_en_q'],ent_pk=ent_alt_json1['ent_pk'])
                                ent_alt.save()
                                print '4,succed'
                        org_info_json = json_list1['org_info']
                        print '5',org_info_json
                        if org_info_json != None:
                            #正式上线将OrgInfoTest改为OrgInfo
                            #删除已经存在的信息，进行刷新数据
                            # try:
                            #     org_info_delete = OrgInfoTest.get(OrgInfoTest.org_id==uid)
                            #     org_info_delete.delete_instance()
                            # except:
                            #     print '这个uid对应数据不存在'
                            #入库
                            org_info_save =  OrgInfo(org_id=uid,reg_code=org_info_json['reg_code'],org_code=org_info_json['org_code'],uniform_code=org_info_json['uniform_code'],org_type=org_info_json['org_type'],est_date=org_info_json['est_date'],issue_date=org_info_json['issue_date'],op_from=org_info_json['op_from'],op_to=org_info_json['op_to'],corp_rpt=org_info_json['corp_rpt'],reg_cap=org_info_json['reg_cap'],reg_state=org_info_json['reg_state'],reg_org=org_info_json['reg_org'],address=org_info_json['address'],op_scope=org_info_json['op_scope'],org_english_name=org_info_json['org_english_name'],industry=org_info_json['industry'],org_scale=org_info_json['org_scale'],org_detail=org_info_json['org_detail'],org_name=org_info_json['org_name'],location=org_info_json['location'])
                            # org_info_save = OrgInfoTest(org_id=org_info_json['org_id'],reg_code=org_info_json['reg_code'])
                            org_info_save.save(force_insert=True)
                            print '5,succed'
                        ent_shareholder_json = json_list1['ent_shareholder']
                        if ent_shareholder_json != None:
                            for ent_shareholder_json1 in ent_shareholder_json:
                                ent_shareholder = EntShareholder(shareh_pk=ent_shareholder_json1['shareh_pk'],shareholder=ent_shareholder_json1['shareholder'],shareh_type=ent_shareholder_json1['shareh_type'],subscribe_invest_amount=ent_shareholder_json1['subscribe_invest_amount'],subscribe_invest_date=ent_shareholder_json1['subscribe_invest_date'],invest_amount=ent_shareholder_json1['invest_amount'],invest_date=ent_shareholder_json1['invest_date'],ent_pk=ent_shareholder_json1['ent_pk'])
                                ent_shareholder.save()
                            print '6',ent_shareholder_json
                            pass
                    except Exception as a:
                        print(u'入库出错')
                        print a

                info_from_db = OrgInfo2.select().where(OrgInfo2.tag==1)
                info_from_spider = OrgInfo2.select().where(OrgInfo2.tag==2)

        return render_template('login.html',form = form ,info_from_spider=info_from_spider, select_name=name,info_from_db=info_from_db,status=status)

    # @app.route('/get/')
    # def get():
    #     cmd1 = EntAlt.get(EntAlt.record_pk==7994497).alt_item
    #     cmd2 = EntAbnormity.get(EntAbnormity.record_pk==1).decision_org
    #     cmd3 = EntBranch.get(EntBranch.record_pk==311).branch_name
    #     cmd4 = EntShareholder.get(EntShareholder.record_pk==2719628).shareholder
    #     cmd5 = EntPrincipal.get(EntPrincipal.record_pk==25230372).name
    #     cmd6 = OrgInfo.get(OrgInfo.reg_code==3570).org_type
    #
    #     return render_template('get.html',cmd=cmd2)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'),404
