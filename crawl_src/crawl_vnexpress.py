from bs4 import BeautifulSoup
from tqdm import tqdm
from utils import create_if_not_exist
import pandas as pd
import requests

URL_LIST = [
    "https://vnexpress.net/kinh-doanh/chung-khoan-p",
    "https://vnexpress.net/suc-khoe/tin-tuc-p",
    "https://vnexpress.net/suc-khoe/vaccine/covid-19-p",
    "https://vnexpress.net/kinh-doanh/quoc-te-p",
    "https://vnexpress.net/kinh-doanh/doanh-nghiep-p"
]

def get_links(url:str):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    titles = soup.findAll("h2", {"class":"title-news"})
    links = []
    for title in titles:
        links.append(title.a['href'])

    return links


def get_html(url:str):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup


def get_content(soup):
    title_detail = soup.find('h1', {'class':'title-detail'}).text
    description = soup.find('p', {'class':'description'}).text
    detail = soup.find('article', {'class':'fck_detail'})

    main_content = title_detail + "\n" + description + "\n"
    for p in detail.findAll('p'):
        main_content += p.text + "\n"

    return main_content


def get_date(soup):
    datetime = soup.find('span', {'class':'date'}).text
    date = datetime.split(",")[1].strip()
    day, month, year = date.split("/")
    datestring = year + f"{int(month):02d}" + f"{int(day):02d}"
    
    return datestring
    

def get_title(soup):
    title = soup.find('h1', {'class':'title-detail'}).text

    return title


def save_each_iter(data_list, output_path):
    df_data = pd.DataFrame(data_list, columns=["title", "content", "date", "source"])
    df_data.to_csv(output_path, index=False)


def crawl_vnexpress():
    create_if_not_exist("data/vnexpress")
    for i in tqdm(range(1, 410)):
        data_list = list()
        for url in URL_LIST:
            links = get_links(url + str(i))
            for link in links:
                try:
                    soup = get_html(link)
                    title = get_title(soup)
                    content = get_content(soup)
                    date = get_date(soup)
                    source = "vnexpress"
                    data_list.append([title, content, date, source])
                except:
                    print("error:", link)
        save_each_iter(data_list, f"data/vnexpress/vnexpress_{i}.csv")

if __name__=="__main__":
    crawl_vnexpress()