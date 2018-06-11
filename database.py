from sqlalchemy import create_engine, Table, Column, Integer, Unicode, Boolean, MetaData, select
import urlparse

DATABASE_NAME = 'data/crawler_realestate.sqlite'
HTML_DIR = 'data/html/'

class CrawlerDb:

	def __init__(self):
		self.connected = False

	def connect(self):

		self.engine = create_engine('sqlite:///' + DATABASE_NAME)
		self.connection = self.engine.connect()
		self.connected = True if self.connection else False
		self.metadata = MetaData()

		# Define the tables
		self.website_table = Table('website', self.metadata,
			Column('id', Integer, primary_key=True),
			Column('url', Unicode, nullable=False),
			Column('has_crawled', Boolean, default=False),
			Column('emails', Unicode, nullable=True),
		)

		# Create the tables
		self.metadata.create_all(self.engine)
		
	def enqueue(self, url, emails = None):
		if not self.connected:
			return False

		s = select([self.website_table]).where(self.website_table.c.url == url)
		res = self.connection.execute(s)
		result = res.fetchall()
		res.close()
		# If we get a result, then this url is not unique
		if len(result) > 0:
# 			print 'Duplicated: %s' % url
			return False

		args = [{'url':unicode(url)}]
		if (emails != None):
			args = [{'url':unicode(url), 'has_crawled':True, 'emails':unicode(",".join(emails))}]
		result = self.connection.execute(self.website_table.insert(), args)
		if result:
			return True
		return False
		
		
	def dequeue(self):
		if not self.connected:
			return False
		# Get the first thing in the queue
		s = select([self.website_table]).limit(1).where(self.website_table.c.has_crawled == False)
		res = self.connection.execute(s)
		result = res.fetchall()
		res.close()
		# If we get a result
		if len(result) > 0:
			# Remove from the queue ?
			# delres = self.connection.execute(self.queue_table.delete().where(self.queue_table.c.id == result[0][0]))
			# if not delres:
			# 	return False
			# Return the row
			# print result[0].url
			return result[0]
		return False
		
		
	def crawled(self, website, new_emails=None):
		if not self.connected:
			return False
		stmt = self.website_table.update() \
			.where(self.website_table.c.id==website.id) \
			.values(has_crawled=True, emails=new_emails)
		self.connection.execute(stmt)


	def get_all_emails(self):
		if not self.connected:
			return None

		s = select([self.website_table])
		res = self.connection.execute(s)
		companies = ["zinetgo-services.com","bosch-si.com","instagrampartners.com","inventateq.com","jobswitch.in","articlecatalog.com","bosch-pt.co.in","10bestseo.com","unikainfocom.in","crestaproject.com","nidmindia.com","goingsocial.ca","ads2book.com","nexevo.in","emarketeducation.in","educationtimes.com","yseo.in","learndigitalmarketing.com","testingxperts.com","australiancontractlaw.com","sitegalleria.com","schoolofdigitalmarketing.co.in","digiterati-academy.com","fuelingnewbusiness.com","electronic-city.in","indrasacademy.com","palbabban.com","skydreamconsulting.com","masiradm.com","imsolutions.co","idigitalacademy.com","seovalley.org","thoughtminds.com","oriondigital.in","cityinnovates.com","chromozomes.com","kumarsacademy.com","ultimez.com","browsermedia.agency","binarydigital360.com","renavo.com","builtinmtl.com","startupcafedigital.com","jaintechnosoft.com","fintechvalleyvizag.com","adworld-india.co.in","taxiq.in","smartechindia.com","skimbox.co","lodestarmg.com","sunhill.in","kepran.com","rainmaker-india.com","digitalcorsel.com","digitallove.in","beboldcreative.com","zestwebdesign.in","trionixglobal.com","webgen.in","sirigroups.com","sigmato.com","synx.com.au","drrudresh.com","digiverti.com","optimizeindia.com","techtrendsolutions.com","grabstance.com","jupitervidya.com","sketchcareer.com","nexgenonlinesolutions.com","bolasintelli.co.in","online24x7.in","inboundkitchen.com","pattronize.com","onlinepaidlook.com","performetris.com","panworldeducation.com","foxgloveawards.com","percoyo.com","yourseoservices.com","entrepreneurreprints.com","brandownerssummit.com","bosch-climate.in","scionacademy.com","troppusweb.com","hexalab.in","prismtechnology.in","hospity.com","crosspollen.com","access1solution.com","wonesty.com","estelle.in","erosinfotech.com","honeycombdigital.net","thesocialmediaexpert.in","bangaloremediaworks.com","panamatechnologies.com","seoconsultindia.com","maditbox.com","savanspaceinteriors.in","bangaloreseoservices.in","ucwebtechnologies.com","seeknext.com","jiffystorage.com","dgepl.com","inventussoftware.com","72-pixels.com","madgeek.in","ads-r-us.de","olivedewtechnologies.com","mvglobe.in","samrudhsolutions.com","thought-starters.com","ben-solutions.com","seodigitz.com","smwibangalore.in","itservicestalk.com","cbrainz.com","imcanny.com"]
		results = res.fetchall()
		res.close()
		email_set = set()
		x = set()
		for result in results:
			if (result.emails == None):
				continue
			for email in result.emails.split(','):
				email_set.add(email)
				url = urlparse.urlparse(result.url)
				hostname = url.hostname.split(".")
				hostname = ".".join(len(hostname[-2]) < 4 and hostname[-3:] or hostname[-2:])
				if any(hostname in s for s in companies):
					print email + ','+hostname
				x.add(email + ','+hostname)
		return email_set

	def delete(self):
		if not self.connected:
			return None
		s = self.website_table.drop(self.engine)
		self.connection.execute(s)

	def get_all_domains(self):
		if not self.connected:
			return None

		s = select([self.website_table])
		res = self.connection.execute(s)
		results = res.fetchall()
		res.close()
		domain_set = set()
		for result in results:
			if (result.url == None):
				continue
			url = urlparse.urlparse(result.url)
			hostname = url.hostname.split(".")
			# Simplistic assumeption of a domain. If 2nd last name is <4 char, then it has 3 parts eg. just2us.com.sg
			hostname = ".".join(len(hostname[-2]) < 4 and hostname[-3:] or hostname[-2:])
			domain_set.add(hostname)

		return domain_set


	def close(self):
		self.connection.close()
		

	def save_html(filename, html):
		filename = os.path.join(HTML_DIR, filename)
		file = open(filename,"w+")
		file.writelines(html)
		file.close()


	def test(self):
		c = CrawlerDb()
		c.connect()
		# c.enqueue(['a12222', '11'])
		# c.enqueue(['dddaaaaaa2', '22'])
		c.enqueue('111')
		c.enqueue('222')
		website = c.dequeue()
		c.crawled(website)
		website = c.dequeue()
		c.crawled(website, "a,b")
		print '---'
		c.dequeue()
	
	
# CrawlerDb().test()

