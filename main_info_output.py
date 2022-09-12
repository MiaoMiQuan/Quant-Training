# Mmq's Data Science Training
# Created at: 2022/8/29 22:51
import datetime

import numpy as np
import pandas as pd
import akshare as ak
import datetime
import related_function as rf

global index_dic
global index_dic_withregion
global buy_target_point_E
index_dic={'000016':'上证50','000300':'沪深300','000905':'中证500','000852':'中证1000','000922':'中证红利','000990':'全指消费','000991':'全指医药','000993':'全指信息','399989':'中证医疗'}  #要查看的指数列表
index_dic_withregion={'sh000016':'上证50','sh000300':'沪深300','sh000905':'中证500','sh000852':'中证1000','sh000922':'中证红利','sh000990':'全指消费','sh000991':'全指医药','sh000993':'全指信息','sz399989':'中证医疗'}
index_to_index_withregion={'000016':'sh000016','000300':'sh000300','000905':'sh000905','000852':'sh000852','000922':'sh000922','000990':'sh000990','000991':'sh000991','000993':'sh000993','399989':'sz399989'}
buy_target_point_E={'上证50':0,'沪深300':3500,'中证500':4800,'中证1000':5800,'中证红利':0,'全指消费':11700,'全指医药':9700,'全指信息':4600,'中证医疗':7900}


if __name__ == '__main__':
    start_time_multi=datetime.datetime.now()
    for index_num in index_dic.keys():
        #准备阶段
        start_time_single=datetime.datetime.now()
        index_component = ak.index_stock_cons_weight_csindex(symbol=index_num)   #获取指数信息
        index_component['成分券代码']=index_component['成分券代码'].astype('int64')  #代码转换为int64
        index_component=index_component.set_index('成分券代码')           #代码设置成index
        #加工阶段
        index_component=rf.add_pbpe_info(index_component)    #补充相关信息
        index_component = index_component.sort_values(by=['权重'],ascending=False)     #把指数信息按指数权重排序
        #输出阶段
        index_component.to_csv(index_dic[index_num]+'构成.csv',encoding='utf_8_sig')     #指数全部信息输出至csv
        rf.show_index_current_pbpe(index_num)      #展示指数当前的pb、pe信息
        rf.show_index_current_point(index_to_index_withregion[index_num])      #展示指数当前点位
        rf.buy_target_point_distance_E(index_to_index_withregion[index_num])  #展示现价比E大的目标点位高多少
        history_info=rf.save_index_history(index_num)   #保存指数点位、估值历史信息库
        rf.draw_index_history(history_info,index_num)  #打印并保存指数历史趋势图
        #结束阶段
        end_time_single=datetime.datetime.now()
        time_used_single=end_time_single-start_time_single
        print(index_dic[index_num],'信息输出完成','用时',time_used_single.seconds//60,'分钟',time_used_single.seconds%60,'秒')
        print('-'.center(60,'-'))
    end_time_multi=datetime.datetime.now()
    time_used_multi=end_time_multi-start_time_multi
    print('信息全部输出完成','总用时',time_used_multi.seconds//60,'分钟',time_used_multi.seconds%60,'秒')