#!/usr/bin/python3
from queue import PriorityQueue
import sys

from emailscraper.config import config
from emailscraper.utils.printing import ot, tprint
from emailscraper.utils.tuple_sorting import TupleSortingOn0


class ProxyList:

    def __init__(self):
        self.proxy_input_file = ""
        self.proxy_queue = PriorityQueue()

        tprint(ot.INFO + "Proxy list initialized.")

    # method for loading a text file with proxies and setting up the object
    def load(self, proxy_input_file):
        self.proxy_input_file = proxy_input_file
        try:
            # read the file
            with open(self.proxy_input_file) as proxy_file:
                self.lines = proxy_file.read().splitlines()
                # iterate through lines
                for line in self.lines:
                    try:
                        # a proxy URI that can be used with requests library is crafted here
                        if config['PROXY_TYPE'] == 1:
                            proxy = {'http':'https://{}'.format(line), 'https':'https://{}'.format(line)}
                        elif config['PROXY_TYPE'] == 2:
                            proxy = {'http':'socks5h://{}'.format(line), 'https':'socks5h://{}'.format(line)}

                        # newly made object is put into the PriorityQueue
                        self.proxy_queue.put(TupleSortingOn0((0, proxy)))
                    except IndexError:
                        continue
                line_count = self.proxy_queue.qsize()
                tprint(ot.INFO + "%d" % line_count + " proxies loaded.")

        # if the file is not found print a message and exit
        except (FileNotFoundError):
            tprint(ot.ERROR + "'%s'" % proxy_input_file + " file not found!")
            sys.exit()

    # method to get the proxy, lower its priority and place it back to the queue
    def get_proxy(self):
        current_proxy = self.proxy_queue.get()
        count, proxy = current_proxy
        self.proxy_queue.put(TupleSortingOn0((count + 1, proxy)))
        return proxy

    # method to get the size of the queue
    def size(self):
        return self.proxy_queue.qsize()
