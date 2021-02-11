import pandas as pd
import numpy as np

# =============================================================================
# 读取病案表
# =============================================================================
surg_2015 = pd.read_csv("D:\\git\\bak\datas\\2015drg\\exp_2015q1_wt4_surgery.csv")
diag_2015 = pd.read_csv("D:\\git\\bak\datas\\2015drg\\exp_2015q1_wt4_diagnose.csv")
wt4_2015 = pd.read_csv("D:\\git\\bak\datas\\2015drg\\exp_2015q1_wt4_utf8.csv")

# =============================================================================
# 读取规则表
# =============================================================================
mdc_2015 = pd.read_json("D:\\git\\bak\datas\\rule_2015_1229_bj_mdc.json", encoding="utf_8_sig")
adrg_2015 = pd.read_json("D:\\git\\bak\datas\\rule_2015_1229_bj_adrg.json", encoding="utf_8_sig")
drg_2015 = pd.read_json("D:\\git\\bak\datas\\rule_2015_1229_bj_drg.json", encoding="utf_8_sig")
icd10_2015 = pd.read_json("D:\\git\\bak\datas\\rule_2015_1229_bj_icd10.json", encoding="utf_8_sig")
icd9_2015 = pd.read_json("D:\\git\\bak\datas\\rule_2015_1229_bj_icd9.json", encoding="utf_8_sig")

# =============================================================================
# 取少量数据用于开发时的快速测试
# =============================================================================
diag = diag_2015.head(100)
surg = surg_2015.head(100)
wt4 = wt4_2015.head(100)

# =============================================================================
# 将诊断表、手术表聚合后，合并到wt4病案主表中
# =============================================================================
a = diag_2015.groupby('B_WT4_V1_ID')['DIAGNOSE_CODE'].agg({'diags': lambda x:list(x)})
b = surg_2015.groupby('B_WT4_V1_ID')['OPERATION_CODE'].agg({'opers': lambda x:list(x)})
wt4_2015.index = wt4_2015['B_WT4_V1_ID']
w1 = wt4_2015.join(a)
w1 = w1.join(b)

# =============================================================================
# 使用规则表，开始分组逻辑判断，最终得到drg、adrg、mdc分组结果
# =============================================================================
w = w1.head(1)

def reduce_1(x):
    return x.index

w['mdc'] = w.apply(lambda x: reduce_1(x))
print(w['mdc'])

