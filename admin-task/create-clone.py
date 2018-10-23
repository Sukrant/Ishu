#!/usr/bin/python

import subprocess as sp 
import os
import sys
import libvirt
from platform import dist

def usage():
    print  """

    ##############################################################################################################
    This script is used to create clone of already existing template Virtual Machines 

    This will also mount mount its File-System in /mnt/virtual-machine directory and copy 

    some admin scripts and SSH public keys for password-less authentication.

    It's quite easy to use this script because it will ask user inputs if proper arguments not used during run-time.
    ################################################################################################################



    ----------------              ./create-clone.py <template-name> <vm-name>              -------------------------
    

    """

Linux_dist=dist()[0]
if Linux_dist != "centos" or Linux_dist != "redhat":
    print """
    
    #################################################    
    This script is only for CentOS or RedHat Machines
    #################################################
    
    """
#    sys.exit()

libvirt_conn = libvirt.open('qemu:///system')
if libvirt_conn == None:
    print "Failed to open connection to qemu:///system"
    sys.exit()


def create_clone(template_name,vm_name):
	try:
		cmd1="virt-clone -o {0} -n {1} -f /data/vm_images/{2}/system.img.".format(template_name,vm_name,vm_name)
		sp.Popen(cmd1,stdout=sp.PIPE,shell=True)
	except:
		print "There are some issues while cloning  Virtual machine, please do it manually"

def vm_checking(vm_name):
	libvirt_conn = libvirt.open('qemu:///system')
	vm_list=libvirt_conn.listDefinedDomains()
	if vm_name in vm_list:
		print "Virtual machine name is already taken. Exiting"
		ID=vm.name.ID()
		if ID == -1:
			print vm_name + "is shutdown state"
		else:
			print "The ID of " + vm_name +" is "+ str(ID)

def vm_dir_checking(vm_name):
	if os.path.isdir("/data/vm_images/%s" % vm_name):
		print " Virtual machine directory already exist, please taken care of. Exiting "
		sys.exit()
	else:
		os.mkdir("/data/vm_images/%s" % vm_name)


if len(sys.argv) != 3:
	usage()
	clone=raw_input("------- >>>> Still need to create clone :")
        if clone == "y" or clone == "Y" or clone == "yes" or clone == "Yes":
		print """

		Below mentioned templates name, please choose your required template

		"""
		vm_names=libvirt_conn.listDefinedDomains()
		template_names=[vms for vms in vm_names if "template" in vms]
		count=1
		template_dic={}
		for vm in template_names:
			if not vm in template_dic:
				template_dic[count]=vm
				count=count+1
		for key, value in template_dic.iteritems():
			print key, value
		template_number=input("Put your number:")
                if template_number in template_dic.keys():
		    print "Only new name would be acceptable,Below are existing one : "
		    for i in [vm for vm in vm_names if "templat" not in vm]:
			print i
			vm_name=raw_input(":-   What would be Virtual Machine Name")
		else:
		    print "Provided template number is not correct , Exit"
		    sys.exit()
	else:
		print " Wrong input ..Exit... "	

