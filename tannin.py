#-------------------------------------------------------------------------------
# Name:        Tannin
# Purpose:     To store hashes encrypted with Tea.lock in a disintegrated fashion so as to decrease malicious accessibility of stored hashes while maintaining ease of use.
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

#Need to figure out how to ensure escape characters are handled properly.
#The file_check function should eventually warn users when only one (non-empty) hash library is present and ask what they'd like to do (retry, overwrite, quit)
#The storage process should also verify that the given keyword has not already been used
#File check should happen at the start of every command prompt

tannin_version = "0.2.1 \"Stay\""

import pyperclip
import os
import datetime

def greeting():
	print("Welcome to Tannin")
	print("version "+tannin_version+"\n\n")

def file_check():
	global log_file
	log_file = open("log.txt", "w")
	log_file.write("Log file created "+str(datetime.datetime.now())+" running version "+tannin_version+"\r")
	global file_status
	file_status = "ok"
	if os.path.exists("keys.txt"):
		log_file.write(str(datetime.datetime.now())+" Key directory found.\r")
	else:
		log_file.write(str(datetime.datetime.now())+" Key directory not found. New file will be created.\r")
		file_status = "bad"
	if os.path.exists("hashes1.txt") and os.path.exists("hashes2.txt"):
		log_file.write(str(datetime.datetime.now())+" hash directories found.\r")
	else:
		log_file.write(str(datetime.datetime.now())+" hash directories not found. New file will be created.\r")
		file_status = "bad"

def get_command():
	x = 0
	while x == 0:
		global option1
		command = str(input("Enter command: "))
		if command == "s" or command == "store":
			return "store"
		elif command == "s -p" or command == "store -p":
			option1 = "p"
			return "store"
		elif command == "r" or command == "retrieve":
			return "retrieve"
		elif command == "r -c" or command == "retrieve -c":
			option1 = "c"
			return "retrieve"
		elif command == "h" or command == "help":
			return "help"
		elif command == "q" or command == "quit":
			return "quit"
		elif command == "w" or command == "wipe":
			return "wipe"
		elif command == "l" or command == "list":
			return "list"
		elif command == "c" or command == "copy":
			return "copy"
		else:
			print("\""+command+"\" bad input. Try again.")
			log_file.write(str(datetime.datetime.now())+" User attempted invalid input. Trying again...\r")
			continue

def store():
	keyword_to_store = str(input("Enter a keyword: "))
	if option1 == "p":
		log_file.write(str(datetime.datetime.now())+" Attempting to pull hash from clipboard...\r")
		print("Getting hash from clipboard...")
		hash_to_store = pyperclip.paste()
	else:
		hash_to_store = str(input("Enter a hash to be stored: "))
	if len(hash_to_store) != 200:
		print("Entered length is "+str(len(hash_to_store))+". hash must equal 200 characters.\r")
		log_file.write(str(datetime.datetime.now())+" User entered hash not length 200.\r")
	else:
		log_file.write(str(datetime.datetime.now())+" Successful keyword and hash input. Storing keyword...\r")
		keyword_file = open("keys.txt", "a")
		keyword_file.write(keyword_to_store+"\r")
		keyword_file.close()
		log_file.write(str(datetime.datetime.now())+" Storing hash...\r")
		hash_file1 = open("hashes1.txt", "a")
		hash_file1.write(hash_to_store[0:100]+"\r")
		hash_file1.close()
		hash_file2 = open("hashes2.txt", "a")
		hash_file2.write(hash_to_store[100:200]+"\r")
		hash_file2.close()
		global file_status
		file_status = "ok"
		log_file.write(str(datetime.datetime.now())+" File writing complete!\r")
		print("File writing complete!\r")

def keyword_query():
	if file_status == "ok":
		keyword_to_find = str(input("Enter a keyword: "))
		keyword_file = open("keys.txt", "r")
		if keyword_to_find in keyword_file.read().split():
			log_file.write(str(datetime.datetime.now())+" Found keyword. Acquiring line number...\r")
			keyword_file.close()
			line_finder(keyword_to_find)
		else:
			log_file.write(str(datetime.datetime.now())+" User attempted bad keyword query.\r")
			print("Keyword \""+keyword_to_find+"\" not found.\r")
			keyword_file.close()
	else:
		log_file.write(str(datetime.datetime.now())+" One or more files are missing; hash retrieval not possible.\r")
		print("Files <keys.txt> <hash1.txt> and <hash2.txt> must be present and non-empty to initiate retrieval.\nEnsure all files are in Tannin directory or store a new hash with command <s>.\n")

