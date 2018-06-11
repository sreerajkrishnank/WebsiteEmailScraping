#!/usr/bin/python
import requests
import time
import sys, getopt
import json
import clearbit
import random

keys = ["CLEARBIT_KEY"]
f = open('finalopemails.txt','r')

for line in f:
	line = line.strip('\n')
	try:
		print line
		clearbit.key = random.choice(keys)
		data = clearbit.Prospector.search(email=line,stream=True)
		fHeaders = {'content-type': "application/json"}
		firebaseUrl = "https://himalayan-base.firebaseio.com/" + line +".json"
		fResponse = requests.request("PATCH", firebaseUrl, data=json.dumps(data), headers=fHeaders)
		f2 = open(line+'.json','w')
		f2.write(json.dumps(data))
		f2.close()
	except Exception as inst:
		print inst
		pass




# lastTrade = 0
# headers = {'referer': "https//opentrade.in/publisher/Ursa%20Major/",'cache-control': "no-cache"}
# timestamp = str(int(round(time.time() / 100000)*100000000))
# idMap = {"Pavo" :110,"Carina":93,"Castor":109,"Deneb":108,"Libra" :107,"Bellatrix":106,"Altair":105,"Polaris" :104,"Eridannus":101,"Auriga":98,"Ara":96,"Cetus":95,"Orion":75,"Cygnus":63,"Scorpius":62,"Lynx":79,"Gemini":74,"Corvus":73,"Draconis":71,"Aquaris":70,"Taurus":69,"Cassiopeia":67,"Leo":65,"Ursa major":64,"Capricornus":76,"Canis major":68,"Columba":66,"Aquila":92,"Perseus":91,"Alhena":90,"Kiana":88,"Virgo":84,"Nova":81,"Andromeda":60,"Hydra":77}
# for key, value in idMap.iteritems():
# 	url = "https://opentrade.in/publisher/api/new_notification/"+ str(value)
# 	print firebaseUrl
# 	try:
# 		querystring = {"last":lastTrade}
# 		response = requests.request("GET", url, headers=headers, params=querystring)
		
# 		print fResponse.text
# 	except Exception as inst:
# 		print inst
# 		print "some exception"

