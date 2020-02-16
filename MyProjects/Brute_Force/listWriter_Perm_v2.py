import timeit
import itertools
import os
from multiprocessing.dummy import Pool as ThreadPool
start = timeit.default_timer()


os.remove("omacPassListMulti.txt")
pool = ThreadPool(50)
#passO = ['omac','dota','manga','25']
spChar = ['@', '#', '$']

passO_U = []
passO = ['omac','dota','manga','cube','rndc','vistaar','25']
#spChar = ['!', '@', '#', '$', '%', '^', '&', '*']

for x in passO:
    passO_U.extend([x.title()])

[x.upper() for x in passO]

newPass = passO + spChar

print("Started")

rangeOfI = []
for i in range(1,len(newPass)):
    rangeOfI.extend([i])
#print(rangeOfI)


def writeList(i):
    global newPass
    with open('omacPassListMulti.txt', 'a') as f:
        for p in itertools.permutations(newPass,i):
            #print(''.join(p))
            f.write(''.join(p)+",")
        f.write('\n')
        f.close()
    

results = pool.map(writeList,rangeOfI)



stop = timeit.default_timer()
print ('Time: ', stop - start)
print ('--Done-- \n')  