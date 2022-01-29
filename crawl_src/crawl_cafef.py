from bs4 import BeautifulSoup
import requests
from utils import create_if_not_exist
from tqdm import tqdm
import pandas as pd
import os

URL_LIST = [
    "https://cafef.vn/timeline/112/trang-", # thoi su
    "https://cafef.vn/timeline/31/trang-", # chung khoan
    "https://cafef.vn/timeline/35/trang-", #bds
    "https://cafef.vn/timeline/36/trang-", #doanh nghiep
    "https://cafef.vn/timeline/34/trang-", #ngan hang
    "https://cafef.vn/timeline/32/trang-", #tai chinh quoc te
    "https://cafef.vn/timeline/33/trang-", #vi mo
    "https://cafef.vn/timeline/114/trang-", #song
    "https://cafef.vn/timeline/39/trang-", #thi truong
]


def pdate2date(pdate:str) -> str:
    datetime = pdate.split(" ")[0]
    date, month, year = datetime.split("-")
    return year + month + date


def cafef_crawl(output_folder="data/cafef"):
    URLcafef = "https://cafef.vn"

    create_if_not_exist(output_folder)
    for i in tqdm(range(117, 1100)):
        data_list = list()
        for URL in tqdm(URL_LIST):
            page = requests.get(URL + str(i) +'.chn')

            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.findAll("a", {"class":"avatar show-popup visit-popup"})

            for result in results:
                link = result.get('href')
                URLpage = URLcafef + link
                article_html = requests.get(URLpage)
                article = BeautifulSoup(article_html.content, 'html.parser')
                try:
                    title = article.findAll("h1", {"class":"title"})[0]
                    title = title.text.replace("\r\n","").strip()

                    pdate = article.findAll("span", {"class":"pdate"})[0]
                    date = pdate2date(pdate.text)

                    summary = article.findAll("h2", {"class":"sapo"})[0].text.strip()
                    results2 = article.find(id="mainContent")
                    all_p = results2.findAll('p')
                    main_content = summary
                    for p in all_p:
                        main_content += p.text
                    
                    source="cafef"

                    data_list.append([title, main_content, date, source])
                except:
                    print("Error at:", link)

        df_data = pd.DataFrame(data_list, columns=["title", "content", "date", "source"])
        df_data.to_csv(os.path.join(output_folder, f"cafef_{i}.csv"), index=False)

cafef_crawl()