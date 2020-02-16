import timeit
import itertools
import os

start = timeit.default_timer()

passO = ['omac','dota','manga','25']
spChar = ['@', '#', '$']

passO_U = []
#passO = ['omac','dota','manga','cube','rndc','vistaar','25']
#spChar = ['!', '@', '#', '$', '%', '^', '&', '*']

for x in passO:
    passO_U.extend([x.title()])

[x.upper() for x in passO]

newPass = passO_U+ spChar

print("Started")


#for i in range(1,len(newPass)):
#    inputFile = [''.join(p) for p in itertools.permutations(newPass,i)]


def writeList(list):
    with open('omacPassList.py', 'w') as f:
        f.write("omacPass = [")
        for i in range(1,len(newPass)):
            for p in itertools.permutations(newPass,i):
                #print(''.join(p))
                f.write("'"+"".join(p)+"',")
        f.seek(-1,os.SEEK_END)
        f.write("]")


writeList(newPass)

stop = timeit.default_timer()
print ('Time: ', stop - start)
print ('--Done-- \n')  


""" with open('phoneList.txt', 'r') as f:
    x = f.read().split(',')

print(x) """
print ('--Done-- \n')  