import logging 
import threading 
import time


def thread_function(name): 
    logging.info("Thread %s: starting (%s)", name, threading.get_ident()) 
    time.sleep(2) 
    logging.info("Thread %s: finishing (%s)", name, threading.get_ident())

if __name__ == "__main__": 
    format = "%(asctime)s: %(message)s" 
    logging.basicConfig(format=format, 
                level=logging.INFO, 
                datefmt="%H:%M:%S") 

    logging.info("Main    : before creating first thread") 
    x = threading.Thread(target=thread_function, args=(1,), daemon=True) 
    logging.info("Main    : before running first thread") 
    x.start() 
    logging.info("Main    : wait for the first thread to finish") 
    x.join() 

    logging.info("Main    : before creating second thread") 
    x = threading.Thread(target=thread_function, args=(2,), daemon=True) 
    logging.info("Main    : before running second thread") 
    x.start() 
    logging.info("Main    : wait for the second thread to finish") 
    x.join() 

    logging.info("Main    : before creating third thread") 
    x = threading.Thread(target=thread_function, args=(3,), daemon=True) 
    logging.info("Main    : before running third thread") 
    x.start() 
    logging.info("Main    : wait for the third thread to finish") 
    x.join() 

    logging.info("Main    : all done")

