#!/usr/bin/python3

import sys
import datetime
import argparse
import os

_VERSION = "0.2.1"
_FILE_NAME_ = ".productivity.ord"
_USAGE="usage: wolf.py [-hov]? <string>"


class Filter():
	def __init__(self, opt):
		self.opt = opt

	def string(self, line):
		return True

	def log(self, val):
		if self.opt.tommorow == True:
			return val.startswith( Format.date( getTomorrow() ) )
		return True

# Output list order file
def order(orderopt):
	checkfile(False)
	with open(getFileName()) as fd:
		clog = Log(orderopt)
		clog.readlogs(fd)
		clog.out()

	print("today: %s" % Format.strend())


# filter order options
def orderfilter(line, opropt):
	result = True
	if orderopt.tommorow == True:
		if isTomorrow(line) == False:
			result = False

	return result

# has tomorrow date in line
# def isTomorrow(line):
# 	return line.startswith(getTomorrowString())

def isTomorrow(log):
	return log.startswith( Format.date(getTomorrow()) )

def getTomorrow():
	return datetime.date.today() - datetime.timedelta(days=1)

# get tomorrow day in format [01.01.2019][23:00:00]
# def getTomorrowString():
# 	tmr = datetime.date.today() - datetime.timedelta(days=1)
# 	strtime = tmr.strftime("[" + '\033[34m' + "%d.%m.%Y" + '\033[0m' + "]")
# 	return strtime

# Add log string in order list 
def log(message, theme=""):
	checkfile()
	fd = open(getFileName(), 'a')
	logmsg = getLog(message, theme)
	fd.write(logmsg)
	fd.close()

# input positive answer
def sinput():
	answer = ''
	while len(answer) <= 0:
		answer = input()
	
	if answer[0] == 'y' or answer[0] == 'Y':
		return True
	
	return False

# check exist file '.productivity.ord' in home directory
def checkfile(isCreate=True):
	if os.path.exists(getFileName()) == False:
		print("[warning]: file is not found")
		if isCreate == True:
			print("you want create file with name " + getFileName() + " ? [Y/n]: ", end='')
			if sinput() == True:
				fd = open(getFileName(), 'a'); fd.close()
				return;
		exit(0)

# get file name
def getFileName():
	name = os.environ['HOME'] + '/' + _FILE_NAME_
	return name

# get log
def getLog(message, theme):
	time = getDateTime()
	theme = getTheme(theme)
	message = getMessage(message)
	log_string = time + theme + message + "\n\n"
	return log_string

# get theme if format string
def getTheme(theme):
	theme_string = "\033[33m" + theme + "\033[0m\n"
	return theme_string

# get message is format string
def getMessage(message):
	message_string = "\t\t\t\033[32m" + message + "\033[0m"
	return message_string

# Print version program and exit
def version():
	print("wolf: v%s" % _VERSION)
	print(" [\033[32m+\033[0m] %s" % "program split on classes")
	print(" [\033[32m+\033[0m] %s" % "program add option tomorrow")
	exit(0)

def getDateTime(today=datetime.datetime.today()):
	return getDate(today) + getTime(today) + "  "

# get time if format string
def getTime(today=datetime.datetime.today()):
	# today = datetime.datetime.today()
	timestr = today.strftime("[" + '\033[36m' + "%H:%M:%S" + "\033[0m" + "]")
	return timestr

def getDate(today=datetime.datetime.today()):
	# today = datetime.datetime.today()
	timestr = today.strftime("[" + '\033[34m' + "%d.%m.%Y" + '\033[0m' + "]")
	return timestr


# @Class (format): for format output
class Format():
	@staticmethod
	def theme(theme):
		theme_string = " \033[33m" + theme + "\033[0m\n"
		return theme_string

	@staticmethod
	def message(message):
		message_string = "\t\t\t\033[32m" + message + "\033[0m" + "\n\n"
		return message_string

	@staticmethod
	def date(dt=datetime.datetime.today().date()):
		return dt.strftime("[" + '\033[34m' + "%d.%m.%Y" + '\033[0m' + "]")

	@staticmethod
	def time(tm=datetime.datetime.today().time()):
		return tm.strftime("[" + '\033[36m' + "%H:%M:%S" + "\033[0m" + "] ")

	@staticmethod
	def strend(date=datetime.datetime.today()):
		return date.strftime("%a.%d %B.%m %Y %H:%M:%S")

	@staticmethod
	def datetime(date, time):
		day = datetime.datetime(date.year, date.month, date.day, time.hour, time.minute, time.second)
		res = day.strftime("[" + '\033[34m' + "%d.%m.%Y" + '\033[0m' + "]" + "[" + '\033[36m' + "%H:%M:%S" + "\033[0m" + "] ")
		return res 

# @Class (Log): functions output and input logs
class Log():

	def __init__(self, opt):
		self.date = None
		self.time = None 
		self.theme = ""
		self.message = ""
		self.logs = [""]
		self.opt = opt

	def out(self):
		wfilter = Filter(self.opt)
		for log in self.logs:
			if wfilter.log(log) == True:
				for line in log.split('\n'):
					if wfilter.string(line) == True:
						print("%s" % line)

	def readlogs(self, fd):
		lines = fd.readlines()
		for line in lines:
			if line == "\n":
				self.logs.append("")
			else:
				self.logs[-1] += line

	def __str__(self):
		res = Format.datetime(self.date, self.time)
		res += Format.theme(self.theme)
		res += Format.message(self.message)
		return res

	# getter and setters
	# def getDate(self):
	# 	return self.date 

	# def setDate(self, dt=datetime.datetime.today()):
	# 	self.date = dt

	# def getTime(self):
	# 	return self.time 

	# def setTime(self, tm):
	# 	self.time = tm

	# def getTheme(self):
	# 	return self.theme 

	# def setTheme(self, thm):
	# 	self.theme = thm

	# def getMessage(self):
	# 	return self.message 

	# def setMessage(self, msg):
	# 	self.message = msg


class OrderOption():
	def __init__(self):
		self.tommorow = None

	def parse(self, opt):
		# set tomorrow flag
		if opt.tomorrow == True:
			self.tommorow = True


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
parser.add_argument('-r', '--tomorrow', action='store_true', help='display only tomorrow date')
options = parser.parse_args();

# Parse order options
orderopt = OrderOption()
orderopt.parse(options)


if options.theme == None:
	options.theme = "";

if options.version == True:
	version()
elif options.order == True:
	order(orderopt)
elif options.log != None:
	log(options.log, options.theme)




exit(0)