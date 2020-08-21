#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time     :   2019/12/18 12:17
# @Author   :   ZANWEB
# @File     :   Frame_Data_Center_Functions.py in Batch
# @IDE      :   PyCharm

from GUI.Project import UiProject
from GUI.Query88 import Query


def select_functions(function_name, main_window):
    print(function_name)
    if function_name == '项目列表':
        func_reply = project_list(main_window)
    if function_name == '查询88':
        func_reply = query_88(main_window)
    if function_name == '构件输入':
        func_reply = undefined_func()
    if function_name == '构件谁做':
        func_reply = undefined_func()
    if function_name == '构件回收':
        func_reply = undefined_func()
    if function_name == '日报输入':
        func_reply = undefined_func()
    if function_name == '统计查询':
        func_reply = undefined_func()
    if function_name == '手工查询':
        func_reply = undefined_func()
    if function_name == '雇员列表':
        func_reply = undefined_func()
    if function_name == '加班数据':
        func_reply = undefined_func()
    if function_name == '休假数据':
        func_reply = undefined_func()
    if function_name == '加班打印':
        func_reply = undefined_func()
    if function_name == '申请打印':
        func_reply = undefined_func()
    if function_name == '核对打印':
        func_reply = undefined_func()
    if function_name == '休假查询':
        func_reply = undefined_func()
    if function_name == '数据输入':
        func_reply = undefined_func()
    if function_name == '切割清单':
        func_reply = undefined_func()
    if function_name == '项目清单':
        func_reply = undefined_func()
    if function_name == '申请接收':
        func_reply = undefined_func()
    if function_name == '材料清单':
        func_reply = undefined_func()
    if function_name == '材料核对':
        func_reply = undefined_func()
    if function_name == 'BOM生成':
        func_reply = undefined_func()
    if function_name == '口令修改':
        func_reply = undefined_func()
    if function_name == '电话查询':
        func_reply = undefined_func()


def project_list(main_window):
    # print('运行-->项目列表')
    main_window.tab3 = UiProject()

    main_window.tabWidget.clear()
    main_window.tabWidget.tabPosition()
    main_window.tabWidget.addTab(main_window.tab3, '项目信息')
    main_window.tab3.get_user_info(main_window.user_info)
    main_window.tab3.init_data()
    return 0


def query_88(main_window):
    main_window.tab3 = Query()

    main_window.tabWidget.clear()
    main_window.tabWidget.tabPosition()
    main_window.tabWidget.addTab(main_window.tab3, '项目信息')
    main_window.tab3.get_user_info(main_window.user_info)
    # main_window.tab3.init_data()


def undefined_func():
    print('此功能未完工.')
    return 0
