## Meta Extraction metaext.py ##
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
    except:
        pass
 

## Organize data rmnl.py ##
f = open ("out.txt")
out_f = open ("outf.txt", 'w')
while True:
    c = f.read(1)
    if not c:
      break
    if c != '\n':
        print(c)
        out_f.write(c)
    elif c == '\n' and f.read(1) == 'h':
        print(c + 'h')
        out_f.write(c + 'h')
    else:
        continue
        
        
## Regular Expression Search regsearch.py ##
#comp = re.compile(r'(?=(.))(?:digital|marketing|marketting|social|media|facebook|advertising|advertizing|ad|google|adwords|seo|search|engine|optimisation|optimization|inbound|website|online)', flags=re.IGNORECASE)
open_f = open("outfbkup.txt")
out_f = open ("names.txt",'w')
for line in open_f:
    line = line.strip('\n')
    if re.search(r"Website development|Inbound marketing|inbound marketting|Social Media|Marketing company|SEO|Search Engine Optimisation|Google adwords|online advertising services|Facebook|marketing|Social media|marketing",line,re.IGNORECASE):
        out_f.write(line+'\n')
    else:
        print (line)

       
      
## Extract Keywords and URL final.py **
#comp = re.compile(r'(?=(.))(?:digital|marketing|marketting|social|media|facebook|advertising|advertizing|ad|google|adwords|seo|search|engine|optimisation|optimization|inbound|website|online)', flags=re.IGNORECASE)
open_f = open("names.txt")
out_f = open ("finalop.txt",'w')
for line in open_f:
    line = line.strip('\n')
    urls = re.findall('^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
    urls[0] = urls[0].rstrip("meta")
    keys = re.findall(r"Website development|Inbound marketing|inbound marketting|Social Media|Marketing company|SEO|Search Engine Optimisation|Google adwords|online advertising services|Facebook|marketing|Social media|marketing",line,re.IGNORECASE)

    out_f.write(urls[0]+" : ")
    for k in keys:
        out_f.write(k+" ")

out_f.write("\n")