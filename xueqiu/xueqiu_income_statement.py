#-*-coding:utf-8 -*-
import urllib.request
import json
import stock_reader


import os

import xueqiu.xueqiu_base as xueqiu_base
import pandas as pd
def get_abs_path():
    abs_dir = __file__[:__file__.rfind("/")]
    return abs_dir

def getIncomeStatements(shOrSz,rangeStart,rangeEnd):
    headers = xueqiu_base.get_headers()
    stockList = stock_reader.readStockList(shOrSz, rangeStart, rangeEnd)
    print(stockList)
    incomeStatements = []
    for stock in stockList:
        incomeStatement=[]
        url = 'https://xueqiu.com/stock/f10/incstatement.json?symbol=' + stock
        print(url)
        incomeStatement.append(url)
        req = urllib.request.Request(url, headers=headers)
        content = urllib.request.urlopen(req).read().decode('utf-8')
        print(content)
        data = json.loads(content)
        incomeStatement.append(json.dumps(data))
        incomeStatements.append(incomeStatement)
    return incomeStatements




def get_is_for_1_stock(str_stock_code):
    # stock_list=readStockList.read_industry_stock_list_by_code(stock_code)
    # data = get_data(stock_list, '/stock/f10/balsheet.json?size=10000&page=1', '../data/bs_'+stock_id)
    str_response=xueqiu_base.get_response('https://xueqiu.com/stock/f10/incstatement.json?size=10000&page=1&symbol='+str_stock_code)
    # write_f10_xls(1, data, '../data/bs_'+stock_id)
    json_data = json.loads(str_response)

    if (('list' in json_data) & (json_data['list'] is not None)):
        json_list = json_data['list']
        str_list=json.dumps(json_list)
        df = pd.read_json(str_list, orient='records')
        df.to_excel(get_file_name(str_stock_code))

def get_is_for_1_stock_new(str_stock_code, country):
    url = 'https://stock.xueqiu.com/v5/stock/finance/'+country+'/income.json?type=all&is_detail=true&count=10000&symbol='+str_stock_code
    print(url)
    str_response=xueqiu_base.get_response(url)
    # write_f10_xls(1, data, '../data/bs_'+stock_id)
    json_data = json.loads(str_response)['data']

    if (('list' in json_data) & (json_data['list'] is not None)):
        json_list = json_data['list']
        str_list=json.dumps(json_list)
        df = pd.read_json(str_list, orient='records')
        df.to_excel(get_file_name(str_stock_code))

def get_file_name(name):
    # xueqiu_base.create_dir_if_not_there('../','data')
    # xueqiu_base.create_dir_if_not_there('../data', 'is')
    # root_dir = os.path.dirname(os.path.abspath('./stock-analyzer'))
    return get_abs_path() + '/../data/is/is_' + name + '.xlsx'