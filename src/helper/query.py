import os
import re
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import json
import time


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
    word_info_dict = {
        "word_tone": "",
        "word_mean": "",
    }
    # 单词结果
    resp = requests.post(url=url1, headers=headers, data=json.dumps(postData))
    resp = resp.json()
    if resp["result"]["code"] != 200:
        return word_info_dict
    # fix: 查询特殊的英文时，会出现没有 word 字段数据
    if "word" not in resp["result"]["results"]["search-all"]["result"]:
        return word_info_dict
    search_res_list = resp["result"]["results"]["search-all"]["result"]["word"][
        "searchResult"
    ]
    if len(search_res_list) == 0:
        return word_info_dict
    else:
        # 暂时这样处理
        search_res_list = search_res_list[0:1]
    res_info = word_info_dict
    search_res = search_res_list[0]
    word_title = search_res["title"]
    if "excerpt" in search_res:
        word_mean = search_res["excerpt"]
    else:
        word_mean = ""
    res_info["word_mean"] = word_mean
    # 方 | かた ②
    word_info_arr = word_title.split("|")
    if len(word_info_arr) <= 1:
        return word_info_dict
    else:
        word_info_dict = word_info_arr[1]
        res_info["word_tone"] = word_info_dict
    return res_info


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
    tmp_result = resp["result"]["results"]["search-all"]["result"]
    if "word" not in tmp_result:
        print("word not found 1. word:" + word)
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
    # word_mean = search_res["excerpt"]
    # 方 | かた ②
    word_info_arr = word_title.split("|")
    if len(word_info_arr) <= 1:
        return tone_info_str
    else:
        tone_info_str = word_info_arr[1]
    return tone_info_str
