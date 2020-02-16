import timeit
import time
from multiprocessing.dummy import Pool as ThreadPool
import sys
#import phoneList


passwd = 9619461856
fileName = 'phoneList.txt'
pool = ThreadPool(20) 


print("Getting Ip File")
inputFile = phoneList.phoneList
print("Got Input File \n")


def BruteForce(idk):
    if(idk == passwd):
        print("[+] Found Match On : %s \n" %idk)


start = timeit.default_timer()
results = pool.map(BruteForce,inputFile)
stop = timeit.default_timer()

print('Time: ', stop - start)
print('--Done--')  