from bs4 import BeautifulSoup
import requests
from utils import pdate2date, save_json, create_if_not_exist
from tqdm import tqdm

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

def cafef_crawl(prefix_id="00", output_folder="data/cafef"):
    URLcafef = "https://cafef.vn"

    create_if_not_exist(output_folder)
    
    suffix_id = 0
    pre_date = None
    for i in tqdm(range(1, 2)):
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
                        main_content += p.text +"\n"
                    
                    id = "".join([prefix_id, date, f"{suffix_id:03}"])
                    source="cafef"

                    save_json(id, title, main_content, date, source, output_folder)
                    if date == pre_date:
                        suffix_id += 1
                    else:
                        pre_date = date
                        suffix_id = 0
                except:
                    print("Error at:", link)
