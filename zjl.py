# -*- code:gbk -*-
import time
from urllib import request

import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


# 有中文出现的情况，需要u'内容'

def get_timstamp():
    timestamp = int(int(time.time()) / 30)
    return str(timestamp)


timestamp = get_timstamp()
print(timestamp)

stock_num = 4000

# http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx/JS.aspx?type=ct&st=(BalFlowMain)&sr=-1&p=1&ps=50&js=var%20UmmtoOzG={pages:(pc),date:%222014-10-22%22,data:[(x)]}&token=894050c76af8597a853f5b408b759f5d&cmd=C._AB&sty=DCFFITA&rt=49714689
# 894050c76af8597a853f5b408b759f5d

url_get = 'http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx/JS.aspx?type=ct&st=(BalFlowMain)&sr=-1&p=1' \
          '&ps=' + str(stock_num) + '&js=var%20tUeSuhKk={pages:(pc),date:%222014-10-22%22,data:[(x)]}' \
                                    '&token=894050c76af8597a853f5b408b759f5d&cmd=C._AB&sty=DCFFITA' \
                                    '&rt=' + str(timestamp)

url = 'http://data.eastmoney.com/zjlx/detail.html'
url = url_get
# url = 'http://data.eastmoney.com/zjlx/000651.html'
headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, sdch',
           'Connection': 'keep-alive',
           'Host': 'data.eastmoney.com',
           'Referer': 'http://data.eastmoney.com/center/',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
           }
opener = request.build_opener()
opener.add_handlers = [headers]
try:
    data = opener.open(url, timeout=10).read().decode('utf-8', 'ignore')
    start_pos = data.index('["')
    end_pos = data.index('"]')
    json_data = data[(start_pos + 2):end_pos]
    # print(json_data)
    data_new = json_data.split('","')

except Exception as er:
    print('错误：')
    print(er)

hs = []

for i in range(len(data_new)):
    # print(data_new[i])
    # data_new[0] = ['stock_info']
    data_detail = data_new[i].split(',')
    # print(data_detail)
    col_headers = ['mno', 'no', 'name', 'pr', 'pp', 'tin', 'tp', 'hin', 'hp', 'bin', 'bp', 'min', 'mp', 'sin', 'sp',
                   'time']
    # df = pd.DataFrame(data_detail)
    hs.append(data_detail)
    # print(hs)
df = pd.DataFrame(hs, columns=col_headers)
# print(df)
# hs.info()
# df.to_csv('20170407_1500.csv')
# df_show_org = df.sort_values(by='tp', ascending=False)[:10]
df_show_org = df.iloc[:10, [2, 6]]
df_show = df_show_org.apply(lambda x: pd.to_numeric(x, errors='ignore'))

print(df_show)

# fig = plt.figure()

# pd.options.display.style = 'default'
df_plot = df_show.plot(kind='bar', x=df_show['name'],
                       title='tin-top10', legend=True)
fig = df_plot.get_figure()
# fig.savefig("20170407")
plt.show()
