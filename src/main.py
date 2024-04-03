import requests
from bs4 import BeautifulSoup

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

# test
tone = get_jp_tone("めうえ")
print(tone)
tone = get_jp_tone("推薦状")
print(tone)
