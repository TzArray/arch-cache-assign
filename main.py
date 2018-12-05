import argparse
import math
import random
import re
import sys

class Node:
    def __init__(self):
        self.time = 0
        self.tag = 0
        self.valid = 1

class Cache:
    def __init__(self, cacheSize, blockSize, assoc, policy, indices, index, tag, offset):
        self.tagSize = int(tag)
        self.offsetSize = int(offset)
        self.indexSize = int(index)
        self.index = 0
        self.tag = 0
        self.offset = 0
        self.indices = int(indices)
        self.cacheSize = int(cacheSize)
        self.blockSize = int(blockSize)
        self.assoc = int(assoc)
        self.policy = policy
        self.total = 0
        self.cacheHit = 0
        self.compMiss = 0
        self.confMiss = 0
        self.cacheArr = [[Node() for j in range(int(assoc))] for i in range(int(indices))]


    def write(self, var, cache, length = 4):
        writeVar = self.getBinAdd(var)
        self.getDecimals(writeVar, cache)
        doAgain = int((cache.offset + length) / cache.blockSize) + 1
        while doAgain > 0:
            self.checkCache(cache)
            cache.index += 1
            if cache.index >= cache.indices:
                cache.index = 0
                cache.tag += 1
            doAgain -= 1


    def getBinAdd(self, var):
        convInt = int(var, 16)
        binRep = format(convInt, '0>32b')
        return binRep


    def getDecimals(self, var, cache):
        off = var[-cache.offsetSize:]
        cache.offset = self.binToDec(off)
        ind = var[cache.tagSize:cache.indexSize+cache.tagSize]
        cache.index = self.binToDec(ind)
        tag = var[0:cache.tagSize]
        cache.tag = self.binToDec(tag)


    def binToDec(self, var):
        val = 0
        pow = 0
        for i in range(len(var)-1, 0, -1):
            if var[i] == '1':
                val += 2**pow
            pow +=1
        return val


    def checkCache(self, cache):
        cache.total += 1
        for i in range(0, assoc):
            if cache.cacheArr[cache.index][i].valid == 1:
                cache.cacheArr[cache.index][i].valid = 0
                self.updateCacheNode(cache, i)
                cache.compMiss += 1
                return
            if cache.cacheArr[cache.index][i].tag == cache.tag:
                cache.cacheHit += 1
                return
        cache.confMiss += 1
        if cache.policy == 'RR':
            self.roundReplace(cache)
        elif cache.policy == 'RND':
            self.randomReplace(cache)
        elif cache.policy == 'LRU':
            self.recentReplace(cache)

    def updateCacheNode(self, cache, col):
        for i in range(0, col):
            if cache.cacheArr[cache.index][i].valid == 0:
                cache.cacheArr[cache.index][i].time += 1
        cache.cacheArr[cache.index][col].tag = cache.tag
        cache.cacheArr[cache.index][col].time += 0

    # chooses a column at random and replaces that one
    def randomReplace(self, cache):
        randInt = random.randint(0, cache.assoc)
        self.updateCacheNode(cache, randInt)

    # replaces one with time = assoc
    def roundReplace(self, cache):
        for i in range(0, assoc):
            if cache.cacheArr[cache.index][i].time == i - 1:
                col = i
        self.updateCacheNode(cache, i)

    # looks for highest time and replaces that one
    def recentReplace(self, cache):
        replace = 0
        for i in range(0, assoc):
            if cache.cacheArr[cache.index][i].time > cache.cacheArr[cache.index][replace].time:
                replace = i
        self.updateCacheNode(cache, replace)






"""
This parses the arguments from the command line.
"""
policies = ["RR", "RND", "LRU"]
parser = argparse.ArgumentParser()
parser.add_argument("-f", metavar="FILENAME", required=True)
parser.add_argument("-s", metavar="OURCACHE", type=int, required=True)
parser.add_argument("-b", metavar="BLOCK", type=int, required=True)
parser.add_argument("-a", metavar="ASSOC", type=int, required=True)
parser.add_argument("-r", metavar="POLICY", choices=policies, required=True)
args = parser.parse_args()

"""
Values set from the command line and used throughout this program.
"""
filename = args.f
cacheSize = args.s
blockSize = args.b
assoc = args.a
policy = args.r
blockNum = cacheSize / blockSize
offset = math.log(blockSize, 2)
indexSize = math.log((cacheSize / (blockSize * assoc)), 2)
indices = 2**indexSize
tagSize = 32-offset-indexSize
memSize = cacheSize+assoc*(1+tagSize)*indices/8

# open file here
# bail if misnamed file
try:
    file = open(filename, "r")
except:
    print("Error: unknown file name %s. Exiting!" % filename)
    sys.exit(1)

# initialize cache
newCache = Cache(cacheSize, blockSize, assoc, policy, indices, indexSize, tagSize, offset)
# newCache.initCacheArr(newCache)

for line in file:
    # skip new lines
    if line == '\n':
        continue
    data = line.split()
    data2 = file.readline().split()
    # if somehow the second line is blank break loop
    if not data2:
        break
    address = data[2]
    length = int(data[1][1:2])
    newCache.write(address, newCache, length)
    dest = data2[1]
    if dest != '00000000':
        newCache.write(dest, newCache)
    src = data2[4]
    if src != '00000000':
        newCache.write(src, newCache)
file.close()

print("\nCache Simulator CS 3853 Fall 2018 - Group #***")
print("\n=======Input=======")
print("Trace File: " + filename)
print("Cache Size: " + str(cacheSize) + " KB")
print("Block Size: " + str(blockSize) + " bytes")
print("Associativity: " + str(assoc)+"-way")
print("Replacement Policy: " + policy)

print("\n=======Calculated Values=======")
print("Total #Blocks: " + str(blockNum))
print("Offset: " + str(int(offset)))
print("Tag Size: " + str(int(tagSize)))
print("Index Size: " + str(int(indexSize)) + " bits, Total Indices: " + str(int(indices)))
print("Implementation Memory Size: " + str(int(memSize)) + " bytes")

print("\n=======Results=======")
print("Total Cache Accesses: %d " % newCache.total)
print("Cache Miss Rate: %f %%" % ((newCache.compMiss + newCache.confMiss)/newCache.total * 100))
print("Cache Hits: %d " % newCache.cacheHit)
print("Cache Misses: %d " % (newCache.compMiss + newCache.confMiss))
print("      >Compulsory Misses: %d " % newCache.compMiss)
print("      >Conflict Misses: %d " % newCache.confMiss)
print("=================")



