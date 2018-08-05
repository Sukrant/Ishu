#!/usr/bin/python

import subprocess as sp
service_name="http"

def service_stat(service_name):
	port=sp.Popen("netstat -ntlp| grep " + service_name + " | awk '{split($4,a,\":\")} {print a[length(a)]}'",stdout=sp.PIPE,shell=True).communicate()[0].rstrip().split("\n")	
	if port:
		print service_name ,"is running and Listening on TCP port : ", port
	else:
		print service_name ,"is not running"

service_stat(service_name)
