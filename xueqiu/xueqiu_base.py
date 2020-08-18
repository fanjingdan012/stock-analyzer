#  -*- coding: utf-8 -*-

import urllib.request
import json
#import eastmoney.eastmoneyStockList
# import stock_reader
#import MySQLdb
import xlrd
import xlwt
# from xlutils.copy import copy
import os
import json
import sys


def get_headers ():
    return {#'X-Requested-With': 'XMLHttpRequest',
           #'Referer': 'http://xueqiu.com/p/ZH010389',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
           #'Host': 'xueqiu.com',
           #'Connection':'keep-alive',
           #'Accept':'*/*',
           'cookie':
           'device_id=24700f9f1986800ab4fcc880530dd0ed; s=bx1rh9f53p; xq_a_token=69a6c81b73f854a856169c9aab6cd45348ae1299; xq_r_token=08a169936f6c0c1b6ee5078ea407bb28f28efecf; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTU5ODMyMzAwNCwiY3RtIjoxNTk3NzE1NjQwNzg3LCJjaWQiOiJkOWQwbjRBWnVwIn0.ojm2GXVcR4svaKvHvAxoEZqYyX9A4NKMHhxCbXxfaGb7mUVTrwpyNsGCC92V3VCpqmLqA0u9bi15Lq53hvKJQ8Kes9fbvJBZ9z7o3oqKFpMWvGr4j1lQucyGCPgSXyT9Kw5GHOMc6Tdv5PD5SjfmZKTjg0BgxcW8okcZGrbDhs5URNReiI9BBXQkbe7LPahtK34Q17mixN9V1Ej5-HT3NO19NnlNLAPY55_oVmYC3i9_28H9B1d6x1RGAMHjg_wUvMc6UgupdK4q_6VHBYUgrG04nftigLchXGAOD-IJKY0Pp0r2rkIAqqtD6mZFztA2plxjm0u4NknhFauJf5Xcvw; u=901597715679405; cookiesu=901597715679405; Hm_lvt_1db88642e346389874251b5a1eded6e3=1597715680; is_overseas=0; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1597715729'
     }


def get_response(url):
    headers = get_headers()
    req = urllib.request.Request(url, headers=headers)
    content = urllib.request.urlopen(req).read().decode('utf-8')
    return content


def get_data(stock_list, urlPattern, fileName):
    """
    deprecated
    """
    f = open(fileName+".txt", "a",encoding='utf-8')
    XUEQIU_DOMAIN = 'https://xueqiu.com'

    # stock_list = readStockList.read_stock_list(sh_sz, range_start, range_end)
    print(stock_list)
    results = []
    for index, row in stock_list.iterrows():
        stock=row['code']
        result = [stock]
        url = XUEQIU_DOMAIN+urlPattern+'&symbol=' + stock
        print(url)
        f.write(url)
        f.write('\n')
        result.append(row['name'])
        result.append(url)
        content = get_response(url)
        print(content)
        f.write(content)
        f.write('\n')
        result.append(content)
        results.append(result)
    f.close()
    return results




def write_price_xls(  results,file_dir):

    for i in range(0, len(results)):
        result = results[i]
        stock = result[0]
        href = result[1]
        jsonStr = result[2]
        data = json.loads(jsonStr)
        if (('chartlist' in data) and (data['chartlist'] is not None)):
            field_col_dict = dict()
            newwb = xlwt.Workbook(encoding='utf-8')
            sheet = newwb.add_sheet('Day')
            row = 1
            sheet.write(0, 0, 'stock')
            sheet.write(0, 1, 'href')
            listJson = data['chartlist']
            for item in listJson:
                sheet.write(row, 0, stock)
                sheet.write(row, 1, href)
                for key, value in item.items():
                    col = field_col_dict.get(key,-1)
                    if col == -1:
                        if field_col_dict:
                            col = max(field_col_dict.values())+1
                        else:
                            col = 2
                        sheet.write(0, col, key)
                        field_col_dict[key]=col
                        print('newly added col:'+key)
                    sheet.write(row, col, value)
                row = row+1
        file_name1 = file_dir +stock+ ".xls"
        newwb.save(file_name1)


def create_dir_if_not_there(path, dir_name):
    """ Checks to see if a directory exists in the users home directory, if not then create it. """
    if not os.path.exists(dir_name):
        os.mkdir(os.path.join(path, dir_name))