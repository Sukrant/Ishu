#!/data/conda/bin/python

import subprocess as sp
import os
import sys 

os_dis,os_maj = None,None 

''' Used to change hostname Os Linux machine 
    Capable of change hostname on Ubuntu/Redhat(5,6,7,8)/CentOS(5,6,7,8)
    This is depend on two files to know Machine details
        1. /etc/redhat-release
        2. /etc/os-release
    If Above files are not present, This will exit without change anythign on Machine    
'''

def os_cmd(cmd):
    '''This is capbale to run on Linux commands and provide Output and Error as return'''
    out, err = sp.Popen(cmd,stdout=sp.PIPE,stderr=sp.PIPE,shell=True).communicate()
    return out, err


def os_file_path():
    ''' This funtions is used to  find out OS file '''
    os_files = ["/etc/redhat-release", "/etc/os-release"]
    for file in os_files:
        if os.path.exists(file):
            return file
    sys.exit('No OS file exists')

def what_os(os_file):
    '''This function is used to find Os information'''
    global os_dis
    global os_maj
    if os_file == "/etc/redhat-release":
        with open("/etc/redhat-release") as file:
            content = file.read().split(" ")
            if [i for i in content if 'Linux' in content]:
                content.remove('Linux')
            if [i for i in content if content[0] == "CentOS"]:
                os_ver = ' '.join(content[0:3:2])
                os_dis = os_ver[0:6]
                os_maj = os_ver[7]
    elif os_file == "/etc/os-release":
        cmd = f"awk -F= '/PRETTY_NAME/{{split ($2,a,\" \"); print a[1]}}' {os_file}"
        out, err = os_cmd(cmd)
        if err:
            print("Unable to find OS Information")
            sys.exit()
        os_dis = out.decode('utf-8').split("\n")[0]
        if "Ubuntu" in os_dis:
            os_dis = "Ubuntu"
            cmd = "awk -F= '/PRETTY_NAME/{{split ($2,a,\" \"); print a[2]}}' /etc/os-release"
            out, err = os_cmd(cmd)
            if err:
                print("Unable to find OS information")
                sys.exit()
            os_maj = out.decode('utf-8').split("\n")[0]
            print(f'This Machine is {os_dis} {os_maj}')

def main(new_hostname):
    def change_hostname(new_hostname):
        ''' This fucntion is used to change hostname of Machine   '''
        if os_dis == "CentOS" and os_maj.startswith("6"):
            cmd1 = "sed -i 's/HOSTNAME=.*/HOSTNAME={0}/g' /etc/sysconfig/network".format(new_hostname)
            sp.Popen(cmd1, stdout=sp.PIPE, shell=True)
            cmd2 = "hostname {0}".format(new_hostname)
            sp.Popen(cmd2, stdout=sp.PIPE, shell=True)
        elif (os_dis == "CentOS" and (os_maj.startswith("7") or os_maj.startswith("8"))) \
                or os_dis == "Ubuntu":
            cmd1 = "echo {} > /etc/hostname".format(new_hostname)
            out, err = os_cmd(cmd1)
            if err:
                print(f'unable to save ew-hostname: {new_hostname} in /etc/hostname {err}')
            cmd2 = "hostname {0}".format(new_hostname)
            out, err = os_cmd(cmd2)
            if err:
                print(f'unable to run hostname command')

    if len(sys.argv) < 2:
        print("You didn't mentioned New Hostname.")
        response = input("Do you like to change: (y/n)")
        if response == 'y' or response == 'Y' or response == 'yes' or response == 'Yes':
            new_hostname = input("What should new hostname for this Machine :")
            os_file = os_file_path
            what_os(os_file)
            change_hostname(new_hostname)
        else:
            print("Ok.. Exit")
    elif len(sys.argv) == 2:
        os_file = os_file_path()
        what_os(os_file)
        change_hostname(new_hostname)
    elif len(sys.argv) > 2:
            print("You can only provide Hostname with script.")

if __name__ == '__main__':
    main(sys.argv[1])
