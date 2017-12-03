#!/usr/bin/python

import argparse
import sys
import os
import git 
from ojs import *
from moodle import *
from crawlerHead import *
from crawler import *
from bruteforce import *
from brutehttp import *
arg = ''


def getParams(arg):
	bforce = []	
	pvalues = []
	parser = argparse.ArgumentParser(description='Escaner de vulnerabilidades en OJS y Moodle',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)

	parser.add_argument('-a', '--Agent',metavar='Set User Agent', help='User Agent value')
	parser.add_argument('-B', '--Bruteforce',metavar='Login,UserField,PassField,User,Password,UsersFile,PassFile,Message',help='Login = Url Login, User = It could be optional, Password = It could be optional, UsersFile = It could be optional, PassFile = It could be optional')
	parser.add_argument('-b', '--bruteFile',metavar='RequestFile,User,Password,UsersFile,PassFile,Message',help=' User = It could be optional, Password = It could be optional, UsersFile = It could be optional, PassFile = It could be optional')
	parser.add_argument('-c', '--crawlerHead', metavar='File', help = 'File with directories')	
	parser.add_argument('-C', '--Crawler', help = 'Crawling site',action='store_true')	
	parser.add_argument('-k', '--Cookie',metavar='Set Cookie', help='Cookie value')
	parser.add_argument('-m','--moodle', metavar='URL', help = 'URL from Moodle site')
	parser.add_argument('-o', '--ojs', metavar= 'URL', help = 'URL from OJS site')
	parser.add_argument('-p','--proxy',metavar='Proxy IP,Port', help = 'Proxy')
	parser.add_argument('-v','--verbose', metavar='Number', nargs = '?',help='Verbose Level 1-3', default = 1)
	options = parser.parse_args()
	
	if len(sys.argv) == 1 :
		print parser.print_help()
		sys.exit(2)

	elif len(sys.argv) >= 2:
		update = raw_input('Do yo want to update the databases? [Y/N] ') or 'N'
		if 'Y' in update or 'y' in update:
			cwd = os.getcwd()		
			g = git.cmd.Git(cwd)
			g.pull()
			print 'Databases Updated'
		else:
			print 'No updated'
			pass

	if options.verbose is None:
		options.verbose = 1
		
	if int(options.verbose)	>= 4 or int(options.verbose) == 0:
		print parser.print_help()
	
	if not (options.ojs or options.moodle):
		print parser.print_help()
	
	if options.crawlerHead in sys.argv and options.Crawler in sys.argv:
		print parser.print_help()
		
	if options.Bruteforce in sys.argv and options.bruteFile in sys.argv:
		print parser.print_help()


	if options.proxy in sys.argv:
		for element in options.proxy.split(','):
			pvalues.append(element)
	else:
		pvalues.append('')
		pvalues.append('')


	if options.ojs in sys.argv:
		ojs(options.ojs,options.verbose,options.Cookie,options.Agent,pvalues[0],pvalues[1])	
	
	if options.moodle in sys.argv:
		moodle(options.moodle,options.verbose,options.Cookie,options.Agent,pvalues[0],pvalues[1])
		
	if options.Bruteforce in sys.argv:
		for element in options.Bruteforce.split(','):
			bforce.append(element)
		if len(bforce[5]) == 0 and len(bforce[6]) == 0 and len(bforce[3]) > 0 and len(bforce[4]) > 0 :
			single(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose,options.Cookie,options.Agent,pvalues[0],pvalues[1])
		elif len(bforce[3]) == 0 and len(bforce[4]) == 0 and len(bforce[5]) > 0 and len(bforce[6]) > 0:
			doubleFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose,options.Cookie,options.Agent,pvalues[0],pvalues[1])
		elif len(bforce[3]) == 0 and len(bforce[6]) == 0 and len(bforce[4]) > 0 and len(bforce[5]) > 0:
			usersFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose,options.Cookie,options.Agent,pvalues[0],pvalues[1])
		elif len(bforce[4]) == 0 and len(bforce[5]) == 0 and len(bforce[3]) > 0 and len(bforce[6]) > 0:
			pwdFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],bforce[6],bforce[7],options.verbose,options.Cookie,options.Agent,pvalues[0],pvalues[1])
	
	if options.bruteFile in sys.argv:
		for element in options.bruteFile.split(','):
			bforce.append(element)
		checkFile(bforce[0],bforce[1],bforce[2],bforce[3],bforce[4],bforce[5],options.verbose,options.Cookie,options.Agent,pvalues[0],pvalues[1])
	
	if options.Crawler == True and options.moodle in sys.argv:
		crawler(options.moodle,options.verbose,options.Cookie,options.Agent,pvalues[0],pvalues[1])
	elif options.Crawler == True and options.ojs in sys.argv:
		crawler(options.ojs,options.verbose,options.Cookie,options.Agent,pvalues[0],pvalues[1])
	
	if options.crawlerHead in sys.argv and options.ojs in sys.argv:
		crawlerHead(options.ojs,options.crawlerHead,options.verbose,options.Cookie,options.Agent,pvalues[0],pvalues[1])
	elif options.crawlerHead in sys.argv and options.moodle in sys.argv:
		crawlerHead(options.moodle,options.crawlerHead,options.verbose,options.Cookie,options.Agent,pvalues[0],pvalues[1])
		
getParams(arg)
