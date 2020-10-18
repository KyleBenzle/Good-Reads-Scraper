
import pandas as pd

df = pd.read_csv('amzonurl.csv', header=None)
split_function = lambda x: x.split('/ref')[0].split('?keyword')[0] + '/?tag=audiobookre03-20'

df[0] = df[0].apply(split_function)

df.to_csv("new_amazon_with_split_and_tag.csv", index=False)





