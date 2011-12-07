#!/bin/python2.7

import urllib2
import codecs
import sys
import random
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
	
	definition = tree.xpath("//span[@id='Swedish']/../following-sibling::*[span[@id[contains(.,'Noun')]]][1]/following-sibling::ol[1]/li[1]/child::node()[not(ancestor-or-self::dl) and not(ancestor-or-self::ul) and not(ancestor-or-self::span)]/descendant-or-self::text()")
	w.definition = "".join(definition).split(";")[0]

	declension = tree.xpath("//span[@id='Swedish']/../following-sibling::*[span[@id[contains(.,'Noun')]]][1]/following-sibling::div[@class='NavFrame'][1]/div[@class='NavContent']/table/tr[3]/td")
	w.declension = tuple([d.xpath("string()").encode("utf-8") for d in declension])

	return w

def generateWordList(definitions):
	wordlist = open("wordlist.tex", "w")
	for d in definitions:
		line = "%(definition)s & %(gender)s " % {"gender":d.gender, "word": d.word, "definition": d.definition}
		line += " & ".join(d.declension)
		line += " \\\\ \n"
		wordlist.write(line)
	wordlist.close()

def generateQuiz(definitions):
	wordlist = open("wordlist.tex", "w")
	for d in definitions:
		words = [d.definition, d.gender + " " + d.word] + list(d.declension[1:])
		line = ""
		num = random.randint(0,4)
		for i in range(5):
			if i == num:
				line += words[i]
			else:
				line += "\\rule{1.5cm}{0.4pt}"
			if i != 4:
				line += " & "
			else:
				line += " \\\\ \n"
		wordlist.write(line)
	wordlist.close()


#chapter 1 and 2
#words = [ao+"r", "kapitel", "fru", "man", "ord", "familj", "flicka", "pojke", "syster", "dotter", "son", "bror", "katt", "fr"+ao+"ga", "text", "bil", "stol", "penna", "hus", "m"+ae+"nniska","rum", "papper", "v"+ae+"ska", "tidning", "lektion", "student", "l"+ae+"rare", "hund", "katt", "l"+ae+"kare", "station", "h"+ao+"llplats", "mening", "l"+ae+"genhet", "gata", "rum", "k"+oe+"k", "vardagsrum", "arbetsrum", "sovrum", "badrum", "soffa", "f"+ao+"t"+oe+"lj", "soffbord", "skrivbord", "dator", "s"+ae+"ng","garderob", "bokhylla", "matta", "spegel", "morgon", "dusch", "frukost", "jobb", "dagis", "buss", "mor", "far", "mamma", "pappa", "f" + oe + "r" + ae + "lder", "syskon", "barn", oe + "ga", "piano", "ben", "v" + ae + "n"]

#chapter 3
#words = ["arbete","bank","skola","elev","klass","lektion","matematik","idrott","musik","hem",ae + "pple","student","bokstav","l" + ae + "xa","helg","fara","undantag","regel","timme","kudde","betoning","stavelse","spr" + ao + "k","polis","telefon","maskin","cigarett","fot","hand","tand","natt","stad","foto","musiker","tekniker","australier"]

#chapter 4 and 5
words = ["t" + ao + "rta","present","paket","cykel","kompis","siffra","morgon","dag","kv" + ae + "ll","mat","lunch","godis","frukt","gr" + oe + "nsak","mj" + oe + "lk","juice","sm" + oe + "r","ost","kaffe","skinka","potatis","gurka","tomat","korv","pasta","f" + ae + "rs","banan","apelsin","kassa","vara","kasse","film","kaka","mellanm" + ao + "l"]
#words = [ao+"r"]

definitions = []

for word in words:
	try:
		definitions.append(getDefinition(word))
	except:
		e = sys.exc_info()[1]
		print "Error for " + word + " " + str(e)

generateWordList(definitions)
#generateQuiz(definitions)


