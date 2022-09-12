# Mmq's Data Science Training
# Created at: 2022/8/31 22:13
import numpy as np
import pandas as pd
import akshare as ak
import main_info_output as iop
import matplotlib
import matplotlib.pyplot as plt
matplotlib.rc("font", family='Microsoft YaHei')  #避免输出格式错误

global stock_info
stock_info = ak.stock_zh_a_spot_em()  #获取个股信息汇总
stock_info['代码'] = stock_info['代码'].astype('int64')  # 代码转换为int64
stock_info = stock_info.set_index('代码')  # 代码设置成index
stock_info.to_csv('全部股票信息.csv', encoding='utf_8_sig')  # 输出至csv

def add_pbpe_info(df):
    df['市盈率-动态']=stock_info[stock_info.index.isin(df.index)]['市盈率-动态']  #从接口获取市盈率信息
    df['市净率']=stock_info[stock_info.index.isin(df.index)]['市净率']    #用df中股票代码做mapping获取市净率
    df['总市值']=stock_info[stock_info.index.isin(df.index)]['总市值']    #用df中股票代码做mapping获取总市值
    df['盈利']=stock_info[stock_info.index.isin(df.index)]['总市值']/stock_info[stock_info.index.isin(df.index)]['市盈率-动态']   #用市盈率反推盈利
    df['净资产']=stock_info[stock_info.index.isin(df.index)]['总市值']/stock_info[stock_info.index.isin(df.index)]['市净率']    #用市净率反推净资产
    return df

def show_index_current_pbpe(index):
    file=iop.index_dic[index]+'构成.csv'   #找到要读的文件
    df=pd.read_csv(file)
    print(iop.index_dic[index],'总计PE:',round(np.sum(df['总市值'])/np.sum(df['盈利']),2))      #算总计PE
    # print(iop.index_dic[index],'的加权PE:',round(100/np.sum(df['权重']/df['总市值']*df['盈利']),2))
    print(iop.index_dic[index],'总计PB:',round(np.sum(df['总市值'])/np.sum(df['净资产']),2))      #算总计PB
    # print(iop.index_dic[index],'的加权PB:',round(100/np.sum(df['权重']/df['总市值']*df['净资产']),2))

def show_index_current_point(index):
    print(iop.index_dic_withregion[index], '指数目前点位:', ak.stock_zh_index_daily_em(symbol=index).iloc[-1].loc['close'])  #输出指数目前点位

def buy_target_point_distance_E(index):
    current=ak.stock_zh_index_daily_em(symbol=index).iloc[-1].loc['close']    #获取指数目前点位
    target=iop.buy_target_point_E[iop.index_dic_withregion[index]]    #mapping到字典里E大推荐的支撑位
    try:
        res=int(current)/int(target)
    except ZeroDivisionError:
        print('E大没给支撑位')
    else:
        print(iop.index_dic_withregion[index],'指数支撑位:',iop.buy_target_point_E[iop.index_dic_withregion[index]])  #输出写死的支撑位
        print('现价比支撑位高:','{:.2%}'.format(current/target-1))    #计算目前价格比支撑位高出的百分比

def save_index_history(index):
    #点位相关数据获取
    history_point = ak.stock_zh_index_daily_em(symbol=iop.index_to_index_withregion[index])  #获取指数历史点位数据
    history_point.rename(columns={'date': 'trade_date'}, inplace=True)  #改名，方便后续数据融合
    history_point['trade_date'] = history_point['trade_date'].astype('datetime64')  #转为规范日期形式
    history_point = history_point.set_index('trade_date')   #用日期当索引
    history_point = history_point['close']  #用收盘价做当日指数点位
    #估值相关数据获取
    index_madeup = pd.read_csv(iop.index_dic[index] + '构成.csv')  #读取指数csv，获取指数组成
    index_stock_df = index_madeup['成分券代码']  #找到指数成分券的代码
    res = pd.DataFrame()
    for index_stock in index_stock_df:
        stock_history = ak.stock_a_lg_indicator(index_stock)  #读某个指数组成股的历史数据
        res = pd.concat([res, stock_history])  #把该指数组成股的历史数据，融合到该指数所有成分股的历史数据大表中，融合后粒度为成分股(300or500个)*日期(5000天)，百万量级
    res['盈利'] = res['total_mv'] / res['pe_ttm']  #用市盈率反推盈利
    res['净资产'] = res['total_mv'] / res['pb']   #用市净率反推净资产
    res_after = res.groupby('trade_date').sum()  #对日期聚合，粒度变为日期粒度
    res_after['after_pe_ttm'] = res_after['total_mv'] / res_after['盈利']  #计算该指数每日总体市盈率-动态
    res_after['after_pb'] = res_after['total_mv'] / res_after['净资产']  #计算该指数每日总体市净率
    res_after.index = res_after.index.astype('datetime64[ns]')  #转为规范日期格式
    #点位、估值数据融合
    res_after['close'] = history_point[history_point.index.isin(res_after.index)]   #用日期当索引，融合每日估值情况和每日点位情况
    output = res_after.dropna(axis=0, how='any')  #扔掉有空值的行
    output=output[['after_pe_ttm','after_pb','close']]
    output.rename(columns={'after_pe_ttm': 'pe_ttm','after_pb':'pb','close':'point'}, inplace=True)
    output.to_csv(iop.index_dic[index]+'历史.csv', encoding='utf_8_sig')  #输出指数点位、估值历史至csv
    return output

def draw_index_history(output,index):
    #画图部分
    x = output.index
    y1 = output['point']
    y2 = output['pe_ttm']
    y3 = output['pb']
    #左轴
    fig, ax1 = plt.subplots()
    ax1.set_xlabel('日期', fontproperties="SimHei")  #设置x轴名称
    ax1.set_ylabel('点位', fontproperties="SimHei")  #设置左y轴名称
    ax1.plot(x, y1, color='blue', linewidth=1.5, label='指数点位')  #画左轴-指数点位
    ax1.legend(loc='upper left')  #标签画在左上角
    #右轴
    ax2 = ax1.twinx() #复制坐标轴
    ax2.set_ylabel('估值', fontproperties="SimHei")  #设置右y轴名称
    ax2.plot(x, y2, color='red', linewidth=0.5, label='市盈率-动态')  #画右轴-市盈率-动态
    ax2.plot(x, y3 * 10, color='yellow', linewidth=0.5, label='市净率*10')  #画右轴-市净率*10(不乘10的话数值太小，无法显示)
    ax2.legend(loc='upper right')  #标签画在右上角
    #画图其他
    plt.title(iop.index_dic[index]+'指数历史点位/估值图') #设置标题
    fig.tight_layout()  #结构展开
    plt.savefig(iop.index_dic[index])  #保存图片
    print(iop.index_dic[index],'指数历史点位/估值图完成保存')
    plt.close()