#!/usr/bin/python3.6

##
##This file could used to work for some basic mysql operations
##

import mysql.connector
import os
import subprocess as sp
import sys
import getpass
User = ""
Host = ""


def dbs_connection():
    print(" \n Please provide Database details :- \n")
    global User
    global Host
    if not User and not Host:
        User = input("What is your Username: ")
        Host = input("What is your host to connect: ")
    else:
        print("We have already have some details for MySQL connection :\n")
        print("User = ",User , "and Host = ",Host, "\t\tplease provide password again...\n")
    Passwd = getpass.getpass("What is you password : ")
    cnx = mysql.connector.connect(user=User, host=Host, password=Passwd)
    return cnx


def show_dbs():
    cnx = dbs_connection()
    cur = cnx.cursor()
    cur.execute("show databases")
    print("\nBelow are Database present in MySQL Instance\n")
    count = 1
    for i in cur:
        print(count, i[0].decode())
        count = count+1
    cur.close()
    cnx.close()
    return_fun()


def creating_database():
    cnx = dbs_connection()
    cur = cnx.cursor()
    Database = input("What database need to create : ")
    sql = "create database {}".format(Database)
    cur.execute(sql)
    cur.close()
    cnx.close()
    return_fun()


def deleting_database():
    cnx = dbs_connection()
    cur = cnx.cursor()
    Database = input("What database need to delete : ")
    sql = "drop database {}".format(Database)
    cur.execute(sql)
    cur.close()
    cnx.close()
    return_fun()


def user_creation():
    cnx = dbs_connection()
    cur = cnx.cursor()
    new_user = input("New user name need to create (test@192.168.123.46 or test@localhost) : ")
    new_passwd = getpass.getpass("New user password : ")
    sql = "CREATE USER {0} IDENTIFIED BY '{1}'".format(new_user, new_passwd)
    cur.execute(sql)
    cur.close()
    cnx.close()
    return_fun()


def user_deletion():
    cnx = dbs_connection()
    cur = cnx.cursor()
    sql1 = "select user,host from mysql.user"
    cur.execute(sql1)
    print("\nBelow are Users present in database instance:  \n")
    for i in cur:
        print(i[0].decode() + '@' + i[1].decode())
    del_user = input("\nplease select which user need to delete (test@192.168.123.46 or test@localhost) :")
    sql2 = "drop user {0}".format(del_user)
    cur.execute(sql2)
    cur.close()
    cnx.close()
    return_fun()


def to_do(user_in):
    if user_in == "1":
        creating_database()
    elif user_in == "2":
        deleting_database()
    elif user_in == "3":
        show_dbs()
    elif user_in == "6":
        user_creation()
    elif user_in == "7":
        user_deletion()
    elif user_in == "q" or user_in == "quit":
        print("Ok Exit...")
        sys.exit()


def main():
    print("\nWhich activity you need to perform with Database\n")
    print("""
              1. Creation of database.
              2. Deletion of database.
              3. Show database.
              4. Assign Grants to user.
              5. Remove Grants to user.
              6. Show all users and their grants.
              6. Creation of user.
              7. Deletion of user.\n""")

    user_in = input("Write down number like 1/2/3 :")
    user_value = ("1", "2", "3", "4", "5", "6", "7", "q", "quit")
    if user_in in user_value:
        to_do(user_in)
    else:
        print("Wrong Input. Exit...")
        sys.exit()


def return_fun():
    return_code = input("\nSo you still need to do another operation step (y/n): ")
    if return_code == "y" or return_code == "Y" or return_code == "yes" or return_code == "Yes":
        main()
    elif return_code == "n" or return_code == "N" or return_code == "no" or return_code == "No":
        print("Ok Exit...")
        sys.exit()
    else:
        print("Wrong Input. Exit...")
        sys.exit()


if __name__ == "__main__":
    main()
