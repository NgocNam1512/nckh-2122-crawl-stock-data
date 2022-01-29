from bs4 import BeautifulSoup
from tqdm import tqdm
from utils import create_if_not_exist
import pandas as pd
import requests

URL_LIST = [
    "https://vneconomy.vn/tieu-diem.htm?trang=",
    "https://vneconomy.vn/dau-tu.htm?trang=",
    "https://vneconomy.vn/tai-chinh.htm?trang=",
    "https://vneconomy.vn/thi-truong.htm?trang=",
    "https://vneconomy.vn/chung-khoan.htm?trang=",
    "https://vneconomy.vn/nhip-cau-doanh-nghiep.htm?trang=",
    "https://vneconomy.vn/dia-oc.htm?trang=",
    "https://vneconomy.vn/kinh-te-the-gioi.htm?trang=",
    "https://vneconomy.vn/dan-sinh.htm?trang="
]

def get_links(url:str):
    soup = get_html(url)
    titles = soup.findAll("h3", {"class":"story__title"})
    links = []
    for title in titles:
        links.append("https://vneconomy.vn/" + title.a['href'])

    return links


def get_html(url:str):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    return soup


def get_content(soup):
    description = soup.find('h2', {'class':'detail__summary'}).text
    detail = soup.find('div', {'class':'detail__content'})

    main_content = description + "\n"
    for p in detail.findAll('p'):
        main_content += p.text + "\n"

    return main_content


def get_date(soup):
    datetime = soup.find('div', {'class':'detail__meta'}).text
    date = datetime.split(" ")[1].strip()
    day, month, year = date.split("/")
    datestring = year + f"{int(month):02d}" + f"{int(day):02d}"
    
    return datestring
    

def get_title(soup):
    title = soup.find('h1', {'class':'detail__title'}).text

    return title


def save_each_iter(data_list, output_path):
    df_data = pd.DataFrame(data_list, columns=["title", "content", "date", "source"])
    df_data.to_csv(output_path, index=False)


def crawl_vneconomy():
    create_if_not_exist("data/vneconomy")
    for i in tqdm(range(1, 501)):
        data_list = list()
        for url in URL_LIST:
            links = get_links(url + str(i))
            for link in links:
                try:
                    soup = get_html(link)
                    title = get_title(soup)
                    content = get_content(soup)
                    date = get_date(soup)
                    source = "vneconomy"
                    data_list.append([title, content, date, source])
                except:
                    print("error:", link)
        save_each_iter(data_list, f"data/vneconomy/vneconomy_{i}.csv")

if __name__=="__main__":
    crawl_vneconomy()