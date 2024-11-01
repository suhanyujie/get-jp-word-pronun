import genanki
from pathlib import Path

DIY_MODEL = genanki.Model(
    1728714695620,
    "Basic (and reversed card) -jp",
    fields=[
        {
            "name": "Front",
            "font": "Arial",
        },
        {
            "name": "Back",
            "font": "Arial",
        },
    ],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{furigana:Front}}",
            "afmt": "{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}",
        },
        {
            "name": "Card 2",
            "qfmt": "{{Back}}",
            "afmt": "{{FrontSide}}\n\n<hr id=answer>\n\n{{furigana:Front}}",
        },
    ],
    css=".card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n",
)


def gen_apkg_by_word_list(model_ins, deck_ins, file_path=""):
    contents = Path(file_path).read_text(encoding="utf-8")
    line_arr = contents.splitlines()
    for line in line_arr:
        info_arr = line.split("-")
        if len(info_arr) == 0:
            continue
        word_part = info_arr[0].strip()
        meaning = info_arr[1].strip()
        tmp_note = genanki.Note(model=model_ins, fields=[word_part, meaning])
        deck_ins.add_note(tmp_note)
    genanki.Package(deck_ins).write_to_file("output1.apkg")
    return


def gen_apkg_by_class_num():
    gen_apkg_by_word_list(my_model, my_deck, "./data/manabou-kanji/tmp20241101.txt")
    pass


# step 1 选择合适的课时
class_num = "11"
# 模板
my_model = DIY_MODEL
# 牌组 step 2
deck1 = "学ぼうー日本語中級::漢字1-7"
deck7 = "学ぼうー日本語中級::漢字7-10"
deck21 = "学ぼうー日本語中級::語彙21-33"
deck34 = "学ぼうー日本語中級::語彙34-40"
deck35 = "学ぼうー日本語中級::語彙35"
deck36 = "学ぼうー日本語中級::語彙36"

my_deck = genanki.Deck(2059400110, deck7)
# 增加卡片
# my_note = genanki.Note(model=my_model, fields=["Capital of Argentina", "Buenos Aires"])
# my_deck.add_note(my_note)
# 生成牌组文件
# genanki.Package(my_deck).write_to_file("output1.apkg")
# step 3 run
gen_apkg_by_class_num()
