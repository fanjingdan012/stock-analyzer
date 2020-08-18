import xueqiu.xueqiu_crawler as xueqiu_crawler
import stock_reader
import industry
import data_preprocessor
import chart.is_cfs_bs_chart as is_cfs_bs_chart
if __name__=="__main__":


    str_stock = 'SZ002488'

    # step 0 download
    # xueqiu_crawler.get_reports_for_1_stock(str_stock)
    #
    # # step 1 append
    # data_preprocessor.adapt(str_stock,'bs',isIndustry=False)
    # data_preprocessor.adapt(str_stock, 'is',isIndustry=False)
    # data_preprocessor.adapt(str_stock, 'cfs',isIndustry=False)
    #
    # # # step 2 merge is cfs
    # df_is_cfs = data_preprocessor.merge_is_cfs(str_stock,isIndustry=False)
    # # #
    # # # # step 3 merge is_cfs bs
    # df_is_cfs_bs = data_preprocessor.merge_is_cfs_bs_match_enddate_bsdate(str_stock,isIndustry=False)
    # df_is_cfs_bs_begin = data_preprocessor.merge_is_cfs_bs_match_begindate_bsdate(str_stock)
    #
    # # # step 3.1 calculate some rates
    # data_preprocessor.calc_profit_ability(str_industry)

    # # step 4 draw chart
    # # step 4.1 draw chart by stocks
    is_cfs_bs_chart.draw_industry_is_cfs_bs_chart_for_stock( str_stock)

