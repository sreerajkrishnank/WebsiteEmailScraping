import re
open_f = open("names.txt")
out_f = open ("finalop.txt",'w')
for line in open_f:
    line = line.strip('\n')
    urls = re.findall('^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', line)
    urls[0] = urls[0].rstrip("meta")
    keys = re.findall(r"Website development|Inbound marketing|inbound marketting|Social Media|Marketing company|SEO|Search Engine Optimisation|Google adwords|online advertising services|marketing|Social media|marketing",line,re.IGNORECASE)

    out_f.write(urls[0])
    # for k in keys:
    #     out_f.write(k+" ")
    out_f.write("\n")
    out_f.flush()