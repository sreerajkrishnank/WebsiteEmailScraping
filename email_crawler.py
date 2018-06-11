from settings import LOGGING
import logging, logging.config
import urllib, urllib2
import re, urlparse
import traceback
from database import CrawlerDb
from googleapiclient.discovery import build
import pprint

my_api_key = 'API_KEY'
my_cse_id = 'CSE_ID'

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

for i in range(1,MAX_SEARCH_RESULTS,10):
	results = google_search(sys.stdin, my_api_key, my_cse_id, num=1,start=i)
	for result in results:
		print result['link']
		

	# for page_index in range(0, MAX_SEARCH_RESULTS, 10):
	# 	query = {'q': keywords}
	# 	url = 'https://www.google.com/search?' + urllib.urlencode(query) + '&start=' + str(page_index)
	# 	data = retrieve_html(url)
	# 	# 	print("data: \n%s" % data)
	# 	for url in google_url_regex.findall(data):
	# 		db.enqueue(unicode(url))
	# 	for url in google_adurl_regex.findall(data):
	# 		db.enqueue(unicode(url))

	# Step 2: Crawl each of the search result
	# We search till level 2 deep
	# while (True):
	# 	# Dequeue an uncrawled webpage from db
	# 	uncrawled = db.dequeue()
	# 	if (uncrawled == False):
	# 		break
	# 	if (getHostName(uncrawled.url) in ['zomato.com','naukri.com', 'facebook.com']):
	# 		db.crawled(uncrawled, 'test@test.com');
	# 	email_set = find_emails_2_level_deep(uncrawled.url)
	# 	if (len(email_set) > 0):
	# 		db.crawled(uncrawled, ",".join(list(email_set)))
	# 	else:
	# 		db.crawled(uncrawled, None)

def retrieve_html(url):
	"""
	Crawl a website, and returns the whole html as an ascii string.

	On any error, return.
	"""
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Just-Crawling 0.1')
	request = None
	status = 0
	try:
		logger.info("Crawling %s" % url)
		request = urllib2.urlopen(req)
	except urllib2.URLError, e:
		logger.error("Exception at url: %s\n%s" % (url, e))
	except urllib2.HTTPError, e:
		status = e.code
	except Exception, e:
		return
	if status == 0:
		status = 200

	try:
		data = request.read()
	except Exception, e:
		return

	return str(data)


def find_emails_2_level_deep(url):
	"""
	Find the email at level 1.
	If there is an email, good. Return that email
	Else, find in level 2. Store all results in database directly, and return None
	"""
	html = retrieve_html(url)
	email_set = find_emails_in_html(html)

	if (len(email_set) > 0):
		# If there is a email, we stop at level 1.
		print email_set
		return email_set

	else:
		# No email at level 1. Crawl level 2
		logger.info('No email at level 1.. proceeding to crawl level 2')

		link_set = find_links_in_html_with_same_hostname(url, html)
		for link in link_set:
			# Crawl them right away!
			# Enqueue them too
			html = retrieve_html(link)
			if (html == None):
				continue
			email_set = find_emails_in_html(html)
			print email_set
			db.enqueue(link, list(email_set))
			# if len(email_set) != 0:
			# 	break;

		# We return an empty set
		return set()


def find_emails_in_html(html):
	if (html == None):
		return set()
	email_set = set()
	for email in email_regex.findall(html):
		email_set.add(email)
	return email_set


def find_links_in_html_with_same_hostname(url, html):
	"""
	Find all the links with same hostname as url
	"""
	if (html == None):
		return set()
	url = urlparse.urlparse(url)
	links = url_regex.findall(html)
	link_set = set()
	for link in links:
		if link == None:
			continue
		try:
			link = str(link)
			if link.startswith("/"):
				link_set.add('http://'+url.netloc+link)
			elif link.startswith("http") or link.startswith("https"):
				if (link.find(url.netloc)):
					link_set.add(link)
			elif link.startswith("#"):
				continue
			else:
				link_set.add(urlparse.urljoin(url.geturl(),link))
		except Exception, e:
			pass

	return link_set




if __name__ == "__main__":
	import sys
	try:
		arg = sys.argv[1].lower()
		if (arg == '--emails') or (arg == '-e'):
			# Get all the emails and save in a CSV
			logger.info("="*40)
			logger.info("Processing...")
			emails = db.get_all_emails()
			logger.info("There are %d emails" % len(emails))
			file = open(EMAILS_FILENAME, "w+")
			file.writelines("\n".join(emails))
			file.close()
			logger.info("All emails saved to ./data/emails.csv")
			logger.info("="*40)
		elif (arg == '--domains') or (arg == '-d'):
			# Get all the domains and save in a CSV
			logger.info("="*40)
			logger.info("Processing...")
			domains = db.get_all_domains()
			logger.info("There are %d domains" % len(domains))
			file = open(DOMAINS_FILENAME, "w+")
			file.writelines("\n".join(domains))
			file.close()
			logger.info("All domains saved to ./data/domains.csv")
			logger.info("="*40)
		else:
			# Crawl the supplied keywords!
			crawl(arg)

	except KeyboardInterrupt:
		logger.error("Stopping (KeyboardInterrupt)")
		sys.exit()
	except Exception, e:
		logger.error("EXCEPTION: %s " % e)
		traceback.print_exc()
