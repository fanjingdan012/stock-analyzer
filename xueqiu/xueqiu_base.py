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
           'aliyungf_tc=AQAAAI4xBBot5AQAhF2dtAhi4C7u71Tw; acw_tc=2760822515896845713355773e670a393ef1cfd67c4c7359f4b58477e92093; xq_a_token=328f8bbf7903261db206d83de7b85c58e4486dda; xqat=328f8bbf7903261db206d83de7b85c58e4486dda; xq_r_token=22ab4927b9acb2a02a4efefe14ccbbc589e007cb; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTU5MTg0Mjc0NiwiY3RtIjoxNTg5Njg0NTI0NTk5LCJjaWQiOiJkOWQwbjRBWnVwIn0.PPEp318ISXxjV7NkZHOLMa1n-0WwAmmccBnguPkMGD25k5CBFw0SaJO8nz6EzX7pDcBV7pcJlfEY4Fm7zBbFx0JLCiB3ehi8-UwT8l6m16lxWAM3VEx1WYM15NPEnMW0bGetZDsje-g3uElUvI_fee0kNJ0dnNPvzBp8D1maImkSooCYOTg_Vyhyhp6vc-8mrlgJB5FArY-Zeyqi2lTR-0fOwmE0VEAooBHke9XSBv8HJmTSpfYRU_iEdTzQffkS5hdX6YdoyLhwhG8mUQI2I_PAwKz7kDi3ThGGimgUbEiXRfP9G0OiOdUCeBl68ywOVgcAdoM5YCAsJ0F31rKqQw; u=671589684571340; device_id=24700f9f1986800ab4fcc880530dd0ed; Hm_lvt_1db88642e346389874251b5a1eded6e3=1589684574; s=bx1rh9f53p; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1589684582; __utma=1.1597517040.1589684582.1589684582.1589684582.1; __utmc=1; __utmz=1.1589684582.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmb=1.1.10.1589684582'
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