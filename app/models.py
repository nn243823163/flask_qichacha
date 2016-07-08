#coding:utf-8
from peewee import *

db = PostgresqlDatabase(
    database='data_warehouse',
    user='data_user',
    password='data_user',
    host='123.56.153.35',
    port=5432
)

class EntAbnormity(Model):

    record_pk = IntegerField(primary_key=True)               #如果是主键一定要加primary_key=True
    ent_pk = UUIDField()
    op_time = DateTimeField()
    record_date = DateField()
    removal_date = DateField()
    decision_org = CharField()
    record_reason = CharField()
    removal_reason = CharField()
    order_code = IntegerField()

    class Meta:

        database = db                                        #要连接的数据库
        db_table = 'ent_abnormity'              #要映射的数据表,名称与原表一致
        schema = 'data_warehouse2'

class EntAlt(Model):

    record_pk = IntegerField(primary_key=True)               #如果是主键一定要加primary_key=True
    ent_pk = UUIDField()
    approve_date = DateField()
    op_time = DateTimeField()
    alt_item = CharField()
    alt_item_en_h = TextField()
    alt_item_en_q = TextField()


    class Meta:

        database = db                                        #要连接的数据库
        db_table = 'ent_alt'              #要映射的数据表,名称与原表一致
        schema = 'data_warehouse2'

class EntBranch(Model):

    record_pk = IntegerField(primary_key=True)               #如果是主键一定要加primary_key=True
    ent_pk = UUIDField()
    branch_pk = UUIDField()
    reg_code = CharField()
    op_time = DateTimeField()
    branch_name = CharField()
    authority = CharField()
    op_time = DateTimeField()
    order_code = IntegerField()


    class Meta:

        database = db                                        #要连接的数据库
        db_table = 'ent_branch'              #要映射的数据表,名称与原表一致
        schema = 'data_warehouse2'


class EntPrincipal(Model):

    record_pk = IntegerField(primary_key=True)               #如果是主键一定要加primary_key=True
    ent_pk = UUIDField()
    name = CharField()
    position = CharField()
    op_time = DateTimeField()
    order_code = IntegerField()

    class Meta:

        database = db                                        #要连接的数据库
        db_table = 'ent_principal'              #要映射的数据表,名称与原表一致
        schema = 'data_warehouse2'



class EntShareholder(Model):
    record_pk = IntegerField(primary_key=True)  # 如果是主键一定要加primary_key=True
    ent_pk = UUIDField()
    shareholder = CharField()
    id_type = CharField()
    id_num = CharField()
    shareh_pk = UUIDField()
    shareh_type = CharField()
    invest_amount = CharField()
    invest_date = CharField()
    op_time = DateTimeField()
    subscribe_invest_amount = CharField()
    subscribe_invest_date = CharField()

    class Meta:
        database = db  # 要连接的数据库
        db_table = 'ent_shareholder'  # 要映射的数据表,名称与原表一致
        schema = 'data_warehouse2'


class OrgInfo(Model):
    org_id = UUIDField(primary_key=True)  # 如果是主键一定要加primary_key=True
    reg_code = CharField()
    org_code = CharField()
    uniform_code = CharField()
    org_name = CharField()
    org_type = CharField()
    est_date = DateField()
    reg_date = DateField()
    issue_date = DateField()
    approve_date = DateField()
    op_from = DateField()
    op_to = DateField()
    cancel_date = DateField()
    corp_rpt = CharField()
    reg_cap = FloatField()
    reg_state = CharField()
    op_time = DateTimeField()
    reg_org = CharField()
    authority = CharField()
    address = CharField()
    op_scope = TextField()
    source = CharField()
    location = CharField()
    reg_cap_type = CharField()
    investor = CharField()
    revoke_date = DateField()
    saic_id = CharField()
    trends_time = DateTimeField()
    org_english_name = CharField()
    industry = CharField()
    org_scale = CharField()
    org_detail = TextField()

    class Meta:
        database = db  # 要连接的数据库
        db_table = 'org_info'  # 要映射的数据表,名称与原表一致
        schema = 'data_warehouse2'

class OrgInfo2(Model):
    org_id = UUIDField(primary_key=True)  # 如果是主键一定要加primary_key=True
    org_name = CharField()
    address = CharField()
    tag = IntegerField()

    class Meta:
        database = db  # 要连接的数据库
        db_table = 'org_info2'  # 要映射的数据表,名称与原表一致
        schema = 'data_warehouse2'
