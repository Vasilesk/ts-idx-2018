import re

SPLIT_RGX = re.compile(r'\w+', re.U)


def extract_words(text):
    words = SPLIT_RGX.findall(text)
    return set([s.lower() for s in words])
    # return map(lambda s: s.lower(), words)
