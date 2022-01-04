from datetime import datetime
import re
import requests
import pandas as pd

def convert_date(text, date_type = '%Y-%m-%d'):
    return datetime.strptime(text, date_type)
    

def convert_text_dateformat(text, origin_type = '%Y-%m-%d', new_type = '%Y-%m-%d'):
    return convert_date(text, origin_type).strftime(new_type)


def crawl_price(symbol, start, end):
    # symbol = "VND"
    # start = "01/09/2019"
    # end = "01/11/2019"

    start_date = convert_text_dateformat(start, origin_type = '%d/%m/%Y', new_type = '%Y-%m-%d')
    end_date = convert_text_dateformat(end, origin_type = '%d/%m/%Y', new_type = '%Y-%m-%d')
    API_VNDIRECT = 'https://finfo-api.vndirect.com.vn/v4/stock_prices/'
    HEADERS = {'content-type': 'application/x-www-form-urlencoded', 'User-Agent': 'Mozilla'}
    query = 'code:' + symbol + '~date:gte:' + start_date + '~date:lte:' + end_date
    delta = datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')
    params = {
        "sort": "date",
        "size": delta.days + 1,
        "page": 1,
        "q": query
    }
    res = requests.get(API_VNDIRECT, params=params, headers=HEADERS)
    data = res.json()['data']  
    data = pd.DataFrame(data)

    return data


def get_list_symbol(path):
    symbol_list = list()
    with open(path) as reader:
        symbol_list = [line.replace("\n","") for line in reader.readlines()]
    
    return symbol_list


def main():
    symbol_list = get_list_symbol("symbol_list.txt")
    start_date = "01/01/2021"
    end_date = "31/12/2021"

    data_list = []
    for symbol in (symbol_list):
        data_list.append(crawl_price(symbol, start_date, end_date))
    
    full_data = pd.concat(data_list, ignore_index=True)
    full_data.to_csv("data/price_data.csv")


if __name__=="__main__":
    main()
