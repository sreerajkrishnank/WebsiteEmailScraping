from Queue import Queue
from threading import Thread
import seolib as seo


def do_stuff(q):
  while True:
    line = q.get()
    url = line.strip('\n')
    alexa_rank = seo.get_alexa('http://'+str(url))
    if str(alexa_rank) != 'None':
    	rank = str(alexa_rank)+'\n'
    	row = url + ','+rank
    	print row
    else:
    	print 'vannillaaaa'
    q.task_done()

q = Queue(maxsize=0)
num_threads = 100

for i in range(num_threads):
  worker = Thread(target=do_stuff, args=(q,))
  worker.setDaemon(True)
  worker.start()

hostfile = open("new_3.txt","r")
for line in hostfile:
    #Put line to queue
    q.put(line)
q.join()