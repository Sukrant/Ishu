#!/data/conda/bin/python

import subprocess as sp
import os
import sys
import libvirt
from platform import dist
import time

def usage():
    print """
                This script is used to delete VMs created on machine with KVM

                      We would delete snapshots before deleting Vms

                please used to describe command arguments like mentioned below


                 ----------------delete_vm.py <vm_name>----------------------
"""
Linux_dist=dist()[0]


#Libvirt connection, if failed exit over here only
libvirt_conn = libvirt.open('qemu:///system')
if libvirt_conn == None:
    print "Failed to open connection to qemu:///system \n"
    sys.exit()


#try to find Any VMs present or not
all_vm_defined=libvirt_conn.listDefinedDomains()
vm_names=[vms for vms in  all_vm_defined if "template" not in vms]
if not vm_names:
    print "No VM found, Exit ... \n"
    sys.exit()

def check_vm(vm_name=None):
    count=1
    global vm_dic
    vm_dic={}
    for vm in vm_names:
        if not vm in vm_dic:
            vm_dic[count]=vm
            count += 1
    for key, value in vm_dic.iteritems():
        print key, value
    if [vm_name for vm_name in vm_names if not vm_name]:
        print "Wrong VM... This", vm_name ,"VM is not defined \n"

#Virtual machine un-define
def undefine_vm(vm_name):
    try:
        cmd1="virsh undefine {0}".format(vm_name)
        sp.Popen(cmd1,stdout=sp.PIPE,shell=True)
        print "Undefine : ", vm_name, "\n"
    except:
        print "faced some issues while undefine Virtual Machine -",vm_name , "\n"
        sys.exit()

#Delete VM Disk and its directory
def delete_vm_disk(vm_name):
    cmd1="virsh domblklist {0} | sed -e '1,2d;/^$/d'| awk '{{print $2}}'".format(vm_name)
    disk_list=sp.Popen(cmd1,stdout=sp.PIPE,shell=True).communicate()[0].split('\n')[:-1]
    try:
        for disk in disk_list:
            os.remove(disk)
            print "Removed ",disk , "\n"
            try:
                os.rmdir(os.path.dirname(disk))
            except:
                print os.path.dirname(disk)," is not empty","\n"
    except:
        print "find some issues while deleting ",disk
        sys.exit()
#Delete VM Snapshot
def delete_snapshot(vm_name):
    cmd1="virsh snapshot-list {0}| sed -e '1,2d;/^$/d'| awk '{{print $1}}'".format(vm_name)
    snap_list=sp.Popen(cmd1,stdout=sp.PIPE,shell=True).communicate()[0].split()
    if not snap_list:
        print "No Snapshot of VM", vm_name, "\n"
    else:
        try:
            for snap in snap_list:
                cmd1="virsh snapshot-delete {0} {1}".format(vm_name,snap)
                sp.Popen(cmd1,stdout=sp.PIPE,shell=True)
                print "Removed snapshot",snap, "\n"
        except:
            print "faced some issues while deleting shopshot", snap, "\n"
            sys.exit()

if len(sys.argv) != 2:
    usage()
    delete=raw_input("------- >>>> Still need to delete VM -- y/Y/yes/Yes :")
    if delete == "y" or delete == "Y" or delete == "yes" or delete == "Yes":
        print """
            Below mentioned VM name, please choose your VM need to delete
                      templates would not allow to delete
            """
        check_vm()
        vm_number=input("Put your number:")
        if vm_number in vm_dic.keys(): #if provided number present
            vm_name=vm_dic[vm_number]
            try:
                delete_vm_disk(vm_name)
                delete_snapshot(vm_name)
                undefine_vm(vm_name)
            except:
                print "Find some issues while deleting VM",vm_name
                sys.exit()
        else:
            print "\n You provide wrong input ... Get Lost... \n"
    else:
        print "OK ... Exit"
elif len(sys.argv) == 2:
    vm_name=sys.argv[1]
    print "___________Below are Defined Virtual Machine_____________"
    check_vm()
    if vm_name in vm_dic.values():
        delete_vm_disk(vm_name)
        delete_snapshot(vm_name)
        undefine_vm(vm_name)
    else:
        print "Provided Virtual Machine", vm_name, "is Wrong"
