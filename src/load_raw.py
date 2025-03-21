# %%
import re
from paths import *
import pandas as pd


# %%
def find_header_lines_cnt(path: Path):
    is_header = True
    header_lines_cnt = 0
    with open(path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if line.strip() == "...":
                is_header = False
            elif is_header:
                header_lines_cnt += 1
    return header_lines_cnt if not is_header else 0


def load_cangjie():
    """Load and process Cangjie dictionary data"""
    cj_df = pd.read_csv(
        DICT_CANGJIE,
        sep="\t",
        header=None,
        skiprows=10,
        names=range(3),
        comment="#",
    )
    cj_df = cj_df[cj_df[0].str.len() == 1]
    cj_df = cj_df.iloc[:, :2]
    cj_df.columns = ["char", "code"]
    cj_df = cj_df[cj_df["code"].str.contains("z") == 0]
    cj_df = cj_df[~cj_df["code"].str.startswith("yyy")]
    # 由于仓颉码的x在最前面的时候写作「重」，所以为了区分，把在最前面的x替换成z
    cj_df["code"] = cj_df["code"].apply(
        lambda x: re.sub(r"^x+", lambda m: "z" * len(m.group(0)), x)
    )
    return cj_df


def load_wubi98():
    """Load and process Wubi98 dictionary data"""
    wubi_header_lines_cnt = find_header_lines_cnt(DICT_WUBI98)
    wubi_df = pd.read_csv(
        DICT_WUBI98,
        sep="\t",
        header=None,
        skiprows=wubi_header_lines_cnt,
        names=range(4),
        comment="#",
    )
    wubi_df = wubi_df[wubi_df[0].str.len() == 1]
    wubi_df = wubi_df[wubi_df[1].str.contains("z") == 0]
    wubi_df = wubi_df.iloc[:, :2]
    wubi_df.columns = ["char", "code"]
    wubi_df["code"] = wubi_df["code"].str.split(",")
    wubi_df["code"] = wubi_df["code"].apply(lambda x: sorted(x, key=lambda a: len(a)))
    wubi_df = wubi_df.explode("code")
    wubi_df.drop_duplicates(inplace=True)
    return wubi_df


def load_wubi86():
    """Load and process Wubi86 dictionary data"""
    wubi_df = pd.read_csv(
        DICT_WUBI86,
        sep="\t",
        header=None,
        names=range(4),
        comment="#",
    )
    wubi_df = wubi_df[wubi_df[1].str.len() == 1]
    wubi_df = wubi_df[wubi_df[2].str.contains("z") == 0]
    wubi_df = wubi_df.iloc[:, [1, 2]]
    wubi_df.columns = ["char", "code"]
    wubi_df["code"] = wubi_df["code"].str.split(",")
    wubi_df["code"] = wubi_df["code"].apply(lambda x: sorted(x, key=lambda a: len(a)))
    wubi_df = wubi_df.explode("code")
    wubi_df.drop_duplicates(inplace=True)
    return wubi_df


def load_pinyin():
    """Load and process Pinyin dictionary data"""
    pinyin_df = pd.read_csv(
        DICT_PINYIN,
        sep=r"\s+",
        header=None,
        skiprows=2,
        names=range(4),
        encoding="utf-8",
    )
    pinyin_df = pinyin_df.iloc[:, [3, 1]]
    pinyin_df.columns = ["char", "code"]
    pinyin_df["code"] = pinyin_df["code"].str.split(",")
    pinyin_df = pinyin_df.explode("code")
    return pinyin_df


def load_moqi():
    """Load and process Moqi dictionary data"""
    moqi_8105_df = pd.read_csv(
        MOQI_8105,
        sep="[\t;]",
        header=None,
        skiprows=find_header_lines_cnt(MOQI_8105),
        names=range(13),
        comment="#",
    )
    moqi_41448_df = pd.read_csv(
        MOQI_41448,
        sep="[\t;]",
        header=None,
        skiprows=find_header_lines_cnt(MOQI_41448),
        names=range(13),
        comment="#",
    )
    moqi_df = pd.concat([moqi_8105_df, moqi_41448_df])
    moqi_df = moqi_df[moqi_df[0].str.len() == 1]
    moqi_df = moqi_df.iloc[:, [0, 1, 2, 3, 4]]
    moqi_df.columns = ["char", "pinyin", "moqi_aux", "xh_aux", "zrm_aux"]
    return moqi_df


# %%
def load_sijiao():
    """Load and process Sijiao dictionary data"""
    sijiao_df = pd.read_csv(
        DICT_SIJIAO,
        sep="\t",
        header=None,
        skiprows=find_header_lines_cnt(DICT_SIJIAO),
        names=range(3),
        comment="#",
    )
    sijiao_df = sijiao_df[sijiao_df[0].str.len() == 1]
    sijiao_df = sijiao_df.iloc[:, [0, 1]]
    sijiao_df.columns = ["char", "code"]
    sijiao_df["code"] = sijiao_df["code"].str.slice(5)
    sijiao_df.drop_duplicates(inplace=True)
    return sijiao_df


def load_zhengma():
    """Load and process Zhengma dictionary data"""
    zhengma_df = pd.read_csv(
        DICT_ZHENGMA,
        sep="\t",
        header=None,
        skiprows=find_header_lines_cnt(DICT_ZHENGMA),
        names=range(3),
        comment="#",
    )
    zhengma_df = zhengma_df[zhengma_df[0].str.len() == 1]
    zhengma_df = zhengma_df.iloc[:, [0, 1]]
    zhengma_df.columns = ["char", "code"]
    zhengma_df.sort_values(by="code", key=lambda x: x.str.len(), inplace=True)
    return zhengma_df


# %%
def load_raw_data():
    """Load all raw dictionary data and return as a tuple of dataframes.

    Returns:
        tuple: (cangjie_df, wubi98_df, wubi86_df, pinyin_df, moqi_df)
    """
    cj_df = load_cangjie()
    wubi98_df = load_wubi98()
    wubi86_df = load_wubi86()
    pinyin_df = load_pinyin()
    moqi_df = load_moqi()
    sijiao_df = load_sijiao()
    zhengma_df = load_zhengma()

    return cj_df, wubi98_df, wubi86_df, pinyin_df, moqi_df, sijiao_df, zhengma_df


# %%
def load_hanzi_chars():
    """Load all hanzi characters from the hanzi-chars directory"""
    load_func = lambda lvl: pd.read_csv(
        HANZI_CHARLIST_DIR / f"《通用规范汉字表》（2013年）{lvl}级字.txt",
        header=None,
        names=["char"],
        comment="#",
        skip_blank_lines=True,
    )
    lvl1 = load_func("一")
    lvl2 = load_func("二")
    lvl3 = load_func("三")
    lvl1["lvl"] = 1
    lvl2["lvl"] = 2
    lvl3["lvl"] = 3
    lvl123 = pd.concat([lvl1, lvl2, lvl3])
    return lvl123


# %%
