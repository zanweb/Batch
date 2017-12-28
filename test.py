# -*-coding:utf-8-*-
import pandas as pd
arr = [1, 2, 3, 2, 3, 1, 4]
arr_appear = dict((a, arr.count(a)) for a in arr)
print(arr_appear)
max_arr = max(arr_appear)
print('max_arr:', max_arr)

my_arr = {13.5: 4, 20.0: 5, 8.0: 3}
print('max key:', max(my_arr), 'min key:', min(my_arr))
prices = {
    'ACME': 45.23,
    'AAPL': 612.78,
    'IBM': 205.55,
    'HPQ': 37.20,
    'FB': 10.75
}

min_price = min(zip(prices.values(), prices.keys()))
print('min_price:', min_price)
# min_price is (10.75, 'FB')
max_price = max(zip(prices.values(), prices.keys()))
# max_price is (612.78, 'AAPL')
print('max_price:',max_price)
prices_sorted = sorted(zip(prices.values(), prices.keys()))
# prices_sorted is [(10.75, 'FB'), (37.2, 'HPQ'),
#                   (45.23, 'ACME'), (205.55, 'IBM'),
#                   (612.78, 'AAPL')]
print('prices_sorted:\n', prices_sorted)


parts = [{'part': 'aaaa',
          'Qty': 15,
          'has hole': True,
          'hole dia': {25: 1, 30: 1}},
         {'part': 'bbb',
          'Qty': 5,
          'has hole': True,
          'hole dia': {25: 2, 30: 3}}
         ]

df = pd.DataFrame(parts)
print(df)


# Create a Pandas dataframe from the data.
df = pd.DataFrame({'G1': ['A', 'B', 'C', 'A', 'B', 'C', 'D'],
                   'G2': ['a', 'a', 'a', 'b', 'b', 'b', 'b'],
                   'Data1': [12, 22, 32, 11, 21, 33, 2],
                   'Data2': [1, 3, 2, 5, 2, 5, 2]})

# Create a Pandas Excel writer using XlsxWriter as the engine.
writer = pd.ExcelWriter('pandas_simple.xlsx', engine='xlsxwriter')

# Convert the dataframe to an XlsxWriter Excel object.
df.to_excel(writer, sheet_name='Sheet1')
df = df.groupby(['G1', 'G2'])['Data1', 'Data2'].sum()
df.to_excel(writer, sheet_name='Sheet2', startrow=6)
pd.pivot_table(df, values=['Data1', 'Data2'], rows=['G1', 'G2'])
pd.crosstab(rows=['G1', 'G2'], values=['Data1', 'Data2'])


# Close the Pandas Excel writer and output the Excel file.
writer.save()
