# Mmq's Data Science Training
# Created at: 2022/8/31 22:26
import numpy as np
import pandas as pd
import akshare as ak
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rc("font", family='Microsoft YaHei')

to_plot_info = ak.stock_zh_index_daily_em(symbol="sh000300")  #导入指数历史行情数据
# print(to_plot_info.info())
x=to_plot_info['date']
y=(to_plot_info['open']+to_plot_info['open'])/2
plt.plot(y)

plt.title('xx指数历史点位图')
plt.xlabel('日期开始自:'+str(to_plot_info.iloc[0].loc['date']))
plt.ylabel('指数点位')
# xticks改变间隔
# xlim设定x轴范围
plt.savefig('沪深300指数历史点位图.jpg')
print('沪深300指数历史点位图完成保存')
plt.show()

