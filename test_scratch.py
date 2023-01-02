# Mmq's Data Science Training
# Created at: 2022/9/11 23:17

import numpy as np
import pandas as pd
import akshare as ak
import matplotlib
import matplotlib.pyplot as plt
import main_info_output as iop
import datetime
import os

index_stock='000300'
stock_a_lg_indicator_df = ak.stock_a_lg_indicator(symbol=str(index_stock).rjust(6,'0'))
print(stock_a_lg_indicator_df)