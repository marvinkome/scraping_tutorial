from urllib import urlopen
from bs4 import BeautifulSoup
import re
import random
import datetime


internalPages = set()
externalPages = set()

random.seed(datetime.datetime.now())

def split_url(url):
	url = url.replace("http://","")
	url = url.split("/")
	url = url[0].split(".")

	if len(url) == 3:
		return url[1]
	else:
		return url[0]
    
def getInternalLink(url):
	
	internalLink = []
	html = urlopen(url)
	bsObj = BeautifulSoup(html,"html.parser")
	splited_url = split_url(url)
	
	links = bsObj.find_all('a',href=re.compile("^(/|.*"+splited_url+")"))
			
	for link in links:
		if link.attrs["href"] is not None:
			if link.attrs["href"] not in internalLink:
				 internalLink.append(link.attrs["href"])
				 
	return internalLink
	
def getExternalLink(url):
	
	externalLinks = []
	html = urlopen(url)		
	bsObj = BeautifulSoup(html,"html.parser")
	splited_url = split_url(url)
	
	links = bsObj.find_all("a", href=re.compile("^(http|www)((?!"+splited_url+").)*$"))

	for link in links:
		if link.attrs["href"] is not None:
			if link.attrs["href"] not in externalLinks:
				externalLinks.append(link.attrs["href"])
	
	return externalLinks
		
def getRandomLink(url):
	external_links = getExternalLink(url)
	
	if len(external_links) == 0:
		internal_links = getInternalLink(url)
		if len(internal_links) == 0:
			print "No more links to follow. Breaking"
			return None
		else:
			randLink = internal_links[random.randint(0, len(internal_links) - 1)]
			getRandomLink(randLink)		
	else:
		randLink = externalLinks[random.randint(0, len(externalLinks) - 1)]
		return randLink
	
def followExternalOnly(url):
	randLink = getRandomLink(url)
	print " "
	print randLink
	print "-"*8
	followExternalOnly(randLink)
	
followExternalOnly("http://oayomide.com.ng")
