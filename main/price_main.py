import sys
sys.path.append('../xueqiu')
sys.path.append('../')
sys.path.append('../chart')
sys.path.append('.')
import xueqiu.xueqiu_industry_price as xueqiu_industry_price
import time
import my_util

if __name__=="__main__":
    date_str = time.strftime("%Y-%m-%d", time.localtime())
    print('today is '+date_str)
    industry_df = xueqiu_industry_price.read_industry_df()
    data = xueqiu_industry_price.get_xueqiu_industry_quote(industry_df, my_util.get_abs_path()+'/data/industry_quote/'+date_str)
    xueqiu_industry_price.write_csv(date_str)