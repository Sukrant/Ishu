#!/bin/bash
/sbin/modprobe nbd

if [ ! -d /mnt/KVM_nbd_mounts ];then
    mkdir /mnt/KVM_nbd_mounts
fi

#Function to find next available nbd device
available_nbd() 
{
    for i in `echo /dev/nbd{0,1,2,3,4,5,6,7,8,9,10}`; do echo `ps h -fC qemu-nbd | awk '{print $10}'| awk -F= '{print $2}'`| grep -q $i; if [ $? != 0 ]; then echo $i;fi ; done| head -1
}

LVM_fs() 
{
    pvscan --cache
    vg_name=`pvs $1| awk '{print $2}'| sed '1d'`
    vgchange -ay
    lv_name=`vgs $vg_name -o +lv_name| grep -v swap | awk '{print $NF}'| sed '1d'`
    mount /dev/$vg_name/$lv_name /mnt/KVM_nbd_mounts/$2
}

Linux_fs() 
{
    mount $1 $2
}

#This count is just used to gather numbers in /tmp/nbd_status
count=1

echo  "S.N VM Device State Connection Socket" > /tmp/nbd_status
#
#For loop for gathering data in /tmp/nbd_status
#
for i in `virsh list --all --name| grep -v ^$`
do 
    if [ ! -d /mnt/KVM_nbd_mounts/$i ];then
        mkdir /mnt/KVM_nbd_mounts/$i
    fi
    VM=$i 											#Virtual Machines names
    disk=`virsh domblklist $i|sed '1d'| awk '{print $2}'| egrep -v '^-|$^'`			#Block disk file used in Virtual machine as Disk
    state=`virsh domstate $i`								#Virtual machine state like running, shutdown, pause etc
    connection=`ps h -fC qemu-nbd| awk '{print $11}'| grep -q $disk; echo $?`		#Connection with nbd disk. 0 - connected / 1 - notconnected
    socket=`ps h -fC qemu-nbd| grep $disk|awk '{print $10}'| cut -f 2 -d=`			#NBD device name
    echo  "$count.  $i  $disk   $state  $connection $socket" >> /tmp/nbd_status		#Gather data in /tmp/nbd_status

    let count=$count+1
done

sed -i 's/shut off/poweroff/g' /tmp/nbd_status
cat /tmp/nbd_status| column -t
echo "

This script can work on KVM Virtual machine filesystem

"
read -p "Which Virtual Machine's filesystem your like to mount-[1,2,3]: " number
vm=`grep ^$number /tmp/nbd_status`
vm_name=`echo $vm | awk '{print $2}'`

#connection to NBD device or not
if [ "`echo $vm | awk '{print $5}'`" == 1 ]; then
    nbd=$(available_nbd)									#Next available NBD
    qemu-nbd --connect=$nbd `echo $vm | awk '{print $3}'`					#Connect to NBD device
    #File-system Type used in Virtual machine
    f_type=`sfdisk -l $nbd| awk '$1~"nbd"'| egrep -v '\*|swap'| awk '{print $NF}'`
    nbd_part=`sfdisk -l $nbd| awk '$1~"nbd"'| egrep -v '\*|swap'| awk '{print $1}'`

    if [ $f_type == "Linux" ];then
        Linux_fs $nbd_part /mnt/KVM_nbd_mounts/$vm_name
    elif [ $f_type == "LVM" ];then
        LVM_fs $nbd_part $vm_name
    fi

elif [ "`echo $vm | awk '{print $5}'`" == 0 ]; then

    nbd=`echo $vm | awk '{print $6}'`

    nbd_part=`sfdisk -l $nbd| awk '$1~"nbd"'| egrep -v '\*|swap'| awk '{print $1}'`
    f_type=`sfdisk -l $nbd| awk '$1~"nbd"'| egrep -v '\*|swap'| awk '{print $NF}'`
    if [ $f_type == "Linux" ];then
        Linux_fs $nbd_part /mnt/KVM_nbd_mounts/$vm_name
    elif [ $f_type == "LVM" ];then
        LVM_fs $nbd_part $vm_name
    fi
fi
