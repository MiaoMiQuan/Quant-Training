# Mmq's Data Science Training
# Created at: 2022/8/29 22:51
import numpy as np
import pandas as pd
import akshare as ak
import related_function as rf

global index_dic
index_dic={'000016':'上证50','000300':'沪深300','000905':'中证500','000922':'中证红利'}  #要查看的指数列表
index_dic_withregion={'sh000016':'上证50','sh000300':'沪深300','sh000905':'中证500','sh000922':'中证红利'}

for index_num in index_dic.keys():
    index_component = ak.index_stock_cons_weight_csindex(symbol=index_num)   #获取指数信息
    index_component['成分券代码']=index_component['成分券代码'].astype('int64')  #代码转换为int64
    index_component=index_component.set_index('成分券代码')           #代码设置成index
    index_component=rf.add_pbpe_info(index_component)    #补充相关信息
    index_component = index_component.sort_values(by=['权重'],ascending=False)     #把指数信息按指数权重排序
    index_component.to_csv(index_dic[index_num]+'.csv',encoding='utf_8_sig')     #输出至csv
    print('...'+index_dic[index_num]+'...'+'信息输出完成')               #打印输出成功信息

print('-'.center(60,'-'))

rf.show_index_ccurrent_pbpe(index_dic)

