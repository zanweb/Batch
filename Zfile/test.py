#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :   2020/7/8 11:27
# @Author   :   ZANWEB
# @File     :   test.py in Batch
# @IDE      :   PyCharm

import pandas as pd
import os
import shutil
import html5lib
import requests
from bs4 import BeautifulSoup
import re
import time


def test_01():
    shutil.copy('C:\\Users\\zzimo\\Desktop\\构件清单\\山东英科二期钢构巴特勒组成清单0529.xls','changed.html')
    shutil.copy('changed.html','txt_output.txt')
    time.sleep(2)

    txt = open('txt_output.txt','r').read()

    # Modify the text to ensure the data display in html page

    txt = str(txt).replace('<style> .text { mso-number-format:\@; } </script>','')

    # Add head and body if it is not there in HTML text

    txt_with_head = '<html><head></head><body>'+txt+'</body></html>'

    # Save the file as HTML

    html_file = open('output.html','w')
    html_file.write(txt_with_head)

    # Use beautiful soup to read

    url = r"output.html"
    page = open(url)
    soup = BeautifulSoup(page.read(), features="lxml")
    my_table = soup.find("table",attrs={'border': '1'})

    frame = pd.read_html(str(my_table))[0]
    print(frame.head())
    frame.to_excel('testoutput.xlsx',sheet_name='sheet1', index=False)


def test_02():
    file_path = 'C:\\Users\\zzimo\\Desktop\\构件清单\\山东英科二期钢构巴特勒组成清单0529 - 副本.xls'
    file = open(file_path)
    for line in file:
        line_t = line.replace('\n', '').strip()
        one_line_list = line_t.split('\t')

def test_03():
    file_path = ''

if __name__ is '__main__':
    test_02()