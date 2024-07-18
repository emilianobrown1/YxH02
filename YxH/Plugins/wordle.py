import random
from easy_words import words
import string
import time
import requests
from bs4 import BeautifulSoup
import re
import asyncio

def _get_soup_object(url, parser="html.parser"):
    return BeautifulSoup(requests.get(url).text, parser)

asc = string.ascii_letters

def is_valid(text: str) -> bool:
  term: str = text
  try:
    html = _get_soup_object("http://wordnetweb.princeton.edu/perl/webwn?s={0}".format(
        term))
    types = html.findAll("h3")
    length = len(types)
    lists = html.findAll("ul")
    out = {}
    for a in types:
        reg = str(lists[types.index(a)])
        meanings = []
        for x in re.findall(r'\((.*?)\)', reg):
            if 'often followed by' in x:
                pass
            elif len(x) > 5 or ' ' in str(x):
                meanings.append(x)
        name = a.text
        out[name] = meanings
    return True
  except:
    return False

def get_reward(correct_guess: bool) -> int:
  if correct_guess:
        return 1  # Reward 1 crystal for correct guess
    else:
        return 0  # No reward  

# def blockify(word, query, neg):
#   word = word.lower()
#   query = query.lower()
#   txt = ''
#   a = 0
#   q = ''
#   for x in query:
#     if x == word[a]:
#       txt += '🟩'
#       q += x.upper() + ' '
#     else:
#       if x in word:
#         txt += '🟨'
#       else:
#         txt += '⬜'
#         if not x.upper() in neg:
#           neg.append(x.upper())
#       q += "_" + ' '
#     txt += ' '
#     a += 1
#   return txt, q, neg

def update_negated(word, text, lis):
  word = word.lower()
  text = text.lower()
  for i in text:
    if not i in word:
      if not i.upper() in lis:
        lis.append(i.upper())
  return lis

dic: dict = {} # normal wordle
time_out_dic: dict = {} # challenge wordle
