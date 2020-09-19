#!/bin/bash
newline() {
    count=0
    new_line=n
    total_lines=$1
    while [ $count -ne $total_lines ]
    do
    echo $line
    let count=$count+1
    done }

rm -rf /tmp/kvm_guest_status
count=1
for i in `virsh list --all --name| grep -v ^$`
do 
    VM=$i                                                                      #Virtual Machines names
    disk=`virsh domblklist $i|sed '1d'| awk '{print $2}'| egrep -v '^-|$^'`    #Block disk file used in Virtual machine as Disk
    state=`virsh domstate $i`                                                  #Virtual machine state like running, shutdown, pause etc
    echo  "$count.  $i  $disk   $state  " >> /tmp/kvm_guest_status             #Gather data in /tmp/kvm_guest_status
    let count=$count+1
done

sed -i 's/shut off/poweroff/g' /tmp/kvm_guest_status
cat /tmp/kvm_guest_status| column -t
read -p "Which Virtual Machine's filesystem your like to mount-[1,2,3]: " number
vm=`grep ^$number /tmp/kvm_guest_status`
vm_status=`echo $vm | awk '{print $4}'`
if [ $vm_status != poweroff ];then  exit; fi
vm_name=`echo $vm | awk '{print $2}'`
vm_disk=`echo $vm | awk '{print $3}'`
vm_disk_size=`du -s -BM $vm_disk|awk '{print $1}' |sed 's/M//'`
mount_disk_avail=`df  -BM --output=avail  $vm_disk| sed '1d'|sed 's/M//'`
newline 3
echo ----Working on $vm_name----
available_size=`echo $mount_disk_avail - $vm_disk_size | bc`
available_size1=`echo $mount_disk_avail/$vm_disk_size |bc `
echo Available size on disk $available_size . is $available_size1 times greater than $vm_name

if [ $available_size1 -lt 3 ]; then  exit
else 
    newline 2
    echo "copy $vm_disk ... to ... $vm_disk.bkp"
    cp -rvfp $vm_disk $vm_disk.bkp
    newline 2
    echo "Rename org disk file $vm_disk ... to ... $vm_disk.org"
    mv $vm_disk $vm_disk.org
    newline 2
    echo "trying reclaiming Disk size"
    qemu-img convert -f raw -O qcow2 $vm_disk.bkp $vm_disk
    newline 4
    echo "Status of KVM Guest machine directory. 
    $vm_disk.bkp used while processing for reclaiming
    $vm_disk is original file prepared after reclaim.
    $vm_disk.org is orginal file"
    newline 2
    ls -lhtr `dirname $vm_disk`|awk 'NR>1'|awk '{print $5,"----",$9}'
fi

read -p "Do you like to run VM for checking $vm_name status" ack

if [ $ack == y] [ $ack == yes ];then
    virsh start $vm_name
fi
