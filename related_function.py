# Mmq's Data Science Training
# Created at: 2022/8/31 22:13
import numpy as np
import pandas as pd
import akshare as ak

global stock_info
stock_info = ak.stock_zh_a_spot_em()  #获取个股信息汇总
stock_info['代码'] = stock_info['代码'].astype('int64')  # 代码转换为int64
stock_info = stock_info.set_index('代码')  # 代码设置成index
stock_info.to_csv('全股信息.csv', encoding='utf_8_sig')  # 输出至csv

def add_pbpe_info(df):
    df['市盈率-动态']=stock_info[stock_info.index.isin(df.index)]['市盈率-动态']
    df['市净率']=stock_info[stock_info.index.isin(df.index)]['市净率']
    df['总市值']=stock_info[stock_info.index.isin(df.index)]['总市值']
    df['盈利']=stock_info[stock_info.index.isin(df.index)]['总市值']/stock_info[stock_info.index.isin(df.index)]['市盈率-动态']
    df['净资产']=stock_info[stock_info.index.isin(df.index)]['总市值']/stock_info[stock_info.index.isin(df.index)]['市净率']
    return df

def show_index_ccurrent_pbpe(dic):
    for index in dic.values():
        file=index+'.csv'
        df=pd.read_csv(file)
        print(index+'的总计PE为:',round(np.sum(df['总市值'])/np.sum(df['盈利']),2))
        print(index+'的加权PE为:',round(100/np.sum(df['权重']/df['总市值']*df['盈利']),2))
        print(index+'的总计PB为:',round(np.sum(df['总市值'])/np.sum(df['净资产']),2))
        print(index+'的加权PB为:',round(100/np.sum(df['权重']/df['总市值']*df['净资产']),2))
        print('........................')

def show_history():


