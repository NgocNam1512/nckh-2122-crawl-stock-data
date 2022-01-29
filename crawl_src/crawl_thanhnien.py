from bs4 import BeautifulSoup
from tqdm import tqdm
from utils import create_if_not_exist, get_html, save_each_iter
import pandas as pd
import requests

URL_LIST = [
    "https://thanhnien.vn/tai-chinh-kinh-doanh/?trang="
]

def get_links(url:str):
    soup = get_html(url)
    titles = soup.findAll("a", {"class":"story__title cms-link"})
    links = []
    for title in titles:
        links.append(title['href'])

    return links


def get_content(soup):
    description = soup.find('h2', {'class':'detail-sapo'}).text
    detail = soup.find('div', {'class':'detail-content afcbc-body'})
    main_content =  description + "\n"
    for p in detail.findAll('p'):
        main_content += p.text + "\n"

    return main_content


def get_date(soup):
    datetime = soup.find('time', {'datetime':'publish-date'}).text
    date = datetime.split(" ")[0].strip()
    day, month, year = date.split("-")
    datestring = year + f"{int(month):02d}" + f"{int(day):02d}"
    
    return datestring
    

def get_title(soup):
    title = soup.find('h1', {'class':'details__headline cms-title'}).text

    return title


def crawl():
    web_name = "thanhnien"
    create_if_not_exist(f"data/{web_name}")
    for i in tqdm(range(1, 270)):
        data_list = list()
        for url in URL_LIST:
            links = get_links(url + str(i) + ".htm")
            for link in links:
                try:
                    soup = get_html(link)
                    title = get_title(soup)
                    content = get_content(soup)
                    date = get_date(soup)
                    source = web_name
                    data_list.append([title, content, date, source])
                except:
                    print("error:", link)
        save_each_iter(data_list, f"data/{web_name}/{web_name}_{i}.csv")

if __name__=="__main__":
    crawl()