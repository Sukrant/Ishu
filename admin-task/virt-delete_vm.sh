#!/bin/bash 
###
##This script is used to delete VMs with their snapshots
###

function usage() {
    cat << EOM
    Detail and usuage of script
    ===========================
    
    This scipt is used to delete Virtual machine from Host machine with their snapshots
    
    VMs name thise contain tempplate will no be deleted

    How to run this script 
    ======================

    ./virt-delete.sh vm-name

EOM
}

vm_name=$1
if [ -z $vm_name ]; then
    echo "Error: You didn't provide any Virtual Machine"
    exit 1
elif echo $vm_name | grep -q template
then
    echo "Error: Template are not allow to delete through this script"
    echo "Error: Get Out..."
    exit 2
fi 

vm_names=`/usr/bin/virsh list --all --name | sed '/^$/d'`
if echo $vm_names | grep -qw $vm_name
then
    :
else
    echo "Error: Provider $vm_name is not in Virtual Machine List"
    exit 3 
fi 

check_vm_stat()
{
    vm_state=`virsh domstate $vm_name | sed '/^$/d'`
    if [ "$vm_state" != "shut off" ]
    then 
        echo "Error: You need to shutdown Virtual Machine $vm_name first."
        exit 4 
    fi 
}

delete_snapshot()
{
    vm_snapshot=`virsh snapshot-list $vm_name| sed -e '1,2d;/^$/d'| awk '{print $1}'`
    if [ $? -ne 0 ]; then 
        echo "Error: Unable to find snapshot details of $vm_name"
        exit 5 
    elif [ -z $vm_snapshot ];
    then
        echo "Info: No snapshot for this Virtual Machine $vm_name " 
    else
        for snaphost in vm_snapshot
        do 
            echo "Info: Deleting snapshot $snapshot of Virtual machine $vm_name"
            virsh snapshot-delete $vm_name $snapshot 
        done
    fi 
}


disks=`virsh domblklist $vm_name | awk  '{if($2~"^/") {print $2}}'| tr '\n' ' '`

if [ $# -lt 1 ]; then
    usage
elif
    [ $# -gt 2 ];then 
    echo -e "Info: ______No use for below arguments. Will only take first argument -- $1______ \n \n"
    while (( $# )); do 
        echo -n " $2 "
        shift 
    done
    echo -e "\n"
fi

if [ -z `virsh list --all --name | grep -x $vm_name` ]; then 
    echo "Info : No Virtual Machine"
else
    check_vm_stat
    delete_snapshot
    for disk in $disks;
    do 
        echo "Info : Deleting disk $disk for Virtual Machine $vm_name"
        rm -rf $disk  
        if [ -z $(ls -1 `dirname $disk`) ];
        then
            echo "Info : Deleting Directory `dirname $disk` "
            rm -rf `dirname $disk`
        fi 
    done

    virsh undefine $vm_name
fi 
