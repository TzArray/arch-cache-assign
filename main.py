'''
Created on Nov 26, 2018

@author: Christopher
'''

import argparse
import random
import math
from math import log
import converters
from cache import Cache
from memory import Memory
from __builtin__ import int
from macpath import split


policies = ["RR", "RND", "LRU"]

parser = argparse.ArgumentParser(description="Computer Arch 2018")
parser.add_argument("FILENAME", metavar="FILENAME")     
parser.add_argument("OURCACHE", metavar="OURCACHE", type=int)
parser.add_argument("BLOCK", metavar="BLOCK", type=int)
parser.add_argument("ASSOC", metavar="ASSOC", type=int)
parser.add_argument("POLICY", metavar="POLICY", choices=policies)
args = parser.parse_args()

filename = args.FILENAME
assoc = args.ASSOC
policy = args.POLICY

ourCache = args.OURCACHE
block = args.BLOCK
blockNum = 2**block
offset = math.log(block,2)
setNum = ourCache/(block*args.ASSOC)*1000 #total indicies
setNumIndexBits = math.log(setNum,2)
indexSize = math.log(setNum,2)
tagSize = 32-offset-setNumIndexBits
memSize = ourCache+assoc*(1+tagSize)*indexSize/assoc

#(2^10)/(2^16*2)=(1024)/(128kb) 131072
print("\nCache Simulator CS 3853 Fall 2018 - Group #***")
print("\n=======Input=======")
print("File Name: " + filename)
print("Cache Size: " + str(ourCache) + " KB")
print("Block Size: " + str(block) + " bytes")
print("Associativity: " + str(assoc)+"-way")
print("Replacement Policy: " + policy)

print("\n=======Calculated Values=======")
print("Total #Blocks: "+str(blockNum)+" KB (2^"+str(block)+")")
print("Offset: "+str(offset))
print("#Sets: "+str(setNum))
print("#Sets/index bits: "+str(setNumIndexBits))
print("Tag Size: "+str(tagSize))
print("Index Size: "+str(indexSize)+" bits, Total Indicies: "+str(setNum)+" KB")
print("Memory Size: "+str(memSize))

print("\n=======Results=======")
print("Cache Hit Rate: ")

print("\n=================\n")

count = 0

f = open(filename,"r")

for aline in f:
    data = aline.split()
    #print(count,data)
    count+=1
    if count == 1:
        address = data[2]
        length = data[1]
        print("Address: "+data[2]+", Length: "+data[1])
    if count == 2:
        address = data[2]
        length = data[1]
        print("Data Write: "+data[1]+" "+data[2]+", Data Read: "+data[4]+" "+data[5])
    if count == 3:
        print ("***Newline***")
    if count == 4:
        address = data[2]
        length = data[1]
        print("Address: "+data[2]+", Length: "+data[1])
    if count == 5:
        address = data[2]
        length = data[1]
        print("Data Write: "+data[1]+" "+data[2]+", Data Read: "+data[4]+" "+data[5])
f.close()



