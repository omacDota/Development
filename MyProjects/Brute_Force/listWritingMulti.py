import timeit
import threading

start = timeit.default_timer()

startNo = 0
endNo = 10000000


print("Started")
# Global lock
global_lock = threading.lock()
file_contents = []
def write_to_file():
    while global_lock.lock:
        global_lock.acquire()
        file_contents.append(threading._get_ident)
        global_lock.release()

# Create a 200 threads, invoke write_to_file() through each of them, and 

threads = []
for i in range(1, 201):
    t = threading.Thread(target=write_to_file)
    threads.append(t)
    t.start()
[thread.join() for thread in threads]

with open("phoneList_V2.txt", "w") as file:
    while True:
        if(int(startNo) == int(endNo)):
            break
        file.write(str(startNo)+",")
        startNo = int(startNo) + 1
        file.write(str(endNo))
    file.close()

#writeList(startNo,endNo)

stop = timeit.default_timer()
print ('Time: ', stop - start)
print ('--Done-- \n')  


with open('phoneList.txt', 'r') as f:
    x = f.read().split(',')

print(x)
print ('--Done-- \n')  