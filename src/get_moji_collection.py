import sys
import requests
import toml
import os
import json
import genanki
from typing import Optional, List, Dict

g_config: Dict = {}


def load_config() -> Dict:
    global g_config
    if len(g_config) == 0:
        config = toml.load("./.env.toml")
        g_config = config
    else:
        config = g_config
    return config


# col_id：收藏夹 id
def get_word_list_of_moji_collection(col_id="") -> List[Dict]:
    global g_config
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
    config = load_config()
    data_str = config["moji"]["dataStr"]
    data = data_str
    # 修改收藏夹 id
    data_dict: Dict[str, str] = json.loads(data)
    if col_id == "":
        data_dict["fid"] = get_current_collect_id()
    else:
        data_dict["fid"] = col_id
    data = json.dumps(data_dict)
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


def gen_apkg_by_word_list(
    model_ins, deck_ins, word_list: List, out_name="output1.apkg"
):
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
    genanki.Package(deck_ins).write_to_file(out_name)
    return


def get_current_collect_name() -> str:
    config = load_config()
    return config["moji"]["current_collect"]


def get_current_collect_id() -> str:
    config = load_config()
    all_collection_dict = config["moji"]["collection_dict"]
    dict_key_by_name = {v: k for k, v in all_collection_dict.items()}
    res = dict_key_by_name[get_current_collect_name()]
    return res


def get_all_collects_map() -> Dict[str, str]:
    config = load_config()
    all_collection_dict = config["moji"]["collection_dict"]
    return all_collection_dict


def get_collection_id_by_name(collection_name="") -> str:
    default_res = ""
    if collection_name == "":
        return default_res
    config = load_config()
    all_collection_dict = config["moji"]["collection_dict"]
    dict_key_by_name = {v: k for k, v in all_collection_dict.items()}
    if collection_name in dict_key_by_name:
        return dict_key_by_name[collection_name]
    return default_res


def gen_apkg_for_moji_collection(class_num=1, collection_name=""):
    col_id = get_collection_id_by_name(collection_name)
    word_list = get_word_list_of_moji_collection(col_id=col_id)
    # 模板
    my_model = genanki.BASIC_AND_REVERSED_CARD_MODEL
    # 牌组 step 2
    if class_num == -1:
        # col 表示 collection，收藏夹
        my_deck = genanki.Deck(2059400111, "ビジネス日本語::" + collection_name)
    else:
        my_deck = genanki.Deck(2059400111, "ビジネス日本語::" + str(class_num))
    out_filename = "output-{}.apkg".format(collection_name)
    gen_apkg_by_word_list(my_model, my_deck, word_list, out_name=out_filename)


def exit():
    os._exit(1)


# single collection: python src/get_moji_collection.py  
# all collections: python src/get_moji_collection.py --type=all
def run():
    arg_arr = sys.argv
    type_val = "default"
    if len(arg_arr) > 1:
        type_val = get_arg_by_key(arg_arr[1], "type")
    match type_val:
        case "all":
            c_map = get_all_collects_map()
            for c_id in c_map:
                tmp_col_name = c_map[c_id]
                gen_apkg_for_moji_collection(-1, collection_name=tmp_col_name)
        case _:
            gen_apkg_for_moji_collection(-1, collection_name=get_current_collect_name())
    pass


# val: `--type testval`
def get_arg_by_key(val: str, k: str) -> str:
    kv_arr = val.split(" ")
    key = kv_arr[0]
    key = key.replace("--", "", 1)
    val = kv_arr[1]
    if key == k:
        return val
    return ""


def test():
    get_current_collect_id()
    pass


if __name__ == "__main__":
    run()
