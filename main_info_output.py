# Mmq's Data Science Training
# Created at: 2022/8/29 22:51
import datetime
import numpy as np
import pandas as pd
import akshare as ak
import datetime
import related_function as rf
import os

global index_dic
global index_dic_withregion
global buy_target_point_E
global to_write_file
# index_dic={'000922':'中证红利'} #跑部分指数
index_dic={'000016':'上证50','000300':'沪深300','000905':'中证500','000852':'中证1000','000922':'中证红利','000990':'全指消费','000991':'全指医药','000993':'全指信息','399989':'中证医疗','000958':'创业成长','000688':'科创50','399971':'中证传媒','000992':'全指金融'}  #要查看的指数列表
index_dic_withregion={'sh000016':'上证50','sh000300':'沪深300','sh000905':'中证500','sh000852':'中证1000','sh000922':'中证红利','sh000990':'全指消费','sh000991':'全指医药','sh000993':'全指信息','sz399989':'中证医疗','sh000958':'创业成长','sh000688':'科创50','sz399971':'中证传媒','sh000992':'全指金融'}
index_to_index_withregion={'000016':'sh000016','000300':'sh000300','000905':'sh000905','000852':'sh000852','000922':'sh000922','000990':'sh000990','000991':'sh000991','000993':'sh000993','399989':'sz399989','000958':'sh000958','000688':'sh000688','399971':'sz399971','000992':'sh000992'}
buy_target_point_E={'上证50':0,'沪深300':3500,'中证500':4800,'中证1000':5800,'中证红利':0,'全指消费':11700,'全指医药':9700,'全指信息':4600,'中证医疗':7900,'创业成长':0,'科创50':0,'中证传媒':0,'全指金融':0}
to_write_file = open('最新信息.txt', mode='w+', encoding='utf_8_sig')


if __name__ == '__main__':
    start_time_multi=datetime.datetime.now()
    for index_num in index_dic.keys():
        #创建文件夹
        if not os.path.exists(str(index_dic[index_num])):
            os.mkdir(str(index_dic[index_num]))
        os.chdir('D:\\Python_Project\\Quant_Training\\'+str(index_dic[index_num]))
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
        history_info = rf.save_index_history(index_num)  # 保存指数点位、估值历史信息库
        rf.show_index_current_point(history_info,index_num)      #展示指数当前点位
        rf.buy_target_point_distance_E(index_to_index_withregion[index_num])  #展示现价比E大的目标点位高多少
        rf.show_index_current_pbpe(history_info,index_num)      #展示指数当前的pb、pe信息
        rf.pbpe_history_5years(history_info,index_num)  #输出5年PE、PB百分位
        rf.pbpe_history_10years(history_info, index_num)  # 输出10年PE、PB百分位
        rf.draw_index_history(history_info,index_num,'-创立起')  #打印并保存指数历史趋势图
        rf.draw_index_history(history_info.tail(1250), index_num, '-5年')  # 打印并保存指数5年趋势图
        rf.draw_index_history(history_info.tail(2500), index_num, '-10年')  # 打印并保存指数10年趋势图
        rf.end()  #画分割线
        #结束阶段
        end_time_single=datetime.datetime.now()
        time_used_single=end_time_single-start_time_single
        print(index_dic[index_num],'信息输出完成','用时',time_used_single.seconds//60,'分钟',time_used_single.seconds%60,'秒')
        print('-'.center(60,'-'))
        os.chdir('D:\\Python_Project\\Quant_Training\\')
    to_write_file.close()
    end_time_multi=datetime.datetime.now()
    time_used_multi=end_time_multi-start_time_multi
    print('信息全部输出完成','总用时',time_used_multi.seconds//60,'分钟',time_used_multi.seconds%60,'秒')