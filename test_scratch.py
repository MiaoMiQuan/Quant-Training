# Mmq's Data Science Training
# Created at: 2022/9/11 23:17

import numpy as np
import pandas as pd
import akshare as ak
import matplotlib
import matplotlib.pyplot as plt
import main_info_output as iop
import datetime

# file=pd.read_csv('中证500历史.csv')
# file_recent_5_year=file.tail(1250)
# pe_ttm_percent_5_year=len(file_recent_5_year[file_recent_5_year['pe_ttm']<file_recent_5_year['pe_ttm'].iloc[-1]])/len(file_recent_5_year)
# print('{:.2%}'.format(pe_ttm_percent_5_year))
#
# file_recent_10_year=file.tail(2500)
# pe_ttm_percent_10_year=len(file_recent_10_year[file_recent_10_year['pe_ttm']<file_recent_10_year['pe_ttm'].iloc[-1]])/len(file_recent_10_year)
# print('{:.2%}'.format(pe_ttm_percent_10_year))

print(ak.stock_a_lg_indicator('858'))


