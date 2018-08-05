#!/bin/python

import os
import subprocess as sp
import re
import logging

logging.basicConfig(level=logging.DEBUG)

def doc():
	"""This script is used to find Mount point usage persentage and generate warning for same"""

warning_threshold=70
critical_threshold=90

Type=["ext2", "ext3", "ext4", "xfs", "vfat"]
type=str(["--type " + i for i in Type])

def repChar(x):
     regexChars = '[\[\'!@$*#,\]]'
     line = re.sub(regexChars,'',x)
     return line

disk_type=repChar(type)

def stat():
	disk_stat=sp.Popen(["df  --output=target,pcent "+ disk_type + "| sed '1d'"],stdout=sp.PIPE,shell=True).communicate()[0].strip().split("\n")
	for i in disk_stat:
		if int(i.split()[-1][:-1]) >= warning_threshold:
			logging.debug("Warning Message : Disk size of {0} reached to {1}".format(i[0],i.split()[1]))
		elif int(i.split()[-1][:-1]) >= critical_threshold:
			logging.debug("Critical Message : Disk size of {0} reached to {1}".format(i[0],i.split()[1]))
		
stat()
