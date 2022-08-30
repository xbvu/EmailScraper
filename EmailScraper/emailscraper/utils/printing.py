from tqdm import tqdm


# output tags
class ot:
	DEBUG = "[d] "
	INFO = "[i] "
	WARNING = "[w] "
	ERROR = "[e] "
	PROMPT = "[?] "


def tprint(message):
	tqdm.write(str(message))
