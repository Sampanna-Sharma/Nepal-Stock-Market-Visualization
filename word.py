import pandas as pd
import re
df = pd.read_csv("news_data.csv")
def seperate(term):
    '''input term as words seperated by commas'''
    x_word = df.news[df.news.str.contains('|'.join(term.split(',')) , flags=re.IGNORECASE, regex=True)]
    return x_word
nabil = 'nabil , nabil bank , nabil-bank'
nic = 'nic, nic asia, nic bank, nic-bank'
lumbini = 'lumbini , lumbini-bank, lumbini bank'
print(seperate(lumbini)) # try nabil and nic
