import genanki
from pathlib import Path

# 模板
my_model = genanki.BASIC_AND_REVERSED_CARD_MODEL
# 牌组 step 1
my_deck = genanki.Deck(2059400110, "学ぼうー日本語初中級::01")
# 增加卡片
# my_note = genanki.Note(model=my_model, fields=["Capital of Argentina", "Buenos Aires"])
# my_deck.add_note(my_note)
# 生成牌组文件
# genanki.Package(my_deck).write_to_file("output1.apkg")


def gen_apkg_by_word_list(model_ins, deck_ins, file_path=""):
    contents = Path(file_path).read_text(encoding="utf-8")
    line_arr = contents.splitlines()
    for line in line_arr:
        info_arr = line.split(", ")
        if len(info_arr) == 0:
            continue
        kanji = info_arr[0]
        furigana = info_arr[1]
        meaning = info_arr[2]
        tmp_note = genanki.Note(
            model=model_ins, fields=[kanji + " | " + furigana, meaning]
        )
        deck_ins.add_note(tmp_note)
    genanki.Package(deck_ins).write_to_file("output1.apkg")
    return


# step 2 调整，读取合适的单词文件
# step 3 run
gen_apkg_by_word_list(my_model, my_deck, "./data/manabou3-1_with_tone.txt")
