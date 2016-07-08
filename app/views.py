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


    @app.route('/index1/')
    def index1():
        # abort(404)
        response = make_response(render_template('index.html',tittle = 'welcome1'))
        response.set_cookie('username','')
        return response


    @app.route('/index')
    @app.route('/nanann/')
    def index():
        return 'nn'



    @app.route('/user/<regex("[a-z]{3}"):user_id>')
    def user(user_id):
        return 'user id is %s ' %user_id


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
            query = OrgInfo2.delete().where(OrgInfo2.tag<3)
            query.execute()

            #查询企业基本信息

            name = form.username.data
            json_list, status = qichacha_spider_list(name)
            if status == None:
                status = u'查询成功'
            #转码并提出主要信息
            json_list = json_list.encode("utf-8")
            json_list = json.loads(json_list)
            json_list = json_list['results']
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
                    #org_info2用来缓存数据，向页面显示
                    org_info2 = OrgInfo2(org_id=uid,tag=tag,org_name=org_info.org_name,address=org_info.address)
                    org_info2.save(force_insert=True)
                except Exception as a:
                    tag = 2

                    #从爬虫抓取信息
                    json_list1 , status1= qichacha_spider_content(json_info['uid'],json_info['area'],json_info['name'])
                    json_list1 = json.loads(json_list1)
                    json_list1 = json_list1['org_info']
                    print '222222222',json_list1
                    org_info2 = OrgInfo2(org_id=uid,tag=2,org_name=json_list1['org_name'],address=json_list1['address'])
                    org_info2.save(force_insert=True)
                    print('33333333')

                info_from_db = OrgInfo2.select().where(OrgInfo2.tag==1)
                info_from_spider = OrgInfo2.select().where(OrgInfo2.tag==2)

        return render_template('login.html',form = form ,info_from_spider=info_from_spider, select_name=name,info_from_db=info_from_db,status=status)


    @app.route('/get/')
    def get():
        cmd1 = EntAlt.get(EntAlt.record_pk==7994497).alt_item
        cmd2 = EntAbnormity.get(EntAbnormity.record_pk==1).decision_org
        cmd3 = EntBranch.get(EntBranch.record_pk==311).branch_name
        cmd4 = EntShareholder.get(EntShareholder.record_pk==2719628).shareholder
        cmd5 = EntPrincipal.get(EntPrincipal.record_pk==25230372).name
        cmd6 = OrgInfo.get(OrgInfo.reg_code==3570).org_type

        return render_template('get.html',cmd=cmd2)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'),404
