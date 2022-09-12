# Mmq's Data Science Training
# Created at: 2022/9/11 23:17

import numpy as np
import pandas as pd
import akshare as ak
import matplotlib
import matplotlib.pyplot as plt
import main_info_output as iop

index='000016'
history_point=ak.stock_zh_index_daily_em(symbol=iop.index_to_index_withregion[index])
history_point.rename(columns={'date':'trade_date'},inplace=True)
history_point['trade_date']=history_point['trade_date'].astype('datetime64')
history_point=history_point.set_index('trade_date')
history_point=history_point['close']

index_madeup = pd.read_csv(iop.index_dic[index]+'.csv')
index_stock_df=index_madeup['成分券代码'].head(3)
res=pd.DataFrame()
for index_stock in index_stock_df:
    stock_history = ak.stock_a_lg_indicator(index_stock)
    res=pd.concat([res,stock_history])
res['盈利']=res['total_mv']/res['pe_ttm']
res['净资产']=res['total_mv']/res['pb']
res_after=res.groupby('trade_date').sum()
res_after['after_pe_ttm']=res_after['total_mv']/res_after['盈利']
res_after['after_pb_ttm']=res_after['total_mv']/res_after['净资产']
res_after.index=res_after.index.astype('datetime64[ns]')

res_after['close']=history_point[history_point.index.isin(res_after.index)]
output=res_after.dropna(axis=0,how='any')

x=output.index
y1=output['close']
y2=output['after_pe_ttm']
y3=output['after_pb_ttm']
fig,ax1=plt.subplots()
ax1.set_xlabel('日期',fontproperties="SimHei")
ax1.set_ylabel('点位',fontproperties="SimHei")
ax1.plot(x,y1,color='blue',linewidth=1.5,label='指数点位')
ax1.legend(loc='upper left')
ax1.grid()
ax2=ax1.twinx()
ax2.set_ylabel('估值',fontproperties="SimHei")
ax2.plot(x,y2,color='red',linewidth=0.5,label='市盈率-动态')
ax2.plot(x,y3*10,color='yellow',linewidth=0.5,label='市净率*10')
ax2.legend(loc='upper right')
fig.tight_layout()
plt.show()