def line_finder(keyword_to_find):
	keyword_file = open("keys.txt", "r")
	for num, line in enumerate(keyword_file,1):
					if keyword_to_find in line:
						keyword_file.close()
						log_file.write(str(datetime.datetime.now())+" Found line number < "+str(num)+" >. Beginning retrieval...\r")
						retrieval(num)
						break

def retrieval(key):
	hash_file1 = open("hashes1.txt", "r")
	hash_file2 = open("hashes2.txt", "r")
	z = 0
	for z in range(int(key)):
		z += 1
		if z == key:
			global found_hash
			found_hash = hash_file1.readline().rstrip('\n')+hash_file2.readline().rstrip('\n')
			print("Hash found:\n\n--------------------------\n"+found_hash+"\n--------------------------")
			log_file.write(str(datetime.datetime.now())+" Hash successfully delivered.\r")
			hash_file1.close()
			hash_file2.close()
		else:
			log_file.write(str(datetime.datetime.now())+" Cycling through hash files...\r")
			hash_file1.readline()
			hash_file2.readline()
			continue
	if option1 == "c":
		copy_hash()

def copy_hash():
	if found_hash != 0:
		log_file.write(str(datetime.datetime.now())+" Copying found hash to clipboard...\r")
		pyperclip.copy(found_hash)
		print("Hash copied to clipboard.")
	else:
		log_file.write(str(datetime.datetime.now())+" User attempted copying hash when no hash found.\r")
		print("Find a hash first with command <r>")

def print_help():
	if os.path.exists("help.txt"):
		log_file.write(str(datetime.datetime.now())+" Opening and printing help file...\r")
		help_file = open("help.txt", "r")
		print(help_file.read())
		help_file.close()
		log_file.write(str(datetime.datetime.now())+" Help file printed.\r")
	else:
		log_file.write(str(datetime.datetime.now())+" User attempted help but no help file found.\r")
		print("No help file found.")

def list_keys():
	if os.path.exists("keys.txt"):
		log_file.write(str(datetime.datetime.now())+" Opening and printing keyword file...\r")
		keyword_file = open("keys.txt", "r")
		print("\nStored keywords:\n\n"+keyword_file.read())
		keyword_file.close()
		log_file.write(str(datetime.datetime.now())+" Keyword file printed.\r")
	else:
		log_file.write(str(datetime.datetime.now())+" User attempted listing keywords but no keyword file found.\r")
		print("No keyword file found.\n")

def wipe_files():
	if os.path.exists("keys.txt"):
		log_file.write(str(datetime.datetime.now())+" Deleting keyword file...\r")
		os.remove("keys.txt")
	else:
		log_file.write(str(datetime.datetime.now())+" Keyword file not found.\r")
		print("Keyword file does not exist.")
	if os.path.exists("hashes1.txt"):
		log_file.write(str(datetime.datetime.now())+" Deleting first hash file...\r")
		os.remove("hashes1.txt")
	else:
		log_file.write(str(datetime.datetime.now())+" First hash file not found.\r")
		print("First hash file does not exist.")
	if os.path.exists("hashes2.txt"):
		log_file.write(str(datetime.datetime.now())+" Deleting second hash file...\r")
		os.remove("hashes2.txt")
	else:
		log_file.write(str(datetime.datetime.now())+" Second hash file not found.\r")
		print("Second hash file does not exist.")
	print("File wiping complete.\n")
	log_file.write(str(datetime.datetime.now())+" File wiping complete.\r")

def task(selected_task):
	if selected_task == "store":
		log_file.write(str(datetime.datetime.now())+" Beginning storage protocol...\r")
		store()
	elif selected_task == "retrieve":
		log_file.write(str(datetime.datetime.now())+" Beginning retrieval protocol...\r")
		keyword_query()
	elif selected_task == "help":
		print_help()
	elif selected_task == "wipe":
		log_file.write(str(datetime.datetime.now())+" Beginning wipe protocol...\r")
		wipe_files()
	elif selected_task == "list":
		log_file.write(str(datetime.datetime.now())+" Beginning list protocol...\r")
		list_keys()
	elif selected_task == "copy":
		log_file.write(str(datetime.datetime.now())+" Beginning copy protocol...\r")
		copy_hash()
	elif selected_task == "quit":
		log_file.write(str(datetime.datetime.now())+" Quitting...\r")
		global T
		T = 1

greeting()
file_check()
found_hash = 0
T = 0
while T == 0:
	option1 = 0
	choice = get_command()
	task(choice)
	continue
log_file.write(str(datetime.datetime.now())+" Successfully reached end of program. Closing log.\r")
log_file.close()
