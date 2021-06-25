#  -*- coding: utf-8 -*-

import urllib.request
import json
#import eastmoney.eastmoneyStockList
# import stock_reader
#import MySQLdb
# import xlrd
# import xlwt
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
        'device_id=24700f9f1986800ab4fcc880530dd0ed; s=dq18rp9aqh; __utmz=1.1609736450.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_1db88642e346389874251b5a1eded6e3=1623722132; __utmc=1; acw_tc=2760820516241556371925094e7d5c969812e32748bc1fd28a974cf243e65f; xq_a_token=f257b9741beeb7f05f6296e58041e56c810c8ef8; xqat=f257b9741beeb7f05f6296e58041e56c810c8ef8; xq_r_token=2e05f6c50e316248a8a08ab6a47bc781da7fddfb; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTYyNjQwMzgwNSwiY3RtIjoxNjI0MTU1NTg0Mjk2LCJjaWQiOiJkOWQwbjRBWnVwIn0.jBM-6ejjd2PQQcwiPW0GTG_aQKUWeJbafWRNrTG8jBqFzu7g_E5c8uWrJy1Cp8nRBI0r7o7VE_cKcI1oR--l6AF0tm2Yxlyd4y_rZF3lacmDBNK1C7iVpQSBJGBfR3CGz_ETtvfFGwDMIPePqQU0pBFmKEFGBsP5lp2zvNZF4xaThK-OgF40sL84JPWzdhBWBzz4PSbfVMqIv5NVD05MKlHhhnCZ2ZbMW1I-kAlBGaa2a7uUDDc6mUoX7XnKA9YA3kYVMmAW_0TAz8Pn9VTnhSEdfJGHUE-zMIAThjDpQeDH4O3H0uCYEf3Y030VWED1Gqv63la4skQY34_HA50pYA; u=641624155637206; __utma=1.1208258989.1609736450.1623722138.1624155648.4; __utmt=1; __utmb=1.1.10.1624155648; is_overseas=0; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1624155674'
           # 'device_id=24700f9f1986800ab4fcc880530dd0ed; s=dq18rp9aqh; __utmz=1.1609736450.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); acw_tc=2760820116237221316058756e140f260d25dd5b4c353289fd7ddbfc3aafa9; xq_a_token=ac3c2b00373aafa819dd63230fff55140e7d0bb4; xqat=ac3c2b00373aafa819dd63230fff55140e7d0bb4; xq_r_token=c73c6ef7939ae99173067d99572528058c22bed7; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTYyNTEwNzgwNiwiY3RtIjoxNjIzNzIyMDc0MTI3LCJjaWQiOiJkOWQwbjRBWnVwIn0.RQ9ipgkhqFY1Bj-3cmbfi8pHdo2agNfkVbqdB6ovRIrvda6Ycq131O1tJTtw9tUyPOMoG1AVymXR2pzYsE-go9EnmEhORbZZF-O1vWhR54szE3kN8cBZWUDeRoRJQjjsTQqYDeyWq5Puz1OwmRb0mEVv5L89INdUGhc1UKTs-KZrL_Xg9boWnbVOPGGLln7OWa_yM_bVR1fX0cLIE8U6cl_ni0_2iyDuyTiGR7d-s2Xvhk4OyH4b4ft5zWASgvtJFzFjfevT1ceDpv_Dx-hai4u-FX57wIliatpoLV7W0qmHqreSsnSaSJmepYoEEeLdCMSHnqixS01Twf7pnJoSJQ; u=511623722131615; Hm_lvt_1db88642e346389874251b5a1eded6e3=1623722132; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1623722138; __utma=1.1208258989.1609736450.1609742854.1623722138.3; __utmc=1; __utmt=1; __utmb=1.1.10.1623722138'
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