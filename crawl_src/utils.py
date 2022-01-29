import os
import requests
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup

def create_if_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)

def save_each_iter(data_list, output_path):
    df_data = pd.DataFrame(data_list, columns=["title", "content", "date", "source"])
    df_data.to_csv(output_path, index=False)

def get_html(url:str):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    return soup