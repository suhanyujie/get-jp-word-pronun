import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import json
import time


# eg: %E5%AE%A2%E9%96%93
def get_url(word):
    res_url = ""
    if word == "":
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
    soup = BeautifulSoup(cont.text, "html.parser")
    # 单词结果
    prononceResArr = soup.find_all(id="jp_Resunt_panel")
    if len(prononceResArr) <= 0:
        print("未找到结果1")
        return tone_info_str

    # 假名
    soup2 = BeautifulSoup(str(list(prononceResArr)[0]), "html.parser")
    trs = soup2.find(attrs={"class": "trs_jp bold"}).getText()
    tone_info_str = trs

    # 音调
    soup2 = BeautifulSoup(str(list(prononceResArr)[0]), "html.parser")
    tone_str = soup2.find(attrs={"class": "tone_jp"}).getText()
    if len(tone_str) <= 0:
        print("未找到音调 1")
        return tone_str
    tone_info_str += " | " + tone_str
    return tone_info_str


# 通过 moji 词典查询音调
# eg: print(get_jp_tone_by_moji('~方'))
def get_jp_tone_by_moji(word):
    url1 = "https://api.mojidict.com/parse/functions/union-api"
    headers = {
        "content-type": "text/plain",
        "origin": "https://www.mojidict.com",
        "referer": "https://www.mojidict.com/",
        "user-agent": "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
    }
    postData = {
        "_SessionToken": "r:603e6e9430f3c668ad0ffc93730a8dff",
        "_ClientVersion": "js3.4.1",
        "_ApplicationId": "E62VyFVLMiW7kvbtVq3p",
        "g_os": "PCWeb",
        "g_ver": "v4.7.7.20240327",
        "_InstallationId": "ce0e63fe-d00a-4079-9576-545cd648eca6",
        "functions": [
            {"name": "search-all", "params": {"text": "", "types": [102, 106, 103]}}
        ],
    }
    postData["functions"][0]["params"]["text"] = word
    tone_info_str = ""
    # 单词结果
    resp = requests.post(url=url1, headers=headers, data=json.dumps(postData))
    resp = resp.json()
    if resp["result"]["code"] != 200:
        return tone_info_str
    search_res_list = resp["result"]["results"]["search-all"]["result"]["word"][
        "searchResult"
    ]
    if len(search_res_list) == 0:
        return tone_info_str
    else:
        # 暂时这样处理
        search_res_list = search_res_list[0:1]
    search_res = search_res_list[0]
    word_title = search_res["title"]
    word_mean = search_res["excerpt"]
    # 方 | かた ②
    word_info_arr = word_title.split("|")
    if len(word_info_arr) <= 1:
        return tone_info_str
    else:
        tone_info_str = word_info_arr[1]
    return tone_info_str


# 通过 moji 词典查询单词信息
def get_jp_word_by_moji(word):
    url1 = "https://api.mojidict.com/parse/functions/union-api"
    headers = {
        "content-type": "text/plain",
        "origin": "https://www.mojidict.com",
        "referer": "https://www.mojidict.com/",
        "user-agent": "user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
    }
    postData = {
        "_SessionToken": "r:603e6e9430f3c668ad0ffc93730a8dff",
        "_ClientVersion": "js3.4.1",
        "_ApplicationId": "E62VyFVLMiW7kvbtVq3p",
        "g_os": "PCWeb",
        "g_ver": "v4.7.7.20240327",
        "_InstallationId": "ce0e63fe-d00a-4079-9576-545cd648eca6",
        "functions": [
            {"name": "search-all", "params": {"text": "", "types": [102, 106, 103]}}
        ],
    }
    postData["functions"][0]["params"]["text"] = word
    tone_info_str = {
        "word_tone": "",
        "word_mean": "",
    }
    # 单词结果
    resp = requests.post(url=url1, headers=headers, data=json.dumps(postData))
    resp = resp.json()
    if resp["result"]["code"] != 200:
        return tone_info_str
    search_res_list = resp["result"]["results"]["search-all"]["result"]["word"][
        "searchResult"
    ]
    if len(search_res_list) == 0:
        return tone_info_str
    else:
        # 暂时这样处理
        search_res_list = search_res_list[0:1]
    res_info = {}
    search_res = search_res_list[0]
    word_title = search_res["title"]
    word_mean = search_res["excerpt"]
    res_info["word_mean"] = word_mean
    # 方 | かた ②
    word_info_arr = word_title.split("|")
    if len(word_info_arr) <= 1:
        return tone_info_str
    else:
        tone_info_str = word_info_arr[1]
        res_info["word_tone"] = tone_info_str
    return res_info


# 只返回单词的音调
# test
# tone = get_jp_tone_only("めうえ")
# print(tone)
def get_jp_tone_only(word):
    url1 = get_url(word)
    cont = get_html(url1)
    tone_info_str = ""
    soup = BeautifulSoup(cont.text, "html.parser")
    # 单词结果
    prononceResArr = soup.find_all(id="jp_Resunt_panel")
    if len(prononceResArr) <= 0:
        print("未找到结果1")
        return tone_info_str

    # 音调
    tone_str = ""
    try:
        soup2 = BeautifulSoup(str(list(prononceResArr)[0]), "html.parser")
        tone_str = soup2.find(attrs={"class": "tone_jp"}).getText()
    except:
        return ""
    if len(tone_str) <= 0:
        print("未找到音调 1 word:" + word)
        return tone_str
    return tone_str


# 查询某一课的所有单词音调，并写入到新文件
def gen_one_class_all_word_tone(file_path, q_type="moji"):
    res_word_list = []
    if file_path == "":
        return res_word_list

    new_file_path = get_new_file_path(file_path)
    contents = Path(file_path).read_text(encoding="utf-8")
    line_arr = contents.splitlines()
    new_lines = []
    # 写入新的文件 todo
    with open(new_file_path, "a", encoding="utf-8") as f:
        for line in line_arr:
            info_arr = line.split(",")
            if len(info_arr) == 0:
                continue
            tmp_word = remove_extra_part(info_arr[0])
            if q_type == "moji":
                tone = get_jp_tone_by_moji(tmp_word)
            else:
                tone = get_jp_tone_only(tmp_word)
            new_line = line + "," + tone
            # print(new_line)
            new_lines.append(new_line)
            f.write(new_line + "\n")
        f.close()
    return res_word_list


# 查询单词信息：音调，中文意思等
def gen_one_class_all_word_info(file_path, q_type="moji"):
    res_word_list = []
    if file_path == "":
        return res_word_list
    new_file_path = get_new_file_path(file_path)
    contents = Path(file_path).read_text(encoding="utf-8")
    line_arr = contents.splitlines()
    new_lines = []
    # 写入新的文件 todo
    with open(new_file_path, "a", encoding="utf-8") as f:
        for line in line_arr:
            line = line.strip()
            if line == "":
                continue
            word_info_list = {
                "word": line,
            }
            info_arr = line.split(",")
            if len(info_arr) == 0:
                continue
            tmp_word = remove_extra_part(info_arr[0])
            if q_type == "moji":
                word_info_list = get_jp_word_by_moji(tmp_word)
            else:
                print("暂不支持")
                os._exit(1)
            if word_info_list["word_mean"] == "":
                print("未查询到。", line)
            new_line = (
                line
                + ", "
                + word_info_list["word_tone"]
                + ", "
                + word_info_list["word_mean"]
            )
            # print(new_line);
            new_lines.append(new_line)
            f.write(new_line + "\n")
            time.sleep(0.5)
        f.close()
    return res_word_list


def get_new_file_path(file_path):
    basename = os.path.basename(file_path)
    file_name, ext = os.path.splitext(basename)
    new_path = "./data/" + file_name + "_with_tone" + ext
    return new_path


# 去除单词中，影响查询的多余部分
# eg: remove_extra_part('~方[右の~]');
def remove_extra_part(word):
    pos = word.find("[")
    if pos == -1:
        return word
    word = word[0:pos]
    return word


# gen_one_class_all_word_tone('./data/06.txt');
# 查询《学ぼう、日本語》教材的单词
gen_one_class_all_word_info("./data/manabou3-1.txt", q_type="moji")
