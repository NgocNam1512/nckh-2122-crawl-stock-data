from symtable import Symbol
import pandas as pd


PRICE_STOCK_LIST = [
    "data/price_data_2020.csv",
    "data/price_data_2021.csv"
]

def load_date():
    df = pd.read_csv("/home/namnn12/personal/nckh-2122-crawl-stock-data/date.txt", sep="\t")
    return df


def load_symbol_list():
    with open("/home/namnn12/personal/nckh-2122-crawl-stock-data/symbol_list.txt") as f:
        symbol_list = [line.replace("\n","") for line in f.readlines() ]

    return symbol_list

def main():
    date_df = load_date()
    symbol_list = load_symbol_list()

    stock_price = list()
    for stock_price_file in PRICE_STOCK_LIST:
        df = pd.read_csv(stock_price_file)
        stock_price.append(df)
    stock_price_df = pd.concat(stock_price, ignore_index=True)  
    filtered_cols =["code", "date", "open", "high", "low", "close", "average", "nmVolume"]
    stock_price_filter_df = stock_price_df[filtered_cols]

    for symbol in symbol_list:
        print(symbol)
        symbol_df = stock_price_filter_df[stock_price_filter_df["code"]==symbol]
        symbol_result_list = list()
        for row in date_df.itertuples():
            date = row.From
            date_str = str(row.From)
            date_str = "-".join([date_str[:4], date_str[4:6], date_str[6:]])
            count = 0
            while len(symbol_df[symbol_df["date"]==date_str]) == 0:
                count += 1
                date = date - 1
                date_str = str(date)
                date_str = "-".join([date_str[:4], date_str[4:6], date_str[6:]])
            symbol_df.loc[symbol_df["date"]==date_str, "date_event"] = str(row.From)
            symbol_result_list.append(symbol_df[symbol_df["date"]==date_str])
        
        symbol_result_df = pd.concat(symbol_result_list, ignore_index=True)
        symbol_result_df.to_csv(f"/home/namnn12/personal/nckh-2122-crawl-stock-data/data/price_data/{symbol}.csv", sep="\t", index=False)
        
        

if __name__=="__main__":
    main()