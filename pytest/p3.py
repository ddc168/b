import pandas as pd
import numpy as np

#读取病案表

surg_2015 = pd.read_csv("D:\\git\\bak\datas\\2015drg\\exp_2015q1_wt4_surgery.csv")
diag_2015 = pd.read_csv("D:\\git\\bak\datas\\2015drg\\exp_2015q1_wt4_diagnose.csv")
wt4_2015 = pd.read_csv("D:\\git\\bak\datas\\2015drg\\exp_2015q1_wt4_utf8.csv")

#读取规则表
mdc_2015 = pd.read_json("D:\\git\\bak\datas\\rule_2015_1229_bj_mdc.json", encoding="utf_8_sig")
adrg_2015 = pd.read_json("D:\\git\\bak\datas\\rule_2015_1229_bj_adrg.json", encoding="utf_8_sig")
drg_2015 = pd.read_json("D:\\git\\bak\datas\\rule_2015_1229_bj_drg.json", encoding="utf_8_sig")
icd10_2015 = pd.read_json("D:\\git\\bak\datas\\rule_2015_1229_bj_icd10.json", encoding="utf_8_sig")
icd9_2015 = pd.read_json("D:\\git\\bak\datas\\rule_2015_1229_bj_icd9.json", encoding="utf_8_sig")

wt4_2015['surg'] = pd.np.empty((len(wt4_2015), 0)).tolist()
wt4_2015['diag'] = pd.np.empty((len(wt4_2015), 0)).tolist()

#def reduce_surg(x):
#    {x:y} = x[0]
##    wt4_2015.loc[wt4_2015["B_WT4_V1_ID"] == x]['surg'].append(y)
#surg_2015.head()[['B_WT4_V1_ID','OPERATION_CODE']].apply(lambda x: reduce_surg(x))

#wt4_2015_1 = wt4_2015.join(surg_2015,on='B_WT4_V1_ID',lsuffix='_left',rsuffix='_right')     
#wt4_2015_1.info()



diag = diag_2015.head(100)

a = diag.groupby('B_WT4_V1_ID')['DIAGNOSE_CODE'].agg({'diags': lambda x:list(x)})

b = diag.pivot_table(index='B_WT4_V1_ID',columns='DIAGNOSE_CODE')



