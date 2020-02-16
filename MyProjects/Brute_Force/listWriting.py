import timeit

start = timeit.default_timer()

startNo = 9000000000
endNo = 9999999999


startNo1 = 60
endNo1 = 90

print("Started")

def writeList(startNo,endNo):
    with open('phoneList.py', 'w') as f:
        f.write("phoneList = [")
        while True:
            if(int(startNo) == int(endNo)):
                break
            f.write(str(startNo)+",")
            startNo = int(startNo) + 1
        f.write(str(endNo))
        f.write("]")


writeList(startNo,endNo)

stop = timeit.default_timer()
print ('Time: ', stop - start)
print ('--Done-- \n')  


""" with open('phoneList.txt', 'r') as f:
    x = f.read().split(',')

print(x) """
print ('--Done-- \n')  