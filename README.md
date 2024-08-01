## 日语单词助手

- 查询日语单词的音调，主要针对《大家的日本语 中 1》，和《学ぼう、日本語》教材的单词查询，并写入文件
- 根据查询的单词信息，制作卡片，生成 apkg 文件，导入 anki 中
- moji 收藏夹导出，并生成 [anki](https://apps.ankiweb.net/) 卡片，方便用手机记忆单词

## 功能列表

- 基于 [moji](https://www.mojidict.com/) [查询单词含义](./src/main.py)，写入到文件，[并生成 anki 卡片](./src/gen_card.py)，方便用手机记忆单词
- 从 [moji](https://www.mojidict.com/) 收藏夹导出单词，[并生成 anki 卡片](./src/get_moji_collection.py)，方便用手机记忆单词。（需要开通 moji 会员，才能使用收藏夹功能）
- 《学ぼう、日本語》教材的单词查询，生成 apkg 文件，导入 anki 中

## ref

- 《大家的日语 中 1》单词来源 https://github.com/wang1zhen/anki-decks/blob/main/%E4%B8%AD%E7%BA%A7%E8%AF%8D%E6%B1%87/1/01.txt
