import re
open_f = open("outf.txt")
out_f = open ("names.txt",'w')
for line in open_f:
    line = line.strip('\n')
    if re.search(r"Website development|Inbound marketing|inbound marketting|Social Media|Marketing company|SEO|Search Engine Optimisation|Google adwords|online advertising services|marketing|Social media|marketing",line,re.IGNORECASE):
        out_f.write(line+'\n')
        out_f.flush()
    else:
        print (line)