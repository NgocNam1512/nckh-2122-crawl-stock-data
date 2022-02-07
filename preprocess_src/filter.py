import pandas as pd


def filter_date(df):
    date_path="/home/namnn12/personal/nckh-2122-crawl-stock-data/date.txt"
    df_filter = df.copy()
    df_filter["event_id"] = 0
    date_df = pd.read_csv(date_path, sep="\t")
    for date in date_df.itertuples():
        df_filter.loc[(df_filter["date"] >= date.From) & (df_filter["date"] <= date.To), "event_id"]=date.STT

    return df_filter[df_filter['event_id']!=0]


def filter_content(df):
    covid_word_path="/home/namnn12/personal/nckh-2122-crawl-stock-data/covid_word.txt"
    with open(covid_word_path) as f:
        list_word = [line.replace("\n","") for line in f.readlines()]

    is_covid_news = list()
    df_filter = df.copy()
    for row in df_filter.itertuples():
        count_word = 0
        for word in list_word:
            if word in row.content.lower():
                count_word += 1
        if count_word >= 2:
            is_covid_news.append(True)
        else:
            is_covid_news.append(False)

    return df_filter[is_covid_news]