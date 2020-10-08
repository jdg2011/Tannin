#-------------------------------------------------------------------------------
# Name:        Tannin
# Purpose:     To store passwords encrypted with Tea.lock in a disintegrated fashion so as to decrease malicious accessibility of stored passwords while maintaining ease of use.
#
# Author:      Jordan Gloor
#
# Created:     08/10/2020
# Copyright:   (c) Jordan Gloor 2020
# Licence:     MIT License
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
#-------------------------------------------------------------------------------

#Need to divide password input into two equal segments and store them in two separate files.
#Eventually it should verify the input is exactly two 200 characters long.
#Need to figure out how to ensure escape characters are handled properly.

tannin_version = "0.0.1 Alpha"

import os
import datetime

def greeting():
    print("Running Tannin Version "+tannin_version)

def file_check():
    global log_file
    log_file = open("log.txt", "w")
    log_file.write("Log file created "+str(datetime.datetime.now())+" running version "+tannin_version+"\r")
    if os.path.exists("tannin_keys.txt"):
        log_file.write(str(datetime.datetime.now())+" Key directory detected!\r")
    else:
        log_file.write(str(datetime.datetime.now())+" Creating new key directory file...\r")
    if os.path.exists("tannin_passwords1.txt"):
        log_file.write(str(datetime.datetime.now())+" Password directory 1 detected!\r")
    if os.path.exists("tannin_passwords2.txt"):
        log_file.write(str(datetime.datetime.now())+" Password directory 2 detected!\r")
    else:
        log_file.write(str(datetime.datetime.now())+" Creating new password directory files...\r")

def select_task():
    x = 0
    while x == 0:
        selected_task = str(input("Enter <s> to store <r> to retrieve <h> to get help: "))
        if selected_task == "s":
            log_file.write(str(datetime.datetime.now())+" Beginning storage protocol...\r")
            x = 1
            store()
        elif selected_task == "r":
            log_file.write(str(datetime.datetime.now())+" Beginning retrieval protocol...\r")
            print("Retrieval function not yet implemented!")
            continue
        elif selected_task == "h":
            print("Help page not yet created!")
            continue
        else:
            print("\""+selected_task+"\" bad input. Try again.")
            continue


def store():
    keyword_to_store = str(input("Enter a keyword: "))
    password_to_store = str(input("Enter a password to be stored: "))
    log_file.write(str(datetime.datetime.now())+" Storing keyword <"+keyword_to_store+">\r")
    keyword_file = open("tannin_keys.txt", "a")
    keyword_file.write(keyword_to_store+"\r")
    keyword_file.close()
    log_file.write(str(datetime.datetime.now())+" Storing password <"+password_to_store+">\r")
    password_file1 = open("tannin_passwords1.txt", "a")
    password_file1.write(password_to_store[0]+"\r")
    password_file1.close()
    password_file2 = open("tannin_passwords2.txt", "a")
    password_file2.write(password_to_store[1]+"\r")
    password_file2.close()
    print("File writing complete!")
    log_file.write(str(datetime.datetime.now())+" File writing complete!")

greeting()
file_check()
select_task()
log_file.close()
