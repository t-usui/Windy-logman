#!/usr/bin/python

import os
import re

kLogDirectory = "../logs/"
kLogExtension = ".xml"

def add_log_string(log_number, log_string):
	global kLogDirectory
	file_name = kLogDirectory + str(log_number) + kLogExtension

	f = open(file_name, "r")
	log_string += f.read()

	f.close()

	return log_string

def remove_file_format_tags(log_string):
	pattern = "</Events>.+?<Events>"

	p = re.compile(pattern, re.DOTALL)
	log_string = p.sub("", log_string)

	return log_string

if __name__ == "__main__":
	log_string = ""

	for i in range(1, 131):
		log_string = add_log_string(i, log_string)
		print "Log[" + str(i) + "] finished to marge"

	log_string = remove_file_format_tags(log_string)

	f = open("./marged_log.xml", "w")
	f.write(log_string)

	f.close()

