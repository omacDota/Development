import time
import threading

start_time = time.time()

startNo = 0
endNo = 1000
fileName = "phoneList_V2.txt"


print("Started")
#Global Lock
global_Lock = threading.Lock()

#Writing Function
def writingFunction(fileName,startNo,endNo):
    global global_Lock
    with open(fileName, "a") as file:
        while True:
            #global_Lock.acquire()
            if(int(startNo) == int(endNo)):
                break
            file.write(str(startNo)+",")
            startNo = int(startNo) + 1
            file.write(str(endNo))
            #global_Lock.release()
        file.close()


# Create a 50 threads, invoke write_to_file() through each of them
threads = []
for i in range(0,20000):
    t = threading.Thread(target=writingFunction, args=(fileName,startNo,endNo,))
    threads.append(t)
    t.start()
for t in threads:
    t.join()


print("--- %s seconds ---" % (time.time() - start_time))
print ('--Done-- \n')  


#with open('phoneList.txt', 'r') as f:
#     x = f.read().split(',')