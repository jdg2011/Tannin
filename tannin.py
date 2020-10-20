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

tannin_version = "3.1.0 \"The Shade\""

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
		log_file.write(str(datetime.datetime.now())+" No files found.\r")
		file_status = "none"
	else:
		log_file.write(str(datetime.datetime.now())+" Some but not all files found. Unstable status.\r")
		print("WARNING: A partial directory was found. Quit and ensure all files are restored before proceeding, or enter command <w> to wipe all present files.\n\n")
		file_status = "bad"
	index_keywords()

def index_keywords():
	global keyword_index
	keyword_index = []
	if file_status == "ok":
		log_file.write(str(datetime.datetime.now())+" Indexing stored keywords...\r")
		f = open("water.txt", "r")
		for x in f:
			keyword_index.append(x.rstrip('\n'))
		f.close()
		log_file.write(str(datetime.datetime.now())+" Indexing complete.\r")
	else:
		log_file.write(str(datetime.datetime.now())+" No keywords to index.\r")

def store():
	if file_status == "ok" or file_status == "none":
		if option2 == 0:
			keyword_to_store = input("Enter a keyword: ")
		else:
			keyword_to_store = option2
		if " " in keyword_to_store:
			log_file.write(str(datetime.datetime.now())+" User attempted storing with keyword with a space.\r")
			print("You cannot store keywords with spaces. Try _ or -.")
		elif keyword_to_store in keyword_index:
			log_file.write(str(datetime.datetime.now())+" User attempted storing with keyword already in use.\r")
			print("Keyword \""+keyword_to_store+"\" is already in use. Choose another.")
		else:
			if option1 == "p":
				log_file.write(str(datetime.datetime.now())+" Getting hash from clipboard...\r")
				print("Getting hash from clipboard...")
				hash_to_store = pyperclip.paste()
			else:
				hash_to_store = input("Enter a hash to be stored: ")
				log_file.write(str(datetime.datetime.now())+" Successful hash input.\r")
			if len(hash_to_store) != 200:
				print("Entered length is "+str(len(hash_to_store))+". Hash length must equal 200 characters.\r")
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
				log_file.write(str(datetime.datetime.now())+" Hash storage complete.\r")
				print("Hash storage complete.")
				file_check()
	elif file_status == "bad":
		log_file.write(str(datetime.datetime.now())+" One or two files are missing; hash storage not possible.\r")
		print("Files <water.txt> <earl.txt> and <grey.txt> must be present and non-empty to initiate storage.\nEnsure all files are in Tannin directory or wipe database with <w>.\n")

def keyword_search():
	if file_status == "ok":
		if option2 == 0:
			keyword_to_find = str(input("Enter a keyword: "))
		else:
			keyword_to_find = option2
		f_water = open("water.txt", "r")
		if keyword_to_find in f_water.read().split():
			log_file.write(str(datetime.datetime.now())+" Found keyword. Acquiring line number...\r")
			f_water.close()
			line_finder(keyword_to_find)
		else:
			log_file.write(str(datetime.datetime.now())+" User attempted bad keyword query.\r")
			print("Keyword \""+keyword_to_find+"\" not found.")
			f_water.close()
	elif file_status == "bad":
		log_file.write(str(datetime.datetime.now())+" One or two files are missing; hash retrieval not possible.\r")
		print("Files <water.txt> <earl.txt> and <grey.txt> must be present and non-empty to initiate query.\nEnsure all files are in Tannin directory or wipe database with <w>.\n")
	else:
		log_file.write(str(datetime.datetime.now())+" User attempted query with no hashes stored.\r")
		print("No hashes stored yet.\nStart storing hashes with command <s>.")

def line_finder(keyword_to_find):
	f_water = open("water.txt", "r")
	for num, line in enumerate(f_water,1):
					if keyword_to_find in line:
						f_water.close()
						log_file.write(str(datetime.datetime.now())+" Found line number < "+str(num)+" >.\r")
						if option1 == "d": delete_hash(num-1)
						else: hash_delivery(num)
						break

def hash_delivery(key):
	log_file.write(str(datetime.datetime.now())+" Beginning hash delivery protocol...\r")
	f_earl = open("earl.txt", "r")
	f_grey = open("grey.txt", "r")
	z = 0
	for z in range(int(key)):
		z += 1
		if z == key:
			global found_hash
			found_hash = f_earl.readline().rstrip('\n')+f_grey.readline().rstrip('\n')
			f_earl.close()
			f_grey.close()
			print("Hash found:\n--------------------------\n"+found_hash+"\n--------------------------")
			log_file.write(str(datetime.datetime.now())+" Hash successfully delivered.\r")
		else:
			log_file.write(str(datetime.datetime.now())+" Cycling through hash files...\r")
			f_earl.readline()
			f_grey.readline()
			continue
	if option1 == "c": copy_hash()

def delete_hash(num):
	log_file.write(str(datetime.datetime.now())+" Beginning delete has protocol...\r")
	f_earl = open("earl.txt", "r")
	earl_lines = f_earl.readlines()
	f_earl.close()
	f_earl = open("earl.txt", "w")
	z = 0
	for x in earl_lines:
		if z != num:
			f_earl.write(x)
		z += 1
	f_earl.close()
	f_grey = open("grey.txt", "r")
	grey_lines = f_grey.readlines()
	f_grey.close()
	f_grey = open("grey.txt", "w")
	z = 0
	for x in grey_lines:
		if z != num:
			f_grey.write(x)
		z += 1
	f_grey.close()
	f_water = open("water.txt", "r")
	water_lines = f_water.readlines()
	f_water.close()
	f_water = open("water.txt", "w")
	z = 0
	for x in water_lines:
		if z != num:
			f_water.write(x)
		z += 1
	f_water.close()
	index_keywords()
	print("Entry deleted.")
	log_file.write(str(datetime.datetime.now())+" Hash and keyword successfully deleted.\r")

def copy_hash():
	if found_hash != 0:
		log_file.write(str(datetime.datetime.now())+" Copying found hash to clipboard...\r")
		pyperclip.copy(found_hash)
		print("Hash copied to clipboard.")
	else:
		log_file.write(str(datetime.datetime.now())+" User attempted copying hash when no hash found.\r")
		print("Find a hash first with command <q>")

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
		print("No keyword file found.")

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
	file_check()
	print("File wiping complete.")
	log_file.write(str(datetime.datetime.now())+" File wiping complete.\r")

def get_command():
	x = 0
	while x == 0:
		global option1
		global option2
		command = str(input("\nEnter command: "))
		if command == "s" or command == "store":
			return "store"
		elif command == "s -p" or command == "store -p":
			option1 = "p"
			return "store"
		elif len(command)>5 and command[0:5]=="s -p ":
			option_end = len(command)
			option1 = "p"
			option2 = command[5:option_end]
			return "store"
		elif len(command)>9 and command[0:9]=="store -p ":
			option_end = len(command)
			option1 = "p"
			option2 = command[9:option_end]
			return "store"
		elif len(command)>2 and command[0:2]=="s ":
			option_end = len(command)
			option2 = command[2:option_end]
			return "store"
		elif len(command)>6 and command[0:6]=="store ":
			option_end = len(command)
			option2 = command[6:option_end]
			return "store"
		elif command == "q" or command == "query":
			return "query"
		elif command == "q -c" or command == "query -c":
			option1 = "c"
			return "query"
		elif len(command)>5 and command[0:5]=="q -c ":
			option_end = len(command)
			option1 = "c"
			option2 = command[5:option_end]
			return "query"
		elif len(command)>9 and command[0:9]=="query -c ":
			option_end = len(command)
			option1 = "c"
			option2 = command[9:option_end]
			return "query"
		elif command == "q -d" or command == "query -d":
			option1 = "d"
			return "query"
		elif len(command)>5 and command[0:5]=="q -d ":
			option_end = len(command)
			option1 = "d"
			option2 = command[5:option_end]
			return "query"
		elif len(command)>9 and command[0:9]=="query -d ":
			option_end = len(command)
			option1 = "d"
			option2 = command[9:option_end]
			return "query"
		elif len(command)>2 and command[0:2]=="q ":
			option_end = len(command)
			option2 = command[2:option_end]
			return "query"
		elif len(command)>6 and command[0:6]=="query ":
			option_end = len(command)
			option2 = command[6:option_end]
			return "query"
		elif command == "h" or command == "help":
			return "help"
		elif command == "e" or command == "exit":
			return "exit"
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

def task(selected_task):
	if selected_task == "store":
		log_file.write(str(datetime.datetime.now())+" Beginning storage protocol...\r")
		store()
	elif selected_task == "query":
		log_file.write(str(datetime.datetime.now())+" Beginning query protocol...\r")
		keyword_search()
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
	elif selected_task == "exit":
		log_file.write(str(datetime.datetime.now())+" Exiting...\r")
		global T
		T = 1

greeting()
log_file = open("log.txt", "w")
log_file.write("Log file created "+str(datetime.datetime.now())+" running version "+tannin_version+"\r")
file_check()
found_hash = 0
T = 0
while T == 0:
	option1 = 0
	option2 = 0
	choice = get_command()
	task(choice)
	continue
log_file.write(str(datetime.datetime.now())+" Successfully reached end of program. Closing log.\r")
log_file.close()
