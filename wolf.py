#!/usr/bin/python3

import sys
import datetime
import argparse
import os

APP_NAME = "wolf"
_VERSION = "0.2.4"

_FILE_NAME_ = ".productivity.ord"
_USAGE = "usage: wolf.py [-hov]? <string>"
NL = "\n"

class App():
	# Print version program and exit
	@staticmethod
	def version():
		print("wolf: v%s" % _VERSION)
		print(" [\033[32m+\033[0m] %s" % "program split on classes")
		print(" [\033[32m+\033[0m] %s" % "program add option yesterday")
		print(" [\033[32m+\033[0m] %s" % "fix typos")
		exit(0)

	@staticmethod
	def error(msg):
		print("[error]: %s" % msg)

	@staticmethod
	def warning(msg):
		print("[warning]: %s" % msg)

	# get file name
	@staticmethod
	def getFileName():
		name = os.environ['HOME'] + '/' + _FILE_NAME_
		return name

	@staticmethod
	def message(msg):
		print("[%s]: %s" %(APP_NAME, msg))


class Filter():
	def __init__(self, opt):
		self.opt = opt

	def string(self, line):
		return True

	def log(self, val):
		if self.opt.yesterday == True:
			return val.startswith( Format.date( getYesterday() ) )
		return True


def getYesterday():
	return datetime.date.today() - datetime.timedelta(days=1)

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
	if os.path.exists(App.getFileName()) == False:
		App.warning("file is not found")
		if isCreate == True:
			print("you want create file with name " + App.getFileName() + " ? [Y/n]: ", end='')
			if sinput() == True:
				fd = open(App.getFileName(), 'a'); fd.close()
				return;
		exit(0)

# @Class (format): for format output
class Format():
	@staticmethod
	def theme(theme):
		theme_string = " \033[33m" + theme + "\033[0m\n"
		return theme_string

	@staticmethod
	def message(message):
		message_string = "\t\t\t\033[32m" + message + "\033[0m" + "\n"
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
	def log(message, theme=""):
		time = Format.datetime()
		theme = Format.theme(theme)
		message = Format.message(message)
		format_log = time + theme + message + NL
		return format_log

	@staticmethod
	def datetime(date=datetime.datetime.today().date(), time=datetime.datetime.today().time()):
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

	def add(self, message, theme):
		checkfile()
		with open(App.getFileName(), 'a') as fd:
			logmsg = Format.log(message, theme)
			fd.write(logmsg)

	def out(self):
		logs_count = 0 
		line_count = 0
		wfilter = Filter(self.opt)
		# loop in logs
		for log in self.logs:
			if wfilter.log(log) == True:
				logs_count = logs_count + 1
				# loop in lines
				for line in log.split('\n'):
					if wfilter.string(line) == True:
						line_count = line_count + 1
						print("%s" % line)

		return [logs_count, line_count]

	def readlogs(self, fd):
		lines = fd.readlines()
		for line in lines:
			if line == "\n":
				self.logs.append("")
			else:
				self.logs[-1] += line

	def order(self):
		reads = [0, 0]
		checkfile(False)
		with open(App.getFileName()) as fd:
			self.readlogs(fd)
			reads = self.out()

		if reads[0] <= 0: 	App.message("no records found")
		else: 				print("today: %s" % Format.strend())

	def __str__(self):
		res = Format.datetime(self.date, self.time)
		res += Format.theme(self.theme)
		res += Format.message(self.message)
		return res


class OrderOption():
	def __init__(self):
		self.yesterday = None

	def parse(self, opt):
		# set yesterday flag
		if opt.yesterday == True:
			self.yesterday = True


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
parser.add_argument('-y', '--yesterday', action='store_true', help='display only yesterday date')
options = parser.parse_args();

# Parse order options
orderopt = OrderOption()
orderopt.parse(options)

# get Log
log = Log(orderopt)

if options.theme == None:
	options.theme = "";

if options.version == True:
	App.version()
elif options.order == True:
	log.order()
elif options.log != None:
	log.add( options.log, options.theme )

exit(0)