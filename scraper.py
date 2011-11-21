#!/bin/python2.7

import urllib2
import codecs
import sys
from lxml import etree

ao = u"\u00e5".encode("utf-8")
ae = u"\u00e4".encode("utf-8")
oe = u"\u00f6".encode("utf-8")

class Word():
	gender = ""
	word = ""
	definition = ""
	declension = ()
	def __str__(self):
		ret = "%(gender)s %(word)s -- %(definition)s\n" % {"gender":self.gender, "word": self.word, "definition": self.definition}
		ret += " ".join(self.declension)
		return ret	

def getDefinition(word):
	url = "".join(["http://en.wiktionary.org/wiki/",word])
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	headers = { 'User-Agent' : user_agent, 'Content-Type' : "charset=UTF-8" }
	req = urllib2.Request(url=url, headers=headers)
	html = codecs.EncodedFile(urllib2.urlopen(req), "utf-8")
	tree = etree.HTML(html.read())

	w = Word()

	gender = tree.xpath("//span[@id='Swedish']/../following-sibling::p/span/i/child::text()")
	if gender[0] == "c":
		w.gender = "en"
	else:
		w.gender = "ett"
	
	w.word = word
	
	definition = tree.xpath("//span[@id='Swedish']/../following-sibling::ol[1]/li[1]/child::node()[not(ancestor-or-self::dl)]/descendant-or-self::text()")
	w.definition = "".join(definition).rstrip()

	declension = tree.xpath("//span[@id='Swedish']/../following-sibling::div[@class='NavFrame'][1]/div[@class='NavContent']/table/tr[3]/td")
	w.declension = tuple([d.xpath("string()").encode("utf-8") for d in declension])

	return w

words = [ao+"r", "kapitel", "fru", "man", "ord", "familj", "flicka", "pojke", "syster", "dotter", "son", "bror", "katt", "fr"+ao+"ga", "text", "bil", "stol", "penna", "hus", "m"+ae+"nniska","rum", "papper", "v"+ae+"ska", "tidning", "lektion", "student", "l"+ae+"rare", "hund", "katt", "l"+ae+"kare", "station", "h"+ao+"llplats", "mening", "l"+ae+"genhet", "gata", "rum", "k"+oe+"k", "vardagsrum", "arbetsrum", "sovrum", "badrum", "soffa", "f"+ao+"t"+oe+"lj", "soffbord", "skrivbord", "dator", "s"+ae+"ng","garderob", "bokhylla", "matta", "spegel", "morgon", "dusch", "frukost", "jobb", "dagis", "buss"]

for word in words:
	try:
		print getDefinition(word)
	except:
		e = sys.exc_info()[1]
		print "Error for " + word + " " + str(e)
	print
