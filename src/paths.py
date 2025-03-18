from pathlib import Path

root = Path(__file__).parent.parent

DICT_PINYIN = root / "pinyin-data/pinyin.txt"
DICT_WUBI98 = root / "98wubi-tables/wubi98_U.dict.yaml"
DICT_CANGJIE = root / "rime-shuangpin-fuzhuma/cangjie5.dict.yaml"
MOQI_SPELLERS = root / "rime-shuangpin-fuzhuma/moqi_speller.yaml"
MOQI_8105 = root / "rime-shuangpin-fuzhuma/cn_dicts/8105.dict.yaml"
MOQI_41448 = root / "rime-shuangpin-fuzhuma/cn_dicts/41448.dict.yaml"
SPELLERS = root / "src/spellers.yaml"

HANZI_CHARLIST_DIR = root / "hanzi-chars/data-charlist"

MERGED_DICT = root / "merged.csv"