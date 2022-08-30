# Mmq's Data Science Training
# Created at: 2022/8/29 22:51
import akshare as ak
index_list=['000016','000300','000905','000922']
for index_num in index_list:
    index_component = ak.index_stock_cons_weight_csindex(symbol=index_num)
    index_component = index_component.sort_values(by=['权重'],ascending=False)
    print(index_component)
    index_component.to_csv(index_num+'.csv',encoding='utf_8_sig')
