import ipdb

import httplib
import urllib
from bs4 import BeautifulSoup
import re

def createHTML(pubID):

	SEARCH_HOST = "ncbi.nlm.nih.gov"
	conn = httplib.HTTPConnection(SEARCH_HOST)
	headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
	url = "http://www.ncbi.nlm.nih.gov/pubmed/"+str(pubID)+"?report=xml"
	conn.request("GET", url, '', headers)
	resp = conn.getresponse()
	if not resp.status == 200:
		raise Exception('Response from Google Scholar url:' +
			url + ' did not return with code 200')

	html = resp.read()
	return html.decode('ascii', 'ignore')
	# return html

def getPaperFromID(pubID):
	#import ipdb
	#ipdb.set_trace()
	html = createHTML(pubID)
	soup = BeautifulSoup(html, 'xml')
	noneformat_str = soup.prettify(formatter=None)
	noneformat_soup = BeautifulSoup(noneformat_str)
	title = noneformat_soup.find('articletitle').get_text()
	href = "http://www.ncbi.nlm.nih.gov/pubmed/"+str(pubID)
	temp = noneformat_soup.find('authorlist')
	authorLasts = temp.find_all('lastname')#.get_text()
	authorFirsts = temp.find_all('forename')
	print authorFirsts
	FinalAuthorNames = []
	for i in range(len(authorLasts)):
		name = authorFirsts[i].get_text() + ' ' +  authorLasts[i].get_text()
		FinalAuthorNames.append((name,None))
	print FinalAuthorNames
	return Paper(title,href,FinalAuthorNames,None)

def getListOfCitations(pubID):
	SEARCH_HOST = "ncbi.nlm.nih.gov"
	conn = httplib.HTTPConnection(SEARCH_HOST)
	headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
	url = "http://www.ncbi.nlm.nih.gov/pubmed/"+str(pubID)+"?report=xml"
	conn.request("GET", url, '', headers)
	resp = conn.getresponse()
	if not resp.status == 200:
		raise Exception('Response from Google Scholar url:' +
			url + ' did not return with code 200')
	html = resp.read()
	html = html.decode('ascii','ignore')
	soup = BeautifulSoup(html, 'xml')
	noneformat_str = soup.prettify(formatter=None)
	noneformat_soup = BeautifulSoup(noneformat_str)
	otherDocIDS = noneformat_soup.find_all('pmid')
	#print otherDocIDS
	adjList = []
	for i in range(len(otherDocIDS)):
		tmp = otherDocIDS[i].get_text()
		adjList.append(tmp)
	return adjList	

def getCitedPapers(pubID):
	adjList = getListOfCitations(pubID)
	ans = []
	for i in adjList:
		ans.append(getPaperFromID)



class Paper:
    def __init__(self, title, title_href, author_list, citers_page_href):
        self.title = title
        self.title_href = title_href
        self.author_list = author_list
        self.citers_page_href = citers_page_href

    def __hash__(self):
        return hash(self.title_href)





	#print noneformat_soup
	#print noneformat_soup.find('')


pubID = 22606286
getPaperInfo(createHTML(pubID),pubID)
getListOfCitations(createHTML(pubID))
