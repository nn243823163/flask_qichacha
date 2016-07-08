from app.models import *


cmd6 = OrgInfo.get(OrgInfo.reg_code==331100000064575).org_type
print(cmd6)