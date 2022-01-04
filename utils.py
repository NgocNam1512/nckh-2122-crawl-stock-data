import os
import json

def pdate2date(pdate:str) -> str:
    datetime = pdate.split(" ")[0]
    date, month, year = datetime.split("-")
    return year + month + date

def save_json(id, title, main_content, date, source, output_folder):
    data = {
        "id": id,
        "title": title,
        "content": main_content,
        "date": date,
        "source": source
    }
    save_path = os.path.join(output_folder, id+".json")
    with open(save_path, "w", encoding="utf-8") as writer:
        json.dump(data, writer, ensure_ascii=False)

def create_if_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)