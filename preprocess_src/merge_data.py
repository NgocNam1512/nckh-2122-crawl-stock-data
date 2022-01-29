import pandas as pd
from filter import filter_content, filter_date
import os


def merge(input_path, output_path):
    df = pd.DataFrame(columns=["title","content","date","source"])
    for file in os.listdir(input_path):
        file_path = os.path.join(input_path, file)
        df_file = pd.read_csv(file_path)
        df = pd.concat([df, df_file])
    
    df = df.drop_duplicates()
    df = filter_date(df)
    df = filter_content(df)
    df.to_csv(output_path, index=False)


if __name__=='__main__':
    merge("/home/namnn12/personal/nckh-2122-crawl-stock-data/data/cafef", "/home/namnn12/personal/nckh-2122-crawl-stock-data/data/cafef.csv")
    merge("/home/namnn12/personal/nckh-2122-crawl-stock-data/data/skds", "/home/namnn12/personal/nckh-2122-crawl-stock-data/data/skds.csv")
    merge("/home/namnn12/personal/nckh-2122-crawl-stock-data/data/vneconomy", "/home/namnn12/personal/nckh-2122-crawl-stock-data/data/vneconomy.csv")
    merge("/home/namnn12/personal/nckh-2122-crawl-stock-data/data/vnexpress", "/home/namnn12/personal/nckh-2122-crawl-stock-data/data/vnexpress.csv")