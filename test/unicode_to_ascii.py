#coding:utf-8
import unicodedata
s = u"Marek Cech"   #(u表示是unicode而非 ascii码，不加报错！)
line = unicodedata.normalize('NFKD',s).encode('ascii','ignore')
print line