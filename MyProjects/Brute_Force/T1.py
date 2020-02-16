from __future__ import print_function
import timeit
import time
from multiprocessing.dummy import Pool as ThreadPool
import sys


passwd = '25#dotamanga'
fileName = 'omacPassListMulti.txt'
pool = ThreadPool(20) 


print("Getting Ip File")

with open(fileName, 'r') as f:
    phoneList = f.read().split(',')
print("Got Input File \n")


def BruteForce(idk):
    if(idk == str(passwd)):
        print("[+] Found Match On : %s \n" %idk)


start = timeit.default_timer()
results = pool.map(BruteForce,phoneList)
stop = timeit.default_timer()

""" for i in range(100):
    time.sleep(0.1)
    print(''+str(i)+'', end='\r') """

""" if(flag is False):
    print("No reasult found") """
print('Time: ', stop - start)
print('--Done--')  