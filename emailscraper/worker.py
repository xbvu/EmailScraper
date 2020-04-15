import re
import threading
from bs4 import BeautifulSoup


def parse_emails(html_source):
    # https://gist.github.com/dideler/5219706
    regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+"
                        "\/=?^_`{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9]"
                        ")?(\.|\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))
    return (email[0] for email in re.findall(
        regex, html_source) if not email[0].startswith('//'))


def parse_links(html_source):
    soup = BeautifulSoup(html_source)
    a_tags = soup.find_all('a')
    links = []
    for tag in a_tags:
        link = tag.get('href', None)
        # checking for http in links to filter out mailto: and non..
        # ..HTTP links, for example torrent magnet links
        if 'http' in link:
            links.append(link)
    return links


class Worker(threading.Thread):

    def __init__(self, thread_id, name, q):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.q = q
        return
