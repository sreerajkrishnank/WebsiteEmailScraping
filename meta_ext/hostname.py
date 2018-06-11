import re
p = '(?:http.*://)?(?P<host>[^:/ ]+).?(?P<port>[0-9]*).*'

f = open('new_1.txt','r')
for line in f:
	m = re.search(p,line)
	print str(m.group('host'))