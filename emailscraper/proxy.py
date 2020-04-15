#!/usr/bin/python3
from queue import PriorityQueue
import emailscraper.utils.output_tags as ot
from emailscraper.utils.tuple_sorting import TupleSortingOn0


class ProxyList:
    def __init__(self):
        self.proxy_input_file = ""
        self.proxy_queue = PriorityQueue()

        print(ot.INFO + "Proxy list initialized.")

    def load(self, proxy_input_file):
        self.proxy_input_file = proxy_input_file
        try:
            with open(self.proxy_input_file) as proxy_file:
                self.lines = proxy_file.read().splitlines()
                for line in self.lines:
                    try:
                        ip = line.split(":")[0]
                        port = line.split(":")[1]
                        self.proxy_queue.put(TupleSortingOn0(
                            (0, {"ip": ip, "port": int(port)})))
                    except IndexError:
                        continue
                line_count = self.proxy_queue.qsize()
                print(ot.INFO + "%d" % line_count + " proxies loaded.")

        except (FileNotFoundError, NameError):
            print(ot.ERROR + "'%s'" % proxy_input_file + " file not found!")

    def get_proxy(self):
        current_proxy = self.proxy_queue.get()
        count, proxy = current_proxy
        self.proxy_queue.put(TupleSortingOn0((count + 1, proxy)))
        return proxy
