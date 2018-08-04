#!/bin/python

import os
import subprocess as sp
import sys
import re

def doc():
	""" This script is used to find Disk size and its usage persentage """

warning_threshold=20

Type=["ext2", "ext3", "ext4", "xfs", "vfat"]
type=str(["--type " + i for i in Type])

def repChar(x):
     regexChars = '[\[\'!@$*#,\]]'
     line = re.sub(regexChars,'',x)
     return line

disk_type=repChar(type)

def Disk_stat():
	disk_stat=sp.Popen(["df  --output=target,pcent "+ disk_type + "| sed '1d'"],stdout=sp.PIPE,shell=True).communicate()[0].strip().split("\n")
	for i in disk_stat:
		if int(i.split()[-1][:-1]) >= warning_threshold:
			print "Warning Message : Disk size of ", i[0] ,"reached to", i.split()[1]
		
Disk_stat()
