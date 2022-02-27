import random
import logging
import threading 
import concurrent.futures

class Pipeline:
    """
    Class to allow a single element pipeline b/w producer and consumer
    """
    def __init__(self):
        self.message = 0
        self.producer_lock = threading.Lock()
        self.consumer_lock = threading.Lock()
        self.consumer_lock.acquire()

    def get_message(self, name):
        logging.debug("%s: about to acquire getlock", name)
        self.consumer_lock.acquire()
        logging.debug("%s: have getlock", name)
        message = self.message
        logging.debug("%s: about to release getlock", name)
        self.producer_lock.release()
        logging.debug("%s: setlock released", name)
        return message

    def set_message(self, message, name):
        logging.debug("%s: about to acquire setlock", name)
        self.producer_lock.acquire()
        logging.debug("%s: have setlock", name)
        self.message = message
        logging.debug("%s: about to release getlock", name)
        self.consumer_lock.release() 
        logging.debug("%s: getlock released", name)

SENTINEL = object()

def producer(pipeline):
    """Pretend we're getting a message from the network"""
    for index in range(5):
        message = random.randint(1, 101)
        logging.info("Producer got message: %s (%d)", message, index)
        pipeline.set_message(message, "Producer")

def consumer(pipeline):
    """Pretend we're saving a number in the database"""
    message = 0
    while message is not SENTINEL:
        message = pipeline.get_message("Consumer")
        if message is not SENTINEL:
            logging.info("Consumer storing messages: %s", message)

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.DEBUG,
                        datefmt="%H:%M:%S") 

    pipeline = Pipeline() 
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        executor.submit(producer, pipeline)
        executor.submit(consumer, pipeline)

