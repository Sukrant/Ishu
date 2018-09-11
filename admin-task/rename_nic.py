#!/usr/bin/python

import subprocess as sp 
import os
import sys

def usage():
		print """

			rename_nic.py <old-nic-name>  <new-nic_name>

					"""

# Check Uid
if os.getuid() != 0:
    print "Only Root user should run it"
    sys.exit()

#
#This will going to do changes once all pre-checks passes, please consider Linux platform Distributions
#
def new_interface(old_interface,new_interface):
    print "Changing interface configuration File"
    cmd4="ip link set {0} down".format(old_interface)
    sp.Popen(cmd4,stdout=sp.PIPE,shell=True)
    cmd1="cp -fp '/etc/sysconfig/network-scripts/ifcfg-{0}' '/etc/sysconfig/network-scripts/ifcfg-{1}'".format(old_interface,new_interface)
    cmd2="sed -i 's/DEVICE=.*/DEVICE={0}/g' '/etc/sysconfig/network-scripts/ifcfg-{1}'".format(new_interface,new_interface)
    sp.Popen(cmd1,stdout=sp.PIPE,shell=True)
    sp.Popen(cmd2,stdout=sp.PIPE,shell=True)
    print "Changing interface name on udev rules"
    cmd3="sed -i 's/{0}/{1}/g' /etc/udev/rules.d/70-persistent-net.rules".format(old_interface,new_interface)
    sp.Popen(cmd3,stdout=sp.PIPE,shell=True)
    cmd5="ip link set {0} name {1}".format(old_interface,new_interface)
    sp.Popen(cmd5,stdout=sp.PIPE,shell=True)
    cmd6="ifup {0}".format(new_interface)
    sp.Popen(cmd6,stdout=sp.PIPE,shell=True)
    cmd7="rm -rf '/etc/sysconfig/network-scripts/ifcfg-{0}'".format(old_interface)
    sp.Popen(cmd7,stdout=sp.PIPE,shell=True)

#
#Will check interfaces name provides are correct, like old one should present and new one should not have used any where.
#
def check_interface():
    print "Checking interface with correct name"
#    cmd1="ls -l /sys/class/net| grep pci| awk '{print $9}'| tr '\n' ' '| xargs echo"
#    cmd2="ls -1 /sys/class/net| tr '\n' ' '| xargs echo"
    cmd3="ip addr list| grep 'scope global'| awk '{print $NF}'"
#    old_interfaces_name=list(sp.Popen(cmd1,stdout=sp.PIPE,shell=True).communicate())[0].strip().split()
#    all_interfaces_name=list(sp.Popen(cmd2,stdout=sp.PIPE,shell=True).communicate())[0].strip().split()
    existing_interfaces_name=list(sp.Popen(cmd3,stdout=sp.PIPE,shell=True).communicate())[0].strip().split()
    if sys.argv[1] in existing_interfaces_name:
        if sys.argv[2] not in existing_interfaces_name:
	    new_interface(sys.argv[1],sys.argv[2])
    	else:
	     print "New intergace name",sys.argv[2],"is already taken"
	     print sys.argv[2]
    else:
	 print "Old interface name", sys.argv[1],"is not Exit"
	 print sys.argv[1]
         


#
#Will check sufficient argument provided, if not will ask 
#

if len(sys.argv) != 3:
	print "You didn't mentioned old and new interfaces names."
	usage()
elif len(sys.argv) == 3:
	check_interface()
elif len(sys.argv) < 3:
	print "You can only provide Hostname with script"
	usage()
