#!/usr/bin/python

import subprocess as sp 
import os
import sys

def change_hostname(new_hostname):
               print "Changing Hostname configuration File"
               cmd1="sed -i 's/HOSTNAME=.*/HOSTNAME={0}/g' /etc/sysconfig/network".format(new_hostname)
               sp.Popen(cmd1,stdout=sp.PIPE,shell=True)
               print "Changing Hostname on Shell"
               cmd2="hostname {0}".format(new_hostname)
               sp.Popen(cmd2,stdout=sp.PIPE,shell=True)

if len(sys.argv) < 2:
print "You didn't mentioned New Hostname."
response=raw_input("Do you like to change: (y/n)")
       if response == 'y' or response == 'Y' or response == 'yes' or response == 'Yes' :
               new_hostname=raw_input("What should new hostname for this Machine :")
change_hostname(new_hostname)
else:
print "Ok.. Exit"	
elif len(sys.argv) == 2:
new_hostname=sys.argv[1]
change_hostname(new_hostname)
elif len(sys.argv) > 2:
print "You can only provide Hostname with script"
