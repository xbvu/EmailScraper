import os
import sys
import queue
from tqdm import tqdm
from multiprocessing.dummy import Pool as ThreadPool

from emailscraper.config import config
from emailscraper.utils.printing import ot, tprint
from emailscraper.worker import worker, url_queue, proxy_queue, emails_dict

# try to load a third party config which would overwrite the default
try:
	config = __import__(sys.argv[1]).config
except IndexError:
	pass
except ModuleNotFoundError:
	sys.exit('[e] Config named "{}" was not found...... quitting.'.format(sys.argv[1]))

# main function
def main():

	# load proxy file specified in config
	proxy_file_absolute = os.path.abspath(config['PROXY_FILE'])
	proxy_queue.load(proxy_file_absolute)

	# load URL list
	with open(config['URL_FILE'], 'r') as r:
		for line in r.read().splitlines():
			url_queue.put((line, 0))

	tprint(ot.INFO + "%d urls loaded!" % url_queue.qsize())

	# create a thread pool
	pool = ThreadPool(config['THREAD_COUNT'])

	# catch KeyboardInterrupt exceptions (CTRL+C)
	try:
		# count URLs scraped and iterations (for terminal title)
		urls_scraped = 0
		current_iteration = 1

		# work while there are items in queue
		while url_queue.qsize() > 0:
			results = list(tqdm(pool.imap_unordered(worker, range(url_queue.qsize())), total=url_queue.qsize(), leave=False))

			os.system('clear')

			# change terminal title (works for Linux)
			sys.stdout.write("\x1b]2;{} {}\x07".format("EmailScraper v0.1  ||  ITERATION: ", current_iteration))
			tprint('-------------------------------------------------')
			tprint(ot.INFO + 'INFORMATION')
			tprint('  Threads working: %d' % config['THREAD_COUNT'])
			tprint('  Proxies active: %d' % proxy_queue.size())
			tprint('-------------------------------------------------')
			tprint(ot.INFO + 'RESULTS')
			tprint('  Total URLs scraped: %d' % urls_scraped)
			tprint('  Total emails gathered: %d' % len(emails_dict))
			tprint('-------------------------------------------------')
			tprint(ot.INFO + "press 'CTRL+C' to after threads finish.")
			tprint(ot.INFO + "press 'CTRL+C' twice to force quit.\n")
			urls_scraped += url_queue.qsize()
			current_iteration += 1

		# close threads if queue is empty 
		pool.close()
		pool.join()

	# catch CTRL+C and gracefully exit threads
	except KeyboardInterrupt:
		try:
			pool.terminate()
			pool.join()
			for email in emails_dict.keys():
				tprint("{} : {} sites".format(email, len(emails_dict[email])))

		# catch CTRL+C and force exit
		except KeyboardInterrupt:
			sys.exit('  Force interrupt by user.')

# if not imported as a nodule execute the main thread
if __name__ == '__main__':
	main()