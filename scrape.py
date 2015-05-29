import urllib
from bs4 import BeautifulSoup
import re
import pickle
import nltk

masterURL = "https://ideas.repec.org/top/top.person.all.html"
prefix = "https://ideas.repec.org"

#Pull all pages for ranked economists
def readAuthorRankings(url):
	doc = urllib.urlopen(url).read()
	soup = BeautifulSoup(doc)
	authors = soup.find('table',{'class':'shorttop'})
	body = str(authors)
	body2 = re.sub("<p>.*?</p>",'',body,0,re.DOTALL|re.IGNORECASE)
	L = re.findall("href=\"(.*?)\">",body2,re.DOTALL|re.IGNORECASE)
	A = [prefix + x for x in L]
	return(A)

#Read the page of an ecomomist and pull all links for articles
def readAuthor(url):
	doc = urllib.urlopen(url).read()
	soup = BeautifulSoup(doc)
	articles = soup.find('div',{'id':'author-articles'})
	body = str(articles)
	body2 = re.sub("\"(otherversion|publishedas)\">.*?</div>",'',body,0,re.DOTALL
		 | re.IGNORECASE)
	L = re.findall("class=\"down.*?href=\"(.*?)\">",body2,re.DOTALL | re.IGNORECASE)
	A = [prefix + x for x in L]
	return(A)

#Read the abstract of an article for a given URL
def readArticle(url):
	doc = urllib.urlopen(url).read()
	soup = BeautifulSoup(doc)
	abstract = soup.find('div',{'id':'abstract-body'})
	body = re.findall("<p>(.*?)</p>",str(abstract),re.DOTALL|re.IGNORECASE)
	return(str(body))

#For a given url, get the name of the author
def readName(url):
	doc = urllib.urlopen(url).read()
	soup = BeautifulSoup(doc)
	title = str(soup.find('div',{'id':'title'}))
	name = re.findall("<h1>(.*?)</h1>",title)
	return(name)

def createDictionary():
	authorURLs = readAuthorRankings(masterURL)
	D = {}
	for each in authorURLs:
		D[each] = readName(each)
		print ("Finished with %s") % D[each]
	return(D)

#Download all abstracts for a given author
def downloadCorpus(authorURL):
	L = readAuthor(authorURL)
	C = ""
	for article in L:
		abstract = readArticle(article)
 		C = C + " " + abstract
	filename = authorURL.replace(prefix,'')
	filename2 = filename.replace(".html","")
	t = open("Corpus/"+filename2.replace("/","")+".txt",'w')
	t.write(C)
	t.close()

#Download all abstracts for all authors
def processAll(n):
	R = readAuthorRankings(masterURL)
	for author in R[0:n]:
		downloadCorpus(author)
		print("Finished with %s" % author)

def writeToFile(text,filename):
	t = open(filename,'w')
	t.write("\n".join(text))
	t.close()
