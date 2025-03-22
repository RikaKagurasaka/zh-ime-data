# %%
from paths import MERGED_DICT
from speller import apply_speller_rules
from load_raw import load_hanzi_chars, load_raw_data
import pandas as pd
from functools import reduce
import opencc

s2t = opencc.OpenCC("s2t.json")
t2s = opencc.OpenCC("t2s.json")

# %%
cj_df, wubi98_df, wubi86_df, pinyin_df, moqi_df, sijiao_df, zhengma_df = load_raw_data()
cj_df = cj_df.rename(columns={"code": "cj"})
cj_df = apply_speller_rules(cj_df, "letters2cj", "cj")
wubi98_df = wubi98_df.rename(columns={"code": "wubi98"})
wubi86_df = wubi86_df.rename(columns={"code": "wubi86"})
sijiao_df = sijiao_df.rename(columns={"code": "sijiao"})
zhengma_df = zhengma_df.rename(columns={"code": "zhengma"})
# %%
pron_df = pinyin_df.copy()
pron_df = pron_df.rename(columns={"code": "pinyin"})
pron_df["terra"] = apply_speller_rules(pron_df["pinyin"], "pinyin2terra")
pron_df["mingyue"] = apply_speller_rules(pron_df["terra"], "terra_drop_tone")
pron_df["bopomofo"] = apply_speller_rules(pron_df["terra"], "terra2bopomofo")
pron_df["flypy"] = apply_speller_rules(pron_df["mingyue"], "flypy")
pron_df["ms"] = apply_speller_rules(pron_df["mingyue"], "ms")
pron_df["zrm"] = apply_speller_rules(pron_df["mingyue"], "zrm")
pron_df["sogou"] = apply_speller_rules(pron_df["mingyue"], "sogou")
pron_df["abc"] = apply_speller_rules(pron_df["mingyue"], "abc")
pron_df["ziguang"] = apply_speller_rules(pron_df["mingyue"], "ziguang")

# remove abnormal pron
abnormal_pinyins = ["ǹ", "ń", "ň", "ê̌", "ḿ", "hng", "ề", "ế", "n", "ê̄"]
pron_df = pron_df[~pron_df["pinyin"].isin(abnormal_pinyins)]

pron_terra_df = pron_df.loc[:, ["char", "terra"]]
pron_mingyue_df = pron_df.loc[:, ["char", "mingyue"]]
pron_bopomofo_df = pron_df.loc[:, ["char", "bopomofo"]]
pron_flypy_df = pron_df.loc[:, ["char", "flypy"]]
pron_ms_df = pron_df.loc[:, ["char", "ms"]]
pron_zrm_df = pron_df.loc[:, ["char", "zrm"]]
pron_sogou_df = pron_df.loc[:, ["char", "sogou"]]
pron_abc_df = pron_df.loc[:, ["char", "abc"]]
pron_ziguang_df = pron_df.loc[:, ["char", "ziguang"]]
# %%
moqi_aux = moqi_df.loc[:, ["char", "moqi_aux"]]
moqi_aux["moqi_aux"] = moqi_aux["moqi_aux"].str.split(",")
moqi_aux = moqi_aux.explode("moqi_aux")
moqi_aux = moqi_aux[moqi_aux["moqi_aux"].str.len() == 2]
moqi_aux = moqi_aux.dropna()
xh_aux = moqi_df.loc[:, ["char", "xh_aux"]]
xh_aux["xh_aux"] = xh_aux["xh_aux"].str.split(",")
xh_aux = xh_aux.explode("xh_aux")
xh_aux = xh_aux[xh_aux["xh_aux"].str.len() == 2]
xh_aux = xh_aux.dropna()
zrm_aux = moqi_df.loc[:, ["char", "zrm_aux"]]
zrm_aux["zrm_aux"] = zrm_aux["zrm_aux"].str.split(",")
zrm_aux = zrm_aux.explode("zrm_aux")
zrm_aux = zrm_aux[zrm_aux["zrm_aux"].str.len() == 2]
# %%
dfs = [
    cj_df,
    wubi98_df,
    wubi86_df,
    sijiao_df,
    zhengma_df,
    pron_terra_df,
    pron_bopomofo_df,
    pron_flypy_df,
    pron_ms_df,
    pron_zrm_df,
    pron_sogou_df,
    pron_abc_df,
    pron_ziguang_df,
    moqi_aux,
    xh_aux,
    zrm_aux,
]
to_merge = []
for df in dfs:
    df = df.dropna()
    df = df.drop_duplicates()
    df = df.groupby("char").agg(lambda x: "|".join(x))
    to_merge.append(df)
# %%
merged = reduce(
    lambda left, right: pd.merge(left, right, on="char", how="outer"), to_merge
)

lvl123 = load_hanzi_chars()
slim_merged = merged[~merged["terra"].isna()]
slim_merged = pd.merge(slim_merged, lvl123, on="char", how="left")

# %%
slim_merged["cht"] = (
    slim_merged["char"].apply(lambda c: s2t.convert(c) == c).astype(int)
)
slim_merged["chs"] = (
    slim_merged["char"].apply(lambda c: t2s.convert(c) == c).astype(int)
)
slim_merged
# %%
slim_merged.to_csv(MERGED_DICT, index=False)
# %%
import gzip

with gzip.open(MERGED_DICT.with_suffix(".gz"), "wt") as f:
    slim_merged.to_csv(f, index=False)
# %%
import shutil

shutil.copy(
    MERGED_DICT.with_suffix(".gz"),
    MERGED_DICT.parent.parent / "public" / MERGED_DICT.with_suffix(".gz").name,
)
# %%
