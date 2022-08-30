import re
import queue
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import urllib3

from emailscraper.config import config
from emailscraper.proxy import ProxyList
from emailscraper.utils.printing import ot, tprint

urllib3.disable_warnings()


def parse_emails(html_source):
    # parse emails using regex
    # https://gist.github.com/dideler/5219706
    regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+"
                        "\/=?^_`{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9]"
                        ")?(\.|\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))
    return (email[0] for email in re.findall(
        regex, html_source) if not email[0].startswith('//') and email[0][-3] not in ['png', 'jpg', 'gif', 'ico'])


def parse_links(html_source):
    # parse a hrefs from HTML code
    soup = BeautifulSoup(html_source, features="lxml")
    a_tags = soup.find_all('a')
    links = []
    for tag in a_tags:
        link = tag.get('href', '')
        if link:
            links.append(link)
    return links

# create the necessary data structures
proxy_queue = ProxyList()
url_queue = queue.Queue()
urls_dict = {}
emails_dict = {}


# the worker function
def worker(args):
    current_url, url_depth = url_queue.get()
    urls_dict[current_url] = True
    proxy = proxy_queue.get_proxy()

    # try to connect and handle possible connection errors
    try:
        r = requests.get(current_url, stream=True, verify=False, proxies=proxy, timeout=config['REQUEST_TIMEOUT'])
    except requests.exceptions.ConnectionError:
        return
    except requests.exceptions.ReadTimeout:
        return
    except requests.exceptions.TooManyRedirects:
        return

    # read requests stream for the number of bytes defined in config
    response_body = str(r.raw.read(config['MAX_RESPONSE_SIZE']+1, decode_content=True))

    for email in parse_emails(response_body):
        if emails_dict.get(email):
            emails_dict[email].append(current_url)
        else:
            emails_dict[email] = [current_url]
            requests.post('http://127.0.0.1:5000/add/', data={'email':email, 'domain':current_url})

    current_url_parse = urlparse(current_url)
    for url in parse_links(response_body):

        new_url_parse = urlparse(url)

        # Skip if url has already been checked.
        if urls_dict.get(url):
            continue

        # TODO: extend this list and move it to configuration
        # skips extensions that will not contain any urls or emails 
        elif url[-4:] in ['.png', '.jpg', '.css', '.pdf', '.gif', '.mp4', '.webm', '.avi']:
            continue

        # check for conditions defined in the config and form an absolute URL from a relative one
        elif url.startswith('/') and ((config['BLACKLIST_ENABLED'] and current_url_parse.netloc not in config['BLACKLIST']) or
          (config['WHITELIST_ENABLED'] and current_url_parse.netloc in config['WHITELIST'])):

            if config['MAX_DEPTH'] and url_depth + 1 > config['MAX_DEPTH']:
                continue
            else:
                new_url = urljoin(current_url_parse.scheme + '://' + current_url_parse.netloc, url)
                url_queue.put((new_url, url_depth + 1))

        # check for conditions defined in the config and use an absolute URL
        elif url.startswith('http') and ((config['BLACKLIST_ENABLED'] and new_url_parse.netloc not in config['BLACKLIST']) or
          (config['WHITELIST_ENABLED'] and new_url_parse.netloc in config['WHITELIST'])):

            if new_url_parse.netloc == current_url_parse.netloc:
                if config['MAX_DEPTH'] and url_depth + 1 > config['MAX_DEPTH']:
                    continue
                else:
                    url_queue.put((url, url_depth + 1))
            else:
                urls_dict[url] = True
                url_queue.put((url, 0))

        else:
            pass

    return

