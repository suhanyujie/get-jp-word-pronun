import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path

# eg: %E5%AE%A2%E9%96%93
def get_url(word):
    res_url = ""
    if (word == ""):
        return res_url
    else:
        res_url = "https://www.dict.asia/jc/" + word
    return res_url

def get_html(url):
    page_cont = requests.get(url)
    return page_cont

# 包含单词假名
def get_jp_tone(word):
    url1 = get_url(word)
    cont = get_html(url1)
    tone_info_str = ""
    soup = BeautifulSoup(cont.text, 'html.parser')
    # 单词结果
    prononceResArr = soup.find_all(id="jp_Resunt_panel")
    if len(prononceResArr) <= 0:
        print("未找到结果1")
        return tone_info_str

    # 假名
    soup2 = BeautifulSoup(str(list(prononceResArr)[0]), 'html.parser')
    trs = soup2.find(attrs={"class": "trs_jp bold"}).getText()
    tone_info_str = trs

    # 音调
    soup2 = BeautifulSoup(str(list(prononceResArr)[0]), 'html.parser')
    tone_str = soup2.find(attrs={"class": "tone_jp"}).getText()
    if len(tone_str) <= 0:
        print("未找到音调 1")
        return tone_str
    tone_info_str += " | " + tone_str
    return tone_info_str

# 只返回单词的音调
# test
# tone = get_jp_tone_only("めうえ")
# print(tone)
def get_jp_tone_only(word):
    url1 = get_url(word)
    cont = get_html(url1)
    tone_info_str = ""
    soup = BeautifulSoup(cont.text, 'html.parser')
    # 单词结果
    prononceResArr = soup.find_all(id="jp_Resunt_panel")
    if len(prononceResArr) <= 0:
        print("未找到结果1")
        return tone_info_str

    # 音调
    tone_str = '';
    try:
        soup2 = BeautifulSoup(str(list(prononceResArr)[0]), 'html.parser')
        tone_str = soup2.find(attrs={"class": "tone_jp"}).getText()
    except:
        return '';
    if len(tone_str) <= 0:
        print("未找到音调 1 word:" + word)
        return tone_str
    return tone_str

# 查询某一课的所有单词音调，并写入到新文件
def gen_one_class_all_word(file_path):
    res_word_list = [];
    if file_path == '':
        return res_word_list;

    new_file_path = get_new_file_path(file_path)
    contents = Path(file_path).read_text(encoding='utf-8')
    line_arr = contents.splitlines();
    new_lines = [];
    # 写入新的文件 todo
    with open(new_file_path, "a", encoding='utf-8') as f:
        for line in line_arr:
            info_arr = line.split(',');
            if len(info_arr) == 0:
                continue
            tone = get_jp_tone_only(info_arr[0]);
            if tone == '':
                continue;
            new_line = line + ','+ tone
            # print(new_line)
            new_lines.append(new_line);
            f.write(new_line + "\n");
        f.close();
    return res_word_list

def get_new_file_path(file_path):
    basename = os.path.basename(file_path);
    file_name, ext = os.path.splitext(basename);
    new_path = "./data/" + file_name + '_with_tone' + ext;
    return new_path;

gen_one_class_all_word('./data/05.txt');
