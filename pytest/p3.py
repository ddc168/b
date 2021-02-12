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
wt4_2015 = wt4_2015.join(a)
wt4_2015 = wt4_2015.join(b)

# =============================================================================
# 使用规则表，开始分组逻辑判断，最终得到drg、adrg、mdc分组结果
# =============================================================================
w1 = wt4_2015.head(10)
w1.fillna(0,inplace = True)

drgs = []
for w in w1.iterrows():
    mdc = ''
    adrg = ''
    drg = ''
    
    diag_main = w[1]['DISEASE_CODE1']
    
    rule_icd10 = icd10_2015.loc[icd10_2015['CODE']==diag_main]
    
    adrg_diag = rule_icd10['adrg']
        
#    adrg = list(adrg_diag)[0][0]
    adrgs = list(adrg_diag)[0]
    for i in adrgs:
        d2_1 = adrg_2015.loc[adrg_2015['ADRG_CODE']==i]
        icd10_B = d2_1['icd10_b']
        icd9_B = d2_1['icd9_b']
        icd9_A = d2_1['icd9_a']
        adrg = i
# =============================================================================
#         
# =============================================================================
#        if len(icd10_B):
#            a = 1
#        if len([val for val in w['diags'] if val in icd10_B]):
#            a = 1
#        else:
#            a = 0
            
    mdc = adrg[0]
    
    rule_adrg = adrg_2015.loc[adrg_2015['ADRG_CODE']==adrg]
    drgs_1 = rule_adrg['drgs_1']
    if list(drgs_1)[0]:
        drg = adrg + list(drgs_1)[0][0]

    drgs.append((w[1]['B_WT4_V1_ID'], mdc, adrg, drg))

# =============================================================================
# 将tuple数组转换为dataframe，再与wt4合并，供下面的DRG分析使用
# =============================================================================
d1 = pd.Series(drgs)
d2 = pd.DataFrame(columns=('B_WT4_V1_ID', 'MDC', 'ADRG', 'DRG'))
d2[['B_WT4_V1_ID', 'MDC', 'ADRG', 'DRG']] = d1.apply(pd.Series)