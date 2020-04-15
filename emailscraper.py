import threading
from queue import Queue
from emailscraper.worker import Worker
# from concurrent.futures import ThreadPoolExecutor


class EmailScraper:

    def __init__(self, start_urls=[], max_workers=10):

        self.start_urls = start_urls
        self.threads = []
        self.thread_names = []
        self.max_workers = max_workers
        # self.pool = ThreadPoolExecutor(max_workers=max_workers)
        self.scraped_urls = {}
        self.to_crawl = Queue.Queue()
        self.queue_lock = threading.Lock()

        for url in self.start_urls:
            self.to_crawl.put(self.base_url)

    def setup(self):

        # Create thread names
        for i in range(1, self.max_workers):
            self.thread_names.append("Worker({})".format(i))

        # Create new threads
        thread_id = 1
        for thread_name in self.thread_names:
            thread = Worker(thread_id, thread_name, self.to_crawl)
            thread.start()
            self.threads.append(thread)
            thread_id += 1

        # Fill the queue
        self.queue_lock.acquire()
        for word in self.start_urls:
            self.queue_lock.put(word)
        self.queue_lock.release()

    def run(self):
        return