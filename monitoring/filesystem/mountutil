#!/bin/python

import os
import subprocess as sp
import re

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
			print "Warning Message : Disk size of ", i[0] ,"reached to", i.split()[1]
		elif int(i.split()[-1][:-1]) >= critical_threshold:
			print "Critical Message : Disk size of ", i[0] ,"reached to", i.split()[1]
		
stat()
