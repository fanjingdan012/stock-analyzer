import xueqiu.xueqiu_crawler as xueqiu_crawler
import stock_reader
import industry
import data_preprocessor
import chart.is_cfs_bs_chart as is_cfs_bs_chart
if __name__=="__main__":

    # str_industry = '采掘' #DONE
    # str_industry = '传媒'#DONE
    # str_industry = '电气设备'#DONE
    str_industry = '电子'#DONE
    # str_industry = '房地产'#DONE
    # str_industry = '纺织服装' #DONE
    # str_industry = '非银金融'#DONE
    # str_industry = '钢铁'#DONE
    # str_industry = '公用事业' #DONE
    # str_industry = '国防军工'#DONE
    # str_industry = '化工'#DONE
    # str_industry = '机械设备'#DONE
    # str_industry = '计算机'#DONE
    # str_industry = '家用电器' #DONE
    # str_industry = '建筑材料' #DONE
    # str_industry = '建筑装饰' #DONE
    # str_industry = '交通运输' #DONE
    # str_industry = '农林牧渔'DONE
    # str_industry = '汽车' #DONE
    # str_industry = '轻工制造'#DONE
    # str_industry = '商业贸易'DONE
    # str_industry = '食品饮料' DONE
    # str_industry = '通信'DONE
    # str_industry = '休闲服务'#DONE
    # str_industry = '医药生物' #DONE
    # str_industry = '银行'DONE
    # str_industry = '有色金属' #DONE
    # str_industry = '综合'#DONE

    # step 0 download
    # df=stock_reader.read_sw_industry_stock_df(str_industry)
    # for stock_code in df['stock_code']:
    #     xueqiu_crawler.get_reports_for_1_stock(stock_code)



    # step 1 append
    # df_industry = stock_reader.read_sw_industry_stock_df(str_industry)
    # industry.append_reports_for_industry(str_industry,df_industry)
    # data_preprocessor.adapt(str_industry,'bs')
    # data_preprocessor.adapt(str_industry, 'is')
    # data_preprocessor.adapt(str_industry, 'cfs')

    # # step 2 merge is cfs
    # df_is_cfs = data_preprocessor.merge_industry_is_cfs(str_industry)
    # #
    # # # step 3 merge is_cfs bs
    # df_is_cfs_bs = data_preprocessor.merge_industry_is_cfs_bs_match_enddate_bsdate(str_industry)
    # df_is_cfs_bs_begin = data_preprocessor.merge_industry_is_cfs_bs_match_begindate_bsdate(str_industry)
    #
    # # # step 3.1 calculate some rates
    # data_preprocessor.calc_profit_ability(str_industry)

    # # step 4 draw chart
    # # step 4.1 draw chart by stocks
    # df = stock_reader.read_sw_industry_stock_df(str_industry)
    # for stock_code in df['stock_code']:
    #     is_cfs_bs_chart.draw_industry_is_cfs_bs_chart_for_stock(str_industry, stock_code)
    is_cfs_bs_chart.draw_industry_is_cfs_bs_chart_for_stock(str_industry, 'SZ300666')

    # # step 4.2 draw chart by year
    # enddates=['2019-12-31','2018-12-31' ,'2017-12-31'  ]
    # for enddate in enddates:
    #     is_cfs_bs_chart.draw_industry_is_cfs_bs_chart_for_enddate(str_industry, enddate)


    # is_cfs_bs_chart.draw_industry_is_cfs_bs_chart_for_stock(str_industry,'SH600153')
    # is_cfs_bs_chart.draw_industry_is_cfs_bs_chart_for_enddate(str_industry,'20171231')