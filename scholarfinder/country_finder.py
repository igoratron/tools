#!/bin/python2.7
import re
import urllib2
import urllib
import codecs
import lxml.html
from time import sleep
import random 

def checkACM(title):
	title = "".join(["\"", title,"\""])
	url = "http://dl.acm.org/results.cfm"
	
	http_header = {
                "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.46 Safari/535.11",
                "Accept" : "text/xml,application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,text/png,*/*;q=0.5",
                "Accept-Language" : "en-us,en;q=0.5",
                "Accept-Charset" : "ISO-8859-1",
                "Content-type": "application/x-www-form-urlencoded",
                }
	
	req = urllib2.Request(url, urllib.urlencode({"query": title}), http_header)
	tree = lxml.html.parse(codecs.EncodedFile(urllib2.urlopen(req), "utf-8")).getroot()

	if(tree.xpath("/html/body/div[1]/table/tr[2]/td/div/table/tr/td/p[2]/span/font")):
		print title, "could not be found in ACM"
		return False
	else:
		print title, "found in ACM"
		acm_title = tree.xpath("title")

		if title[1:-1].lower() == acm_title.lower():
			print "There is a title mismatch"
			print "ACM's", acm_title
			print "Original's", title[1:-1]
			ok = raw_input("Proceed? ")
			if ok != "y":
				return False

		link = tree.xpath("/html/body/div[1]/table/tr[3]/td/table/tr[3]/td[2]/table/tr[2]/td[2]/table/tr[1]/td/a/@href")[0]
		url = "".join(["http://dl.acm.org/",link])
		http_header.pop("Content-type");
		req = urllib2.Request(url=url, headers=http_header)
		tree = lxml.html.parse(codecs.EncodedFile(urllib2.urlopen(req), "utf-8")).getroot()
		rows = tree.xpath("//*[@id=\"divmain\"]/table[1]/tr/td[1]/table[2]/tr")
		
		for i, row in enumerate(rows):
			author = row.xpath(".//td[2]/a")[0].text.encode("utf-8")
			university = row.xpath(".//small")[0].text.encode("utf-8")
			contacts[author] = university
		
		return True

publication_regex = re.compile("\(\d\d\d\d\)\.?(?:\s*(?:\w+ )*[A-Z]\w*,?(?:\s?[A-Z]\.)+(?:[;,]| &)?)+,?\s+(.+?)[,.] (?:[A-Z]|\d)", re.UNICODE)

with open("publications.txt","r") as f:
	publications = f.readlines()

contacts = {}
titles = []
failed = 0
failedTitles = []

for i, line in enumerate(publications):
	match = publication_regex.match(line)
	if(match):
		titles.append(match.group(1))
	else:
		failed += 1
		failedTitles.append(line)

print "Found ", len(titles), "valid titles.", failed, "failed"

failed = 0

#for i, title in enumerate(titles):
#	if not checkACM(title):
#		failed += 1
#		failedTitles.append(title)
#	sleep(random.randint(1000, 5000)

with open("contacts.txt","w") as f:
	for name in contacts:
		print name, "-", contacts[name]
		f.write("".join([name, " - ", contacts[name],"\n"]))

with open("failed.txt","w") as f:
	for i, line in enumerate(failedTitles):
		f.write(line + "\n")

print "Got", len(contacts), "authors.", failed, "papers couldn't be found"
