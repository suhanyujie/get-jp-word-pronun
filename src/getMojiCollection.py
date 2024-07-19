import requests
import toml
import os
import json

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
    # print(type(word["target"]), word["target"])
    # os._exit(1)
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
    print(new_word)
    new_list.append(new_word)
print(new_list)
