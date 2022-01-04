from json2csv import json2csv
from crawl import cafef_crawl
from utils import create_if_not_exist
import os

if __name__=="__main__":
    output_folder = "data"
    create_if_not_exist(output_folder)
    cafef_crawl()
    json2csv()