#!/usr/bin/env python3

import argparse
import os
import re
import sys

matches = 0
fasta_start= 0
fasta_end = 0
seq_of_int= ''
seq_loc= ''
full_fasta= ''

#once a row is matched, get seq from substring of seq(1) where start(4):end(5)

#list of attributes in file (always in format attribute = value)
#ID; Name; gene; Alias; Ontology_term; dbxref; Note; orf_classification;

#collecting the arguments
parser = argparse.ArgumentParser()
parser.add_argument("--source", "--source", type=str, required=True)
parser.add_argument("--type", "--type", type = str, required = True)
parser.add_argument("--attribute", "--attribute", type = str, required = True)
parser.add_argument("--value", "--value", type = str, required = True)
args = parser.parse_args()

def print_fasta_format(fasta):    
    print(fasta)
    fasta_len = len(fasta)
    #trying to print with fasta format...
    '''for n in range(0, fasta_len):
   	 sys.stdout.write(((fasta[n]).rstrip))
   	 #count = count +1
   	 if (n%60)==0:
   		 sys.stdout.write("\n")'''

def print_seq(full):
    f_line = full.find('\n')
    full = full[f_line:]
    seq_of_int = full[(int(fasta_start)):(int(fasta_end))]
    print_fasta_format((seq_of_int).rstrip())
    #print(seq_of_int)

def find_fasta():
    full_fasta = ''
    add_seq = False
    print(">{0}:{1}:{2}".format(args.type, args.attribute, args.value))
    #print(seq_loc)
    for line in open(args.source):
   	 if line.startswith(">"+seq_loc+"\n"):
   		 add_seq = True
   		 
   	 if add_seq:
   		 full_fasta = full_fasta + line
    #print(full_fasta)    
    fasta_list = full_fasta.split('>')
    #print(len(fasta_list))
    full_fasta = fasta_list[1]
    
    print_seq(full_fasta)    

#going through file, line by line
for line in open(args.source):
    #if args.type in line:
    line = line.rstrip()
    cols = line.split("\t")
    if (len(cols)) ==9: #only interested in lines with attributes
   	 #print(cols)
   	 if args.type == cols[2]: #matching the type entered
   		 #print(cols)
   		 attributes = cols[8].split(";") #making a list of all attributes within one entry
   		 for attribute in attributes:
   			 #print(attribute)
   			 full_search = (args.attribute)+"="+(args.value) #formatting to find match
   			 #print(full_search)
   			 if full_search == attribute:
   				 matches = matches+1   				 
   				 #print(attribute)
   				 #print(line)
   				 #print("{0} match(es) found.".format(matches))
   				 fasta_start = int(cols[3]) - 1
   				 fasta_end = int(cols[4]) + 1
   				 seq_loc = cols[0]
   				 #print("Beg at: {0}, end at: {1}".format(fasta_start, fasta_end))


if matches ==1:
    print("{0} successful match found.".format(matches))
    find_fasta()
if matches == 0:
    print("No matches found.  Program ending.")
elif matches>1:
    print("{0} matches found.".format(matches))
    print("Cannot continue, program ending")

