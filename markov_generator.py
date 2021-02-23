import markovify
import random
import re

with open("quotesntweets.txt", encoding="utf-8") as quotes:
    text = quotes.read()

text_model = markovify.NewlineText(text)

text_model.compile()

def generate():
    regex = "((?i){|sheriff:|bosby:|juberr:|toes:|wulf:|kayla:|whatsoup:|gianni:|krygowski:|shots:|mito:|scarf:|mikey:})"
    msg = text_model.make_sentence(tries=100).split()
    out = ""

    for i in msg:
        if re.match(regex, i):
            out += "\n" + i
        else: out += " " + i
            
    return out
