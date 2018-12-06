#!/bin/bash

#Only user root should run this script

red='\e[1;31m%s\e[0m\n'
green='\e[1;32m%s\e[0m\n'
site=`hostname| cut -d. -f 2 --complement`
node_name=`hostname`
hostname=`hostname -n`

if [ $EUID -ne 0 ]; then
	printf "$red" "This script should only through root. Exit ..."
	exit 1
fi

if [ $hostname != "systems1"] || [ $hostname != "fileserver1"];then
	printf "$red" "This script should only run on systems1 and fileserver1, Exit ..."
	exit 1
fi 



service_check(service_names){
	for i in service_names
	do 
		service $i status
		case "$?" in
			0)
				printf "$green" "Service $i -- Running";;
			3)
				printf "$red" "Service $i -- It seems service is down";;
			1) 
				printf "$red" "Service $i -- It seems $i is not installed";;
			*)
				printf "$red" "Service $i -- Unrecognized status";;
			esac
		}
	done 

dns_check(site){
	#checking of Zone file
	for i in `ipinfo -s $site| awk -F \| '{print $2}'| sed '/Prefix/d;/^$/d;s/^ //;s/\/.*//;s/^/zone-/;s/.0$//'`
	do
		echo -n "Zone $i ---"
		if [ -f /var/name/master.$site/$i ]; then
			printf "$green" "File /var/name/master.$site/$i present"
		else
			printf "$red" "File not found"
		fi
done
	#Check named.conf file mapping
	if [ readlink /etc/named.conf != /var/named/configs/named.conf.$site.master ]; then
		printf "$red" "/etc/named.conf is link to `readlink /etc/named.conf`"
	else
		printf "$green" "/etc/named.conf is link to `readlink /etc/named.conf`"
	fi
	# check DNS host -l Domain
	if host -l $site > /dev/null 2>&1; then
		printf "$green" Local domain host list --- OK
	else
		printf "$red" Local domain host list is --- not OK
	fi
}

mount_point($node_name){
	if [[ $site =~ *.off.* ]];then
		printf "green" This is office location, we assume there is no fileserver present on Office location 
		return 0
		sys_mount="/n/systems1/homesnaps,/n/infra"
		file_mount="/n/fileserver1,/n/infrad,/n/infra"
	if [ $hostname == "systems1" ]; then 

}


