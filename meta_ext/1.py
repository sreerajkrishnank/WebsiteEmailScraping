import urllib2
from lxml import etree
import re
from xml.etree.ElementTree import tostring

out_f = open ('out.txt', 'w')
url_f = open ('domains.csv')
urls = url_f.readlines()
print (urls)
j=0
for i in urls:
    urls[j]=i.rstrip("\n")
    j+=1

print (urls)

for k in urls:
    k = "http://" + k + "/"
    out_f.write (k + '\n')
    print (k)
    req = urllib2.Request(k);
    req.add_header('User-Agent','Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11')
    try:
        site = urllib2.urlopen(req).read()
        tree = etree.HTML( site )
        meta = tree.xpath( "//meta" )
        for i in meta:
            w = etree.tostring( i )
            w = w.decode("utf-8")
            w.strip('\n')
            out_f.write (w)
        out_f.write("\n")
        out_f.flush()
    except:
        pass