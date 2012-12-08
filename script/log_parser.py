# -*- coding: utf-8 -*-

import sys
import re
import xml.dom.minidom
import datetime

class Log:
	timestamp = []
	hostname = []
	user = []
	datanum = None

	aggregate_result = {}


	def __init__(self):
		self.datanum = 0

		self.aggregate_result["magwin01"] = {}
		self.aggregate_result["magwin02"] = {}
		self.aggregate_result["magwin03"] = {}
		self.aggregate_result["magwin04"] = {}
		self.aggregate_result["magwin05"] = {}
		self.aggregate_result["magwinws"] = {}


	def parse_xml(self, filename):
		dom = xml.dom.minidom.parse(filename)

		for node1st in dom.documentElement.childNodes:
			for node2nd in node1st.childNodes:
				for node3rd in node2nd.childNodes:
					if node3rd.nodeName == "TimeCreated":
						self.timestamp.append(self.parse_timestamp(node3rd.attributes.getNamedItem("SystemTime").nodeValue))
						self.datanum += 1

					elif node3rd.nodeName == "Computer":
						self.hostname.append(self.parse_hostname(node3rd.firstChild.data))

					elif node3rd.nodeName == "Data" and node3rd.attributes.getNamedItem("Name").nodeValue == "TargetUserName":
						self.user.append(node3rd.firstChild.data)

					else:
						continue

		self.clean_data()


	def parse_timestamp(self, timestamp):
		# 2011-01-12T18:00:42.642395600Z
		pattern = "([0-9]+)-([0-9]+)-([0-9]+)T([0-9]+):([0-9]+):([0-9]+).([0-9]+)Z"

		# To be revised to compile only 1st time
		result = re.compile(pattern).search(timestamp)

		year = int(result.group(1))
		month = int(result.group(2))
		day = int(result.group(3))
		hour = int(result.group(4))
		minute = int(result.group(5))
		second = int(result.group(6))
		microsecond = int(int(result.group(7))/1000)

		return datetime.datetime(year, month, day, hour, minute, second, microsecond)


	def parse_hostname(self, computer):
		pattern = "magwin[0-9a-zA-Z]+"

		result = re.compile(pattern).search(computer)

		return result.group(0)


	def clean_data(self):
		i = 0

		while(i < self.datanum-1):
			if self.user[i] == "SYSTEM" or self.user[i] == "NETWORK SERVICE" or self.user[i] == "LOCAL SERVICE":
				self.timestamp.pop(i)
				self.user.pop(i)
				self.hostname.pop(i)
				self.datanum -= 1
				continue
			i += 1


	def init_aggregate_data(self):
		first_day = self.timestamp[0].date()
		last_day  = self.timestamp[len(self.timestamp)-1].date()

		day = first_day

		while day <= last_day:
			self.aggregate_result["magwin01"][day] = 0
			self.aggregate_result["magwin02"][day] = 0
			self.aggregate_result["magwin03"][day] = 0
			self.aggregate_result["magwin04"][day] = 0
			self.aggregate_result["magwin05"][day] = 0
			self.aggregate_result["magwinws"][day] = 0

			day += datetime.timedelta(days=1) 


	def aggregate_data_by_date(self):
		previous_date = None		# the date which this routine is focusing on, not today

		for i in range(0, self.datanum-1):
			previous_date = self.timestamp[i].date()

			if self.hostname[i] == "magwin01":
				self.aggregate_result["magwin01"][previous_date] += 1

			elif self.hostname[i] == "magwin02":
				self.aggregate_result["magwin02"][previous_date] += 1

			elif self.hostname[i] == "magwin03":
				self.aggregate_result["magwin03"][previous_date] += 1

			elif self.hostname[i] == "magwin04":
				self.aggregate_result["magwin04"][previous_date] += 1

			elif self.hostname[i] == "magwin05":
				self.aggregate_result["magwin05"][previous_date] += 1

			elif self.hostname[i] == "magwinws":
				self.aggregate_result["magwinws"][previous_date] += 1

			else:
				print "Unknown host is found"


	def print_history(self):
		for i in range(0, self.datanum-1):
			print self.timestamp[i],
			print self.hostname[i] + " " + self.user[i]


	def print_aggregate_result(self):
		for (i, j) in self.aggregate_result.items():
			print i,
			print j


	def print_sorted_aggregate_result(self):
		for i in sorted(self.aggregate_result["magwin01"].keys()):
			print i,
			print self.aggregate_result["magwin01"][i],
			print self.aggregate_result["magwin02"][i],
			print self.aggregate_result["magwin03"][i],
			print self.aggregate_result["magwin04"][i],
			print self.aggregate_result["magwin05"][i],
			print self.aggregate_result["magwinws"][i]


	def generate_output_file(self, filename):
		f = open(filename, "w")

		for i in sorted(self.aggregate_result["magwin01"].keys()):
			line = "%s %s %s %s %s %s %s\n" % (i, self.aggregate_result["magwin01"][i], self.aggregate_result["magwin02"][i], self.aggregate_result["magwin03"][i], self.aggregate_result["magwin04"][i], self.aggregate_result["magwin05"][i], self.aggregate_result["magwinws"][i])
			f.write(line)

		f.close()


if __name__ == "__main__":
	argc = len(sys.argv)
	argv = sys.argv

	if argc != 2:
		print "Usage: python this_program filename"
		sys.exit()

	filename = argv[1]

	log = Log()

	log.parse_xml(filename)
	## log.print_history()
	log.init_aggregate_data()
	log.aggregate_data_by_date()
	## log.print_aggregate_result()
	log.print_sorted_aggregate_result()

	log.generate_output_file("logon_output.dat")
