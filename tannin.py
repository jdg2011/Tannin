#-------------------------------------------------------------------------------
# Name:        Tannin
# Purpose:     To store passwords encrypted with Tea.lock in a disintegrated fashion so as to decrease malicious accessibility of stored passwords while maintaining ease of use.
#
# Author:      Jordan Gloor
#
# Created:     08/10/2020
# Copyright:   (c) gloorj 2020
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#One helpful feature would be using a keyword for each entry, probably stored in a separate file. This would avoid reliance on proper order for retrieval and helps the user remember which entry is which. It would need to detect and reject previously used keywords.

import os

def greeting():
    print("-----------------------------------\rRunning Tannin Version 0.0.1 Alpha\r-----------------------------------\r")

def file_check():
    if os.path.exists("tannin_keys.txt"):
        print("Key directory detected!")
    else:
        print("Creating new key directory file...")
    if os.path.exists("tannin_passwords.txt"):
        print("Password directory detected!")
    else:
        print("Creating new password directory file...")

def select_task():
    selected_task = str(input("Enter <s> to store <r> to retrieve <h> to get help: "))
    if selected_task == "s":
        print("Beginning storage protocol...")
        store()
    elif selected_task == "r":
        print("Beginning retrieval protocol...")
    elif selected_task == "h": print("Help page not yet created!")
    else:
        print("\""+selected_task+"\"Bad input. Try again.")

def store():
    keyword_to_store = str(input("Enter a keyword: "))
    password_to_store = str(input("Enter a password to be stored: "))
    print("Storing keyword...")
    keyword_f = open("tannin_keys.txt", "a")
    keyword_f.write(keyword_to_store+"\r")
    keyword_f.close()
    print("Storing password...")
    password_f = open("tannin_passwords.txt", "a")
    password_f.write(password_to_store+"\r")
    password_f.close()
    print("File writing complete!")

greeting()
file_check()
select_task()
#store()