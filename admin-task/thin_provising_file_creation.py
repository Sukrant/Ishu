#!/data/conda/bin/python

import subprocess as sp
import os
import sys

def file_creation():
    diretory_name = input("\nIn which directory you like create file : ")
    file_name = input("\nplease mentioned File name (Only file name not complete path, like vdisk1): ")
    file_path=os.path.join(diretory_name, file_name)
    if "/" in file_name:
        sys.exit("\n Wrong file name. Get Out \n")
    elif os.path.exists(file_path):
        sys.exit("File already exits.. Exit.. ")
    file_size = input("\n Please mentioned file size in MB (Default Size 5GB) : ")
    if int(file_size) > 20480:
        sys.exit("\n Maximum File Size: 20 GB. Exit ...   \n")
    if not os.path.exists(diretory_name):
        os.makedirs(diretory_name)
    cmd = "qemu-img create -f qcow2 {0} -o size={1}M,preallocation=metadata".format(file_path,file_size)
    os.system(cmd)
    if os.path.isfile(file_path):
        print("file ",file_path," created\n")

if __name__ == "__main__":
    file_creation()
