# Currently not all settings are used.

config = {
	# GENERAL FILES
	# urls file
	'URL_FILE': 'urls.txt',
	# proxies_file
	'PROXY_FILE': 'proxies.txt',
	# proxy type 1 = SSL, 2 = SOCKS5
	'PROXY_TYPE': 2,


	# WHITELIST AND BLACKLIST
	# blacklist enabled
	'BLACKLIST_ENABLED': False,
	# blacklist items
	'BLACKLIST': [''],
	# blacklist file
	'BLACKLIST_FILE': None,
	# whitelist enabled
	'WHITELIST_ENABLED': True,
	# whitelist items
	'WHITELIST': ['example.com', 'www.example.com'],
	# whitelist file
	'WHITELIST_FILE': None,


	# SETTINGS
	# thread count
	'THREAD_COUNT': 25,
	# max response size
	'MAX_RESPONSE_SIZE': 100000,
	# request timeout in seconds
	'REQUEST_TIMEOUT': 10,
	# crawler depth
	'MAX_DEPTH': False,
}
