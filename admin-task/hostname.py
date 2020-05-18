#!/data/conda/bin/python

import subprocess as sp 
import os
import sys


def os_cmd(cmd):
    out,err = sp.Popen(cmd,stdout=sp.PIPE,stderr=sp.PIPE,shell=True).communicate()
    return out,err

if not os.path.exists("/etc/os-release"):
    sys.exit(f'/etc/os-release doesn\'t . Unable to find OS')


cmd = "awk -F= '/PRETTY_NAME/{{split ($2,a,\" \"); print a[1]}}' /etc/os-release"
out,err = os_cmd(cmd)
if err:
    print("Unable to find OS Information")
    sys.exit()
os_dis = out.decode('utf-8').split("\n")[0]
if "CentOS" in os_dis:
    os_dis = "CentOS"
    cmd = "awk -F= '/PRETTY_NAME/{{split ($2,a,\" \"); print a[3]}}' /etc/os-release"
    out,err=os_cmd(cmd)
    if err:
        print("Unable to find OS information")
        sys.exit()
    os_maj = out.decode('utf-8').split("\n")[0]
    print(f'This Machine is {os_dis} {os_maj}')
elif "Ubuntu" in os_dis:
    os_dis = "Ubuntu"
    cmd = "awk -F= '/PRETTY_NAME/{{split ($2,a,\" \"); print a[2]}}' /etc/os-release"
    out,err=os_cmd(cmd)
    if err:
        print("Unable to find OS information")
        sys.exit()
    os_maj = out.decode('utf-8').split("\n")[0]
    print(f'This Machine is {os_dis} {os_maj}')


def change_hostname(new_hostname):
    if os_dis == "CentOS" and os_maj.startswith("6"):
        cmd1 = "sed -i 's/HOSTNAME=.*/HOSTNAME={0}/g' /etc/sysconfig/network".format(new_hostname)
        sp.Popen(cmd1,stdout=sp.PIPE,shell=True)
        cmd2 = "hostname {0}".format(new_hostname)
        sp.Popen(cmd2,stdout=sp.PIPE,shell=True)
    elif (os_dis == "CentOS" and (os_maj.startswith("7") or os_maj.startswith("8"))) \
            or os_dis == "Ubuntu":
        cmd1 = "echo {} > /etc/hostname".format(new_hostname)
        out,err = os_cmd(cmd1)
        if err:
            print(f'unable to save ew-hostname: {new_hostname} in /etc/hostname {err}')
        cmd2 = "hostname {0}".format(new_hostname)
        out,err = os_cmd(cmd2)
        if err:
            print(f'unable to run hostname command')
            
if len(sys.argv) < 2:
    print("You didn't mentioned New Hostname.")
    response=input("Do you like to change: (y/n)")
    if response == 'y' or response == 'Y' or response == 'yes' or response == 'Yes' :
        new_hostname=input("What should new hostname for this Machine :")
        change_hostname(new_hostname)
    else:
        print("Ok.. Exit")
elif len(sys.argv) == 2:
	new_hostname=sys.argv[1]
	change_hostname(new_hostname)
elif len(sys.argv) > 2:
	print("You can only provide Hostname with script.")
