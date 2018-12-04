"""
Created on Nov 26, 2018

@author: Christopher
"""

import argparse
import math
import re

policies = ["RR", "RND", "LRU"]

parser = argparse.ArgumentParser(description="Computer Arch 2018")
parser.add_argument("FILEFLAG", metavar="FILEFLAG")
parser.add_argument("FILENAME", metavar="FILENAME")
parser.add_argument("CACHEFLAG", metavar="CACHEFLAG")
parser.add_argument("OURCACHE", metavar="OURCACHE", type=int)
parser.add_argument("BLOCKFLAG", metavar="BLOCKFLAG")
parser.add_argument("BLOCK", metavar="BLOCK", type=int)
parser.add_argument("ASSOCFLAG", metavar="ASSOCFLAG")
parser.add_argument("ASSOC", metavar="ASSOC", type=int)
parser.add_argument("POLICYFLAG", metavar="POLICYFLAG")
parser.add_argument("POLICY", metavar="POLICY", choices=policies)
args = parser.parse_args()

filename = args.FILENAME
assoc = args.ASSOC
policy = args.POLICY
ourCache = args.OURCACHE
block = args.BLOCK
blockNum = 2**block
offset = math.log(block, 2)
indexSize = ourCache/(block*8)
indices = 2**indexSize
tagSize = 32-offset-indexSize
memSize = ourCache+assoc*(1+tagSize)*indices/8
genSize = ""
if indices >= 1024:
    genSize = " KB"
elif indices >= 1048576:
    genSize = " MB"

# (2^10)/(2^16*2)=(1024)/(128kb) 131072
print("\nCache Simulator CS 3853 Fall 2018 - Group #***")
print("\n=======Input=======")
print("File Name: " + filename)
print("Cache Size: " + str(ourCache) + " KB")
print("Block Size: " + str(block) + " bytes")
print("Associativity: " + str(assoc)+"-way")
print("Replacement Policy: " + policy)

print("\n=======Calculated Values=======")
print("Total #Blocks: " + str(blockNum) + " KB (2^" + str(block) + ")")
print("Offset: " + str(int(offset)))
print("Tag Size: " + str(int(tagSize)))
print("Index Size: " + str(int(indexSize)) + " bits, Total Indices: " + str(int(indices)) + genSize)
print("Memory Size: " + str(int(memSize)))

print("\n=======Results=======")
print("Cache Hit Rate: ")

print("\n=================\n")

count = 0
file = open(filename, "r")

for line in file:
    if line == '\n':
        continue
    data = line.split()
    data2 = file.readline().split()
    if not data2:
        break
    address = data[2]
    length = data[1]
    length = re.sub('[():]', '', length)
    dest = data2[1]
    src = data2[4]
file.close()
