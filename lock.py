import logging
import threading
import time
import concurrent.futures

class FakeDatabase:
    def __init__(self):
        self.value = 0
        self._lock = threading.Lock()

    def update(self, name):
        logging.info("Thread %s: starting update", name)
        logging.info("Thread %s about to lock", name)
        with self._lock:
            logging.info("Thread %s has lock", name)
            local_copy = self.value
            local_copy += 1
            time.sleep(0.1)
            self.value = local_copy
            logging.info("Thread %s about to release lock", name)
        logging.info("Thread %s after release", name)
        logging.info("Thread %s: finishing update", name)

def thread_function(name):
    logging.info("Thread %s: starting", name)
    time.sleep(2)
    logging.info("Thread %s: finishing", name)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S") 

    database = FakeDatabase()
    logging.info("Testing update. Starting value is %d.", database.value)

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        for index in range(4):
            executor.submit(database.update, index)

    logging.info("Testing update. Ending value is %d.", database.value)
    

