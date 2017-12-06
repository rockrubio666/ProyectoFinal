#!/usr/bin/python

import hashlib
import re
import sys
import csv
import requests
from lxml import etree
from lxml import html
import wget
import os
from collections import Counter
import operator
from termcolor import colored

def ojs(arg,verbose,cookie,agent,proxip,proxport):
	
	requests.packages.urllib3.disable_warnings()
	
	if len(proxip) == 0:
		if cookie is None and agent is None:
			req = requests.get(arg,verify=False)
			
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			req = requests.get(arg,headers = headers,verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			req = requests.get(arg, cookies = cookies, verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			req = requests.get(arg, cookies = cookies, headers = headers,verify=False)
	else:
		proxy = proxip + ':' + proxport	
		proxies = {'http' : proxy, 'https' : proxy,}
		if cookie is None and agent is None:
			req = requests.get(arg,proxies = proxies,verify=False)
			
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			req = requests.get(arg,headers = headers, proxies = proxies,verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			req = requests.get(arg, cookies = cookies, proxies = proxies,verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			req = requests.get(arg, cookies = cookies, headers = headers, proxies = proxies,verify=False)
	
	page_source =  req.text
	regex = re.compile(r'(.*)(name="generator") content="(.*)"(.*)')
	match = regex.search(page_source)

	try:
		if match.group():	
			if int(verbose) == 1:
				print "la version del sitio es: " + colored(match.group(3),'green')
			elif int(verbose) == 2:
				print "La version del sitio: " + colored(arg, 'green') + " es: " + colored(match.group(3),'green')
			elif int(verbose) == 3:
				print "La version del sitio: " + colored(arg, 'green') + " es: " + colored(match.group(3),'green')
				print "Version del sitio encontrada en:" + colored(match.group(),'green')
		
	except:
		version(arg,verbose,cookie,agent,proxip,proxport)
	
	files(arg,verbose,match.group(3),cookie,agent,proxip,proxport)
	
			
	
def version(arg,verbose,cookie,agent,proxip,proxport):
	m = hashlib.md5()
	elements = []
	average = []
	listFind = [ '//script/@src', '//head/link[@rel="stylesheet"]/@href', '//img/@src','//link[@rel="shortcut icon"]/@href']
	
	requests.packages.urllib3.disable_warnings()					
	proxy = proxip + ':' + proxport
	proxies = {'http' : proxy, 'https' : proxy,}
	if len(proxip) == 0:
		if cookie is None and agent is None:
			req = requests.get(arg, verify=False)
		
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			req = requests.get(arg,headers = headers, verify=False)
	
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			req = requests.get(arg, cookies = cookies, verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			req = requests.get(arg, cookies = cookies, headers = headers, verify=False)
	else:
		if cookie is None and agent is None:
			req = requests.get(arg,proxies = proxies,verify=False)
		
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			req = requests.get(arg,headers = headers, proxies = proxies,verify=False)
	
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			req = requests.get(arg, cookies = cookies, proxies = proxies,verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			req = requests.get(arg, cookies = cookies, headers = headers, proxies = proxies,verify=False)
	
	webpage = html.fromstring(req.content)
	dom = re.sub(r'(http|https)://','',arg)

	for i in range(0,len(listFind)):
		for link in webpage.xpath(listFind[i]):
			if dom in link:
				if len(proxip) == 0:
					if cookie is None and agent is None:
						req = requests.get(link,verify=False)
		
					elif cookie is None and agent is not None:
						headers = {'user-agent': agent}
						req = requests.get(link,headers = headers, verify=False)
			
					elif cookie is not None and agent is None:
						cookies = dict(cookies_are=cookie) 
						req = requests.get(link, cookies = cookies, verify=False)
		
					elif cookie is not None and agent is not None:
						headers = {'user-agent': agent}
						cookies = dict(cookies_are=cookie) 
						req = requests.get(link, cookies = cookies, headers = headers, verify=False)
				else:
					if cookie is None and agent is None:
						req = requests.get(link,proxies = proxies,verify=False)
		
					elif cookie is None and agent is not None:
						headers = {'user-agent': agent}
						req = requests.get(link,headers = headers, proxies = proxies,verify=False)
			
					elif cookie is not None and agent is None:
						cookies = dict(cookies_are=cookie) 
						req = requests.get(link, cookies = cookies, proxies = proxies,verify=False)
		
					elif cookie is not None and agent is not None:
						headers = {'user-agent': agent}
						cookies = dict(cookies_are=cookie) 
						req = requests.get(link, cookies = cookies, headers = headers, proxies = proxies,verify=False)
	
				if req.status_code == 200 and i in range(2,3):
					try:
						filename = wget.download(link, bar=None)
						m.update(filename)
						hs = m.hexdigest()
						elements.append(hs)
						os.remove(filename)
					except:
						continue
				
				else:
					try:
						m.update(req.text)
						hs =  m.hexdigest()
						elements.append(hs)
					except:
						continue
					
	f = open('versions','rb')
	reader = csv.reader(f,delimiter=',')
			
	for element in elements:
		for row in reader:
			try:
				if element in row[2] and 'Ojs' in row[0]:
					average.append(row[1])
			except:
				continue
	f.close()

	cnt = Counter(average)
	if int(verbose) == 1 or int(verbose) == 2 or int(verbose) == 3:
		v = max(cnt.iteritems(),key=operator.itemgetter(1))[0]
		print '\nVersion del sitio aproximada mediante archivos de configuracion: ' + colored(v, 'green')
	files(arg,verbose,v,cookie,agent,proxip,proxport)
	
	
def files(arg,verbose,version,cookie,agent,proxip,proxport):
	
	f = open('versions','rb')
	reader = csv.reader(f,delimiter=',')

	listThemes = ['//script/@src', '//@href']
	tmp = []
	requests.packages.urllib3.disable_warnings()					
	
	proxy = proxip + ':' + proxport
	proxies = {'http' : proxy, 'https' : proxy,}
	for row in reader:
		try:
			if 'Plugin' in row[1] and 'Ojs' in row[0]:
				plugin = arg + '/plugins' + row[2]
				
				if len(proxip) == 0:
					if cookie is None and agent is None:
						req = requests.get(plugin,verify=False)
					
					elif cookie is None and agent is not None:
						headers = {'user-agent': agent}
						req = requests.get(plugin,headers = headers, verify=False)
			
					elif cookie is not None and agent is None:
						cookies = dict(cookies_are=cookie) 
						req = requests.get(plugin, cookies = cookies, verify=False)
		
					elif cookie is not None and agent is not None:
						headers = {'user-agent': agent}
						cookies = dict(cookies_are=cookie) 
						req = requests.get(plugin, cookies = cookies, headers = headers, verify=False)
				
				else:
					if cookie is None and agent is None:
						req = requests.get(plugin,proxies = proxies,verify=False)
					
					elif cookie is None and agent is not None:
						headers = {'user-agent': agent}
						req = requests.get(plugin,headers = headers, proxies = proxies,verify=False)
			
					elif cookie is not None and agent is None:
						cookies = dict(cookies_are=cookie) 
						req = requests.get(plugin, cookies = cookies,proxies = proxies, verify=False)
		
					elif cookie is not None and agent is not None:
						headers = {'user-agent': agent}
						cookies = dict(cookies_are=cookie) 
						req = requests.get(plugin, cookies = cookies, headers = headers, proxies = proxies,verify=False)
					
				if req.status_code == 200:
					plugName = re.compile(r'=== (.*)')
					pN = plugName.search(req.text)
					plugVers = re.compile(r'(===) (Version(.*))')
					pV = plugVers.search(req.text)
					try:
						if pN.group():	
							try:
								if pV.group():
									if int(verbose) == 1:
										print "Plugin Name: " + colored(pN.group(1),'green')
									elif int(verbose) == 2:
										print "Plugin, Name: " + colored(pN.group(1),'green') + ' ,Path: ' + colored(plugin, 'green')
									elif int(verbose) == 3:
										print "Plugin, Name: " + colored(pN.group(1), 'green') + ' ,Path: ' + colored(plugin, 'green') + " " + colored(pV.group(2), 'blue')
							except:
								if int(verbose) == 1:
									print "Plugin Name: " + colored(pN.group(1), 'green') 
								elif int(verbose) == 2 or int(verbose) == 3:
									print "Plugin, Name: " + colored(pN.group(1), 'green') + ' ,Path: ' + colored(plugin, 'green')		
					except:
						continue
					
					regex = re.compile(r'(.*)\/(.*)\/README(.*)')
					match = regex.search(plugin)
					try:
						if match.group():
							if int(verbose) == 1:
								print "Plugin Name: " + colored(match.group(2),'green')
							elif int(verbose) == 2 or int(verbose) == 3:
								print "Plugin, Name: " + colored(match.group(2), 'green') + ' ,Path: ' + colored(plugin, 'green')
					except:
						continue
				
				else:
					continue

			elif 'Readme' in row[1] and 'Ojs' in row[0]:
				readme = arg + '/docs/release-notes/README-' + row[2]
				
				
				if len(proxip) == 0:
					if cookie is None and agent is None:
						req = requests.get(readme,verify=False)
		
					elif cookie is None and agent is not None:
						headers = {'user-agent': agent}
						req = requests.get(readme,headers = headers, verify=False)
			
					elif cookie is not None and agent is None:
						cookies = dict(cookies_are=cookie) 
						req = requests.get(readme, cookies = cookies, verify=False)
		
					elif cookie is not None and agent is not None:
						headers = {'user-agent': agent}
						cookies = dict(cookies_are=cookie) 
						req = requests.get(readme, cookies = cookies, headers = headers, verify=False)
				
				else:
					if cookie is None and agent is None:
						req = requests.get(readme,proxies = proxies,verify=False)
		
					elif cookie is None and agent is not None:
						headers = {'user-agent': agent}
						req = requests.get(readme,headers = headers, proxies = proxies,verify=False)
			
					elif cookie is not None and agent is None:
						cookies = dict(cookies_are=cookie) 
						req = requests.get(readme, cookies = cookies, proxies = proxies,verify=False)
			
					elif cookie is not None and agent is not None:
						headers = {'user-agent': agent}
						cookies = dict(cookies_are=cookie) 
						req = requests.get(readme, cookies = cookies, headers = headers,proxies = proxies, verify=False)
	
				if req.status_code == 200 and int(verbose) == 3:
					print 'README file: ' + colored(readme, 'green')
				else:
					continue
					
			
			elif 'Change' in row[1] and 'Ojs' in row[0]:		
				changeLog = arg + '/docs/release-notes/ChangeLog-' + row[2]
				
				if len(proxip) == 0:
					if cookie is None and agent is None:
						req = requests.get(changeLog,verify=False)
		
					elif cookie is None and agent is not None:
						headers = {'user-agent': agent}
						req = requests.get(changeLog,headers = headers, verify=False)
			
					elif cookie is not None and agent is None:
						cookies = dict(cookies_are=cookie) 
						req = requests.get(changeLog, cookies = cookies, verify=False)
		
					elif cookie is not None and agent is not None:
						headers = {'user-agent': agent}
						cookies = dict(cookies_are=cookie) 
						req = requests.get(changeLog, cookies = cookies, headers = headers, verify=False)
	
				else:
					if cookie is None and agent is None:
						req = requests.get(changeLog,proxies = proxies,verify=False)
		
					elif cookie is None and agent is not None:
						headers = {'user-agent': agent}
						req = requests.get(changeLog,headers = headers, proxies = proxies,verify=False)
			
					elif cookie is not None and agent is None:
						cookies = dict(cookies_are=cookie) 
						req = requests.get(changeLog, cookies = cookies, proxies = proxies,verify=False)
		
					elif cookie is not None and agent is not None:
						headers = {'user-agent': agent}
						cookies = dict(cookies_are=cookie) 
						req = requests.get(changeLog, cookies = cookies, headers = headers, proxies = proxies,verify=False)

				if req.status_code == 200 and int(verbose) == 3:
					print 'ChangeLog: ' + colored(changeLog,'green')
				else:
					continue

			elif 'Robots' in row[1] and 'Ojs' in row[0]:
				
				if len(proxyip) == 0:
					if cookie is None and agent is None:
						req = requests.get(arg + row[2],verify=False)
		
					elif cookie is None and agent is not None:
						headers = {'user-agent': agent}
						req = requests.get(arg + row[2],headers = headers, verify=False)
			
					elif cookie is not None and agent is None:
						cookies = dict(cookies_are=cookie) 
						req = requests.get(arg + row[2], cookies = cookies, verify=False)
		
					elif cookie is not None and agent is not None:
						headers = {'user-agent': agent}
						cookies = dict(cookies_are=cookie) 
						req = requests.get(arg + row[2], cookies = cookies, headers = headers, verify=False)
	
				else:
					if cookie is None and agent is None:
						req = requests.get(arg + row[2],proxies = proxies,verify=False)
		
					elif cookie is None and agent is not None:
						headers = {'user-agent': agent}
						req = requests.get(arg + row[2],headers = headers, proxies = proxies,verify=False)
			
					elif cookie is not None and agent is None:
						cookies = dict(cookies_are=cookie) 
						req = requests.get(arg + row[2], cookies = cookies, proxies = proxies,verify=False)
		
					elif cookie is not None and agent is not None:
						headers = {'user-agent': agent}
						cookies = dict(cookies_are=cookie) 
						req = requests.get(arg + row[2], cookies = cookies, headers = headers, proxies = proxies,verify=False)
				
				if req.status_code == 200 and int(verbose) == 3:
					print 'Robots file: ' + colored(req.url, 'green')
				else:
					continue
		except:
			continue
	f.close()
	
	if len(proxip) == 0:
		if cookie is None and agent is None:
			req = requests.get(arg,verify=False)
		
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			req = requests.get(arg,headers = headers, verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			req = requests.get(arg, cookies = cookies, verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			req = requests.get(arg, cookies = cookies, headers = headers, verify=False)
	else:
		if cookie is None and agent is None:
			req = requests.get(arg,proxies = proxies,verify=False)
		
		elif cookie is None and agent is not None:
			headers = {'user-agent': agent}
			req = requests.get(arg,headers = headers, proxies = proxies,verify=False)
		
		elif cookie is not None and agent is None:
			cookies = dict(cookies_are=cookie) 
			req = requests.get(arg, cookies = cookies, proxies = proxies,verify=False)
		
		elif cookie is not None and agent is not None:
			headers = {'user-agent': agent}
			cookies = dict(cookies_are=cookie) 
			req = requests.get(arg, cookies = cookies, headers = headers, proxies = proxies,verify=False)
	
	webpage = html.fromstring(req.content)
	for i in range(0,len(listThemes)):
		for link in webpage.xpath(listThemes[i]):
			if 'theme' in link or 'journals' in link or 'themes' in link:
				tmp.append(link)
			else:
				continue
				
	for element in range(0,len(tmp)):
		if 'default' in tmp[element]:
			if int(verbose) == 1:
				print colored('Default Theme', 'green')
			elif int(verbose) == 2 or int(verbose) == 3:
				print colored( 'Default Theme', 'green') + ' Path: ' + colored(tmp[element], 'green')
			element + i
		elif 'journals' in tmp[element]:
			regex = re.compile(r'(.*)\/(.*)\.css')
			match = regex.search(tmp[element])
			try:
				if match.group():
					if int(verbose) == 1:
						print colored('Customize Theme ', 'green')
					elif int(verbose) == 2:
						print colored('Customize Theme, Name: ' + match.group(2), 'green')
					elif int(verbose) == 3:	
						print 'Customize Theme, Name: ' + colored(match.group(2), 'green') + ', Path: ' + colored(tmp[element],'green')
					element + 1
			except:
				pass
		elif 'theme' in tmp[element]:
			regex = re.compile(r'(.*)\/(.*)\.css')
			match = regex.search(tmp[element])
			try:
				if match.group():
					if int(verbose) == 1:
						print 'Theme, Name: ' + colored(match.group(2),'green')
					elif int(verbose) == 2 or int(verbose) == 3:	
						print 'Theme, Name: ' + colored(match.group(2), 'green') + ', Path: ' + colored(tmp[element],'green')
			except:
				pass	
		elif 'bootstrap' in tmp[element]:
			regex = re.compile(r'(.*)\/(.*)\.css')
			match = regex.search(tmp[element])
			try:
				if match.group():	
					if int(verbose) == 1:
						print 'Theme, Name: ' + colored(match.group(2))
					elif int(verbose) == 2 or int(verbose) == 3:
						print 'Theme, Name: ' + colored(match.group(2), 'green') + ', Path: ' + colored(tmp[element],'green')
			except:
				pass	
		else:
			sys.exit
	vuln(version,verbose)

def vuln(version,verbose):
	f = open('vuln','rb')
	reader = csv.reader(f,delimiter=',')
	
	for row in reader:
		if 'Ojs' in row[0] and row[1] in version:
			if int(verbose) == 1:
				print "Vulnerability Link: " + colored(row[3],'green')
			elif int(verbose) == 2 or int(verbose) == 3:
				print "Vulnerability Name: " + colored(row[2],'green') + ' ,Vulnerability Link: ' + colored(row[3],'green')
	f.close()
	

