import requests
import toml
import os
import json
import genanki
from typing import Optional, List, Dict


def get_word_list_of_moji_collection() -> List[Dict]:
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "cache-control": "no-cache",
        "content-type": "text/plain",
        "origin": "https://www.mojidict.com",
        "pragma": "no-cache",
        "priority": "u=1, i",
        "referer": "https://www.mojidict.com/",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
    }
    config = toml.load("./.env.toml")
    data_str = config["moji"]["dataStr"]
    data = data_str
    response = requests.post(
        "https://api.mojidict.com/parse/functions/folder-fetchContentWithRelatives",
        headers=headers,
        data=data,
    )
    resp_json = response.json()
    word_list = resp_json["result"]["result"]
    new_list = []
    for word in word_list:
        new_word = {}
        new_word["title"] = word["title"]
        if "excerpt" in word["target"]:
            new_word["zh"] = word["target"]["excerpt"]
        elif "trans" in word["target"]:
            new_word["zh"] = word["target"]["trans"]
        else:
            print("异常1001", word)
        if "pron" in word["target"]:
            new_word["pron"] = word["target"]["pron"]
        new_list.append(new_word)
    return new_list


def gen_apkg_by_word_list(model_ins, deck_ins, word_list: List):
    for one_word in word_list:
        if len(one_word) == 0:
            continue
        if "|" in one_word["title"]:
            cont1 = one_word["title"]
        elif "pron" in one_word:
            cont1 = "{} | {}".format(one_word["title"], one_word["pron"])
        else:
            cont1 = one_word["title"]
        # 防止翻译中有一些非法字符
        one_word["zh"] = one_word["zh"].replace("<", "[")
        one_word["zh"] = one_word["zh"].replace(">", "]")
        tmp_note = genanki.Note(model=model_ins, fields=[cont1, one_word["zh"]])
        deck_ins.add_note(tmp_note)
    genanki.Package(deck_ins).write_to_file("output1.apkg")
    return


def gen_apkg_for_moji_collection(class_num=1):
    word_list = get_word_list_of_moji_collection()
    # 模板
    my_model = genanki.BASIC_AND_REVERSED_CARD_MODEL
    # 牌组 step 2
    my_deck = genanki.Deck(2059400111, "ビジネス日本語::" + str(class_num))
    gen_apkg_by_word_list(my_model, my_deck, word_list)
    pass


def exit():
    os._exit(1)


def run():
    gen_apkg_for_moji_collection(3)
    pass


if __name__ == "__main__":
    run()
