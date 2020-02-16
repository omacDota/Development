import timeit
import time
from multiprocessing.dummy import Pool as ThreadPool
import sys
import itertools
import omacPassList

passwd = 'Dotamangaomac25@'
pool = ThreadPool(20)


#passO = ['omac','dota','manga','cube','rndc','vistaar','25']
#spChar = ['!', '@', '#', '$', '%', '^', '&', '*']
#newPass = passO + spChar

print("Getting Ip File")
inputFile = omacPassList.omacPass
inputFile = set(inputFile)
print("Got Input File \n")

#print(inputFile)
def BruteForce(idk):
    if(idk == passwd):
        print("[+] Found Match On : %s \n" %idk)


start = timeit.default_timer()
results = pool.map(BruteForce,inputFile)
stop = timeit.default_timer()

print('Time: ', stop - start)
print('--Done--')