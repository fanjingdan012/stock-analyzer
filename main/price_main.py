import xueqiu.xueqiu_industry_price as xueqiu_industry_price

if __name__=="__main__":
    industry_df = xueqiu_industry_price.read_industry_df()
    data = xueqiu_industry_price.get_xueqiu_industry_quote(industry_df, '../data/industry_quote/2020-05-21')
    xueqiu_industry_price.write_csv('2020-05-21')