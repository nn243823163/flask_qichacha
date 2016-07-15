#coding:utf-8
from peewee import *
import peewee

db = PostgresqlDatabase(
    database='marketbox',
    user='data_server',
    password='data_server',
    host='10.172.238.195',
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
    par_no = IntegerField()
    class Meta:
        database = db                                        #要连接的数据库
        db_table = 'temp_ent_abnormality'              #要映射的数据表,名称与原表一致
        schema = 'data_warehouse'
    def save(self,force_insert=False,only=None):
        try:
            super(EntAbnormity, self).save(force_insert=True, only=only)
        except peewee.DatabaseError as e:
            print('Datebaseerror:', e)
            db.rollback()
            # db_pg.close()
            return None

class EntAlt(Model):
    record_pk = IntegerField(primary_key=True)               #如果是主键一定要加primary_key=True
    ent_pk = UUIDField()
    approve_date = DateField()
    op_time = DateTimeField()
    alt_item = CharField()
    alt_item_en_h = TextField()
    alt_item_en_q = TextField()
    par_no = IntegerField()
    class Meta:
        database = db                                        #要连接的数据库
        db_table = 'temp_ent_alt'              #要映射的数据表,名称与原表一致
        schema = 'data_warehouse'
    def save(self,force_insert=False,only=None):
        try:
            super(EntAlt, self).save(force_insert=True, only=only)
        except peewee.DatabaseError as e:
            print('Datebaseerror:', e)
            db.rollback()
            # db_pg.close()
            return None

class EntBranch(Model):
    record_pk = IntegerField(primary_key=True)               #如果是主键一定要加primary_key=True
    ent_pk = UUIDField()
    branch_pk = UUIDField()
    reg_code = CharField()
    op_time = DateTimeField()
    branch_name = CharField()
    authority = CharField()
    order_code = IntegerField()
    # ent_area = CharField()
    # ent_uid = CharField()
    class Meta:
        database = db                                        #要连接的数据库
        db_table = 'temp_ent_branch'              #要映射的数据表,名称与原表一致
        schema = 'data_warehouse'
    def save(self,force_insert=False,only=None):
        try:
            super(EntBranch, self).save(force_insert=True, only=only)
        except peewee.DatabaseError as e:
            print('Datebaseerror:', e)
            db.rollback()
            # db_pg.close()
            return None

class EntPrincipal(Model):
    record_pk = IntegerField(primary_key=True)               #如果是主键一定要加primary_key=True
    ent_pk = UUIDField()
    name = CharField()
    position = CharField()
    op_time = DateTimeField()
    order_code = IntegerField()
    par_no = IntegerField()
    class Meta:
        database = db                                        #要连接的数据库
        db_table = 'temp_ent_principal'              #要映射的数据表,名称与原表一致
        schema = 'data_warehouse'
    def save(self,force_insert=False,only=None):
        try:
            super(EntPrincipal, self).save(force_insert=True, only=only)
        except peewee.DatabaseError as e:
            print('Datebaseerror:', e)
            db.rollback()
            # db_pg.close()
            return None

class OrgUuid(Model):
    pk = IntegerField(primary_key=True)               #如果是主键一定要加primary_key=True
    org_id = UUIDField()
    org_name = CharField()
    op_time = DateTimeField()
    class Meta:
        database = db                                        #要连接的数据库
        db_table = 'temp_org_uuid'              #要映射的数据表,名称与原表一致
        schema = 'data_warehouse'
    def save(self,force_insert=False,only=None):
        try:
            super(OrgUuid, self).save(force_insert=True, only=only)
        except peewee.DatabaseError as e:
            print('入库出错:', e)
            db.rollback()
            # db_pg.close()
            return None

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
    par_no = IntegerField()
    class Meta:
        database = db  # 要连接的数据库
        db_table = 'temp_ent_shareholder'  # 要映射的数据表,名称与原表一致
        schema = 'data_warehouse'
    def save(self,force_insert=False,only=None):
        try:
            super(EntShareholder, self).save(force_insert=True, only=only)
        except peewee.DatabaseError as e:
            print('Datebaseerror:', e)
            db.rollback()
            # db_pg.close()
            return None

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
    # corp_rpt = CharField()
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
        db_table = 'temp_org_info'  # 要映射的数据表,名称与原表一致
        schema = 'data_warehouse'
    def save(self,force_insert=False,only=None):
        try:
            super(OrgInfo, self).save(force_insert=True, only=only)
        except peewee.DatabaseError as e:
            print('Datebaseerror:', e)
            db.rollback()
            # db_pg.close()
            return None

# class OrgInfo2(Model):
#     org_id = UUIDField(primary_key=True)  # 如果是主键一定要加primary_key=True
#     org_name = CharField()
#     address = CharField()
#     tag = IntegerField()
#
#     class Meta:
#         database = db  # 要连接的数据库
#         db_table = 'org_info2'  # 要映射的数据表,名称与原表一致
#         schema = 'data_warehouse'
