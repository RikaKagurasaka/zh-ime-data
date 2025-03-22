from pathlib import Path

root = Path(__file__).parent.parent

DICT_PINYIN = root / "pinyin-data/pinyin.txt"
DICT_WUBI98 = root / "98wubi-tables/wubi98_U.dict.yaml"
DICT_WUBI86 = root / "wubi-convert-cpp/wubi86.dict.txt"
DICT_CANGJIE = root / "Cangjie5/Cangjie5.txt"
DICT_ZHENGMA = root / "rime-zong/lyzm.dict.yaml"
DICT_SIJIAO = root / "rime-zong/sjhm.dict.yaml"
DICT_HUMA = root / "rime-huma/huma.dict/huma.char.dict.yaml"
DICT_XUMA = root / "rime-xuma/schema/xuma.dict.yaml"
DICTS_LIUR = [
    root / "RIME-Liur2024/Rime/liur_Japan.dict.yaml",
    root / "RIME-Liur2024/Rime/liur_Trad.dict.yaml",
    root / "RIME-Liur2024/Rime/liur_TradExt.dict.yaml",
    root / "RIME-Liur2024/Rime/liur_TradToSimp.dict.yaml",
]
MOQI_SPELLERS = root / "rime-shuangpin-fuzhuma/moqi_speller.yaml"
MOQI_8105 = root / "rime-shuangpin-fuzhuma/cn_dicts/8105.dict.yaml"
MOQI_41448 = root / "rime-shuangpin-fuzhuma/cn_dicts/41448.dict.yaml"
SPELLERS = root / "src/spellers.yaml"


HANZI_CHARLIST_DIR = root / "hanzi-chars/data-charlist"

MERGED_DICT = root / "merged.csv"
