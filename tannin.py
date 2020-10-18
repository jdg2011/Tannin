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
#The storage process should also verify that the given keyword has not already been used.

tannin_version = "0.2.3 \"I Just Wanted to Make You Something Beautiful\""

import pyperclip
import os
import datetime

def greeting():
	print("Welcome to Tannin")
	print("version "+tannin_version+"\n")

def file_check():
	global file_status
	log_file.write(str(datetime.datetime.now())+" Checking files...\r")
	water_check = bool(os.path.exists("water.txt"))
	earl_check = bool(os.path.exists("earl.txt"))
	grey_check = bool(os.path.exists("grey.txt"))
	if water_check and earl_check and grey_check:
		log_file.write(str(datetime.datetime.now())+" All files found.\r")
		file_status = "ok"
	elif not water_check and not earl_check and not grey_check:
		log_file.write(str(datetime.datetime.now())+" No files found. New directories will be created.\r")
		file_status = "bad"
	else:
		log_file.write(str(datetime.datetime.now())+" Some but not all files found. Unstable status.\r")
		print("WARNING: A partial directory was found. Quit and ensure all files are restored before proceeding, or enter command <w> to wipe all present files.\n\n")
		file_status = "bad"

def index_keywords():
	log_file.write(str(datetime.datetime.now())+" Indexing stored keywords...\r")
	global keyword_index
	keyword_index = []
	f = open("water.txt", "r")
	for x in f:
		keyword_index.append(x.rstrip('\n'))
	log_file.write(str(datetime.datetime.now())+" Indexing complete.\r")
	f.close()

def get_command():
	x = 0
	while x == 0:
		global option1
		command = input("\nEnter command: ")
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
			log_file.write(str(datetime.datetime.now())+" User attempted invalid command. Trying again...\r")
			continue

def store():
	keyword_to_store = str(input("Enter a keyword: "))
	if keyword_to_store in keyword_index:
		log_file.write(str(datetime.datetime.now())+" User attempted storing with keyword already in use.\r")
		print("Keyword is already being used in this database. Choose another.")
	else:
		if option1 == "p":
			log_file.write(str(datetime.datetime.now())+" Attempting to pull hash from clipboard...\r")
			print("Getting hash from clipboard...")
			hash_to_store = pyperclip.paste()
		else:
			hash_to_store = input("Enter a hash to be stored: ")
			log_file.write(str(datetime.datetime.now())+" Successful hash input.\r")
		if len(hash_to_store) != 200:
			print("Entered length is "+str(len(hash_to_store))+". hash must equal 200 characters.\r")
		else:
			log_file.write(str(datetime.datetime.now())+" Successful keyword and hash input. Storing keyword...\r")
			f_water = open("water.txt", "a")
			f_water.write(keyword_to_store+"\r")
			f_water.close()
			log_file.write(str(datetime.datetime.now())+" Storing hash...\r")
			f_earl = open("earl.txt", "a")
			f_earl.write(hash_to_store[0:100]+"\r")
			f_earl.close()
			f_grey = open("grey.txt", "a")
			f_grey.write(hash_to_store[100:200]+"\r")
			f_grey.close()
			log_file.write(str(datetime.datetime.now())+" File writing complete!\r")
			print("File writing complete!")
			index_keywords()

def keyword_query():
	if file_status == "ok":
		keyword_to_find = str(input("Enter a keyword: "))
		f_water = open("water.txt", "r")
		if keyword_to_find in f_water.read().split():
			log_file.write(str(datetime.datetime.now())+" Found keyword. Acquiring line number...\r")
			f_water.close()
			line_finder(keyword_to_find)
		else:
			log_file.write(str(datetime.datetime.now())+" User attempted bad keyword query.\r")
			print("Keyword \""+keyword_to_find+"\" not found.")
			f_water.close()
	else:
		log_file.write(str(datetime.datetime.now())+" One or more files are missing; hash retrieval not possible.\r")
		print("Files <water.txt> <earl.txt> and <grey.txt> must be present and non-empty to initiate retrieval.\nEnsure all files are in Tannin directory or store a new hash with command <s>.\n")

def line_finder(keyword_to_find):
	f_water = open("water.txt", "r")
	for num, line in enumerate(f_water,1):
					if keyword_to_find in line:
						f_water.close()
						log_file.write(str(datetime.datetime.now())+" Found line number < "+str(num)+" >. Beginning retrieval...\r")
						retrieval(num)
						break

def retrieval(key):
	f_earl = open("earl.txt", "r")
	f_grey = open("grey.txt", "r")
	z = 0
	for z in range(int(key)):
		z += 1
		if z == key:
			global found_hash
			found_hash = f_earl.readline().rstrip('\n')+f_grey.readline().rstrip('\n')
			print("Hash found:\n\n--------------------------\n"+found_hash+"\n--------------------------")
			log_file.write(str(datetime.datetime.now())+" Hash successfully delivered.\r")
			f_earl.close()
			f_grey.close()
		else:
			log_file.write(str(datetime.datetime.now())+" Cycling through hash files...\r")
			f_earl.readline()
			f_grey.readline()
			continue
	if option1 == "c": copy_hash()

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
	if os.path.exists("water.txt"):
		log_file.write(str(datetime.datetime.now())+" Opening and printing keyword file...\r")
		f_water = open("water.txt", "r")
		print("\nStored keywords:\n\n"+f_water.read())
		f_water.close()
		log_file.write(str(datetime.datetime.now())+" Keyword file printed.\r")
	else:
		log_file.write(str(datetime.datetime.now())+" User attempted listing keywords but no keyword file found.\r")
		print("No keyword file found.\n")

def wipe_files():
	if os.path.exists("water.txt"):
		log_file.write(str(datetime.datetime.now())+" Deleting keyword file...\r")
		os.remove("water.txt")
	else:
		log_file.write(str(datetime.datetime.now())+" Keyword file not found.\r")
		print("Keyword file does not exist.")
	if os.path.exists("earl.txt"):
		log_file.write(str(datetime.datetime.now())+" Deleting first hash file...\r")
		os.remove("earl.txt")
	else:
		log_file.write(str(datetime.datetime.now())+" First hash file not found.\r")
		print("First hash file does not exist.")
	if os.path.exists("grey.txt"):
		log_file.write(str(datetime.datetime.now())+" Deleting second hash file...\r")
		os.remove("grey.txt")
	else:
		log_file.write(str(datetime.datetime.now())+" Second hash file not found.\r")
		print("Second hash file does not exist.")
	print("File wiping complete.")
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
log_file = open("log.txt", "w")
log_file.write("Log file created "+str(datetime.datetime.now())+" running version "+tannin_version+"\r")
file_check()
if file_status == "ok": index_keywords()
found_hash = 0
T = 0
while T == 0:
	option1 = 0
	choice = get_command()
	task(choice)
	continue
log_file.write(str(datetime.datetime.now())+" Successfully reached end of program. Closing log.\r")
log_file.close()
