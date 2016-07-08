import json

obj = '[[1,2,3],123,123.123,'abc',{'key1':(1,2,3),'key2':(4,5,6)}]'
encodedjson = json.loads(obj)
print repr(obj)
print encodedjson
print '1',type(obj)
print '2',type(encodedjson)
