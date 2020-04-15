# temporary solution  for relative imports..
# ..until I turn this into a proper package
from emailscraper.proxy import ProxyList
import emailscraper.utils.output_tags as ot

PROXY_FILE = "proxies.txt"

proxy_list = ProxyList()
proxy_list.load(PROXY_FILE)

print(ot.INFO + "Getting one proxy.")
print(proxy_list.get_proxy())
