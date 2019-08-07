import pandas as pd 

nabil_news = pd.read_csv('nabil.csv')

nabil_news_list = list(nabil_news['news'])

print(nabil_news_list[:3])