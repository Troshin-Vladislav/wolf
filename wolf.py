#!/usr/bin/python3

import sys
import datetime
import argparse
import os

_VERSION = "0.1.2"
_FILE_NAME_ = ".productivity.ord"
_USAGE="usage: wolf.py [-hov]? <string>"


# Output list order file
def order():
	with open(getFileName()) as fd:
		for line in fd:
			print(line, end='')

# Add log string in order list 
def log(message, theme=""):
	fd = open(getFileName(), 'a')
	logmsg = getLog(message, theme)
	fd.write(logmsg)
	fd.close()

# get file name
def getFileName():
	name = os.environ['HOME'] + '/' + _FILE_NAME_
	return name

# get log
def getLog(message, theme):
	time = getTime()
	theme = getTheme(theme)
	message = getMessage(message)
	log_string = time + theme + message + "\n\n"
	return log_string

# get theme if format string
def getTheme(theme):
	theme_string = " \033[33m" + theme + "\033[0m\n"
	return theme_string

# get message is format string
def getMessage(message):
	message_string = "\t\t\t\033[32m" + message + "\033[0m"
	return message_string

# Print version program and exit
def version():
	print("wolf: v%s" % _VERSION)
	exit(0)

# get time if format string
def getTime():
	today = datetime.datetime.today()
	timestr = today.strftime("[" + '\033[34m' + "%d.%m.%Y" + '\033[0m' + "][" + '\033[36m' + "%H:%M:%S" + "\033[0m" + "] ")
	return timestr

# Block arguments
if len(sys.argv) < 2:
	print(_USAGE)
	exit(1)

# Parse Arguments
parser = argparse.ArgumentParser(description='wolf - work order list. watch productivity work day', usage=_USAGE)
parser.add_argument('-o', '--order', action='store_true', help='output list productivity file')
parser.add_argument('-v', '--version', action='store_true', help='print version program and exit')
parser.add_argument('-l', '--log', action='store', help='add log string')
parser.add_argument('-t', '--theme', action='store', help='scpecified theme')
options = parser.parse_args();

if options.theme == None:
	options.theme = "";

if options.version == True:
	version()
elif options.order == True:
	order()
elif options.log != None:
	log(options.log, options.theme)


exit(0)