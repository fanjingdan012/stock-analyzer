import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from mpl_toolkits.mplot3d import axes3d
import industry
import chart.is_chart as is_chart
import chart.bs_chart as bs_chart
import chart.cfs_chart as cfs_chart
import chart.is_cfs_chart as is_cfs_chart
import stock_reader
from matplotlib.font_manager import FontProperties
import data_preprocessor




def draw_industry_is_cfs_bs_subplot(ax,df,x):
    width = 0.10
    # cfs var

    stock_code = df['stock_code']
    stock_name = df['stock_name_cfs']
    bizcashinfl = df['sub_total_of_ci_from_oa']
    bizcashoutf = df['sub_total_of_cos_from_oa']
    mananetr = df['ncf_from_oa']

    invcashinfl = df['sub_total_of_ci_from_ia']
    invcashoutf = df['sub_total_of_cos_from_ia']
    invnetcashflow = df['ncf_from_ia']

    fincashinfl = df['sub_total_of_ci_from_fa']
    fincashoutf = df['sub_total_of_cos_from_fa']
    finnetcflow = df['ncf_from_fa']




    # is var
    t = df['report_date']
    # bti = df['biztotinco']
    bi = df['total_revenue']
    inteinco = df['invest_income']
    pouninco = df['exchg_gain']
    otherbizinco = df['other_income']
    # btc = df['biztotcost']
    bc = df['operating_cost']
    pp = df['profit_total_amt']
    biztax = df['operating_taxes_and_surcharge']
    salesexpe = df['sales_fee']
    manaexpe = df['manage_fee']
    finexpe = df['financing_expenses']
    asseimpaloss = df['asset_impairment_loss']
    inveinco = df['invest_income']
    nonoreve = df['non_operating_income']
    nonoexpe = df['non_operating_payout']
    noncassetsdisl = df['noncurrent_assets_dispose_gain']
    incotaxexpe = df['income_tax_expenses']
    netprofit = df['net_profit']


    # bs vars
    t = df['report_date_str_bs']
    a = df['total_assets']
    ca = df['total_current_assets']
    la = df['total_noncurrent_assets']

    b = df['total_liab_and_holders_equity']
    cl = df['total_current_liab']
    ll = df['total_noncurrent_liab']
    l = df['total_liab']
    e = df['total_holders_equity']

    if x=='stock_code':
        ind = np.arange(len(stock_name))  # the x locations for the groups
    else:
        ind = np.arange(len(t))

    # bar1 inco
    # btib = ax.bar(ind, bti, width*8,color='silver')

    # bar 2 inco
    bar2_position=ind-width*4
    is_chart.draw_is_income_bar(ax,bar2_position,width*6,bi,otherbizinco,inveinco,pouninco,inteinco)

    # bar 3 co
    # bar3_position=ind - 3 * width
    # rects3 = ax.bar(bar3_position, btc, width, bottom=pp,color='blue')

    # bar 4 co

    bar4_position=ind -1.5 * width-width*4
    is_chart.draw_is_cost_bar(ax, bar4_position, width * 2, bc, biztax, salesexpe, manaexpe, finexpe, asseimpaloss, pp)

    # bar 6 co
    bar5_position = bar4_position
    is_chart.draw_is_net_profit_bar(ax, bar5_position, width, nonoreve, nonoexpe, noncassetsdisl, incotaxexpe,
                                    netprofit)
    # cfs bars
    bar6_position=ind+1.5*width-width*4
    cfs_chart.draw_cfs_biz_cash_bar(ax, bar6_position, width * 2, bizcashinfl, bizcashoutf, mananetr)

    # bs bars
    bs_position = ind
    bs_chart.draw_bs_bars(ax,bs_position,width,ca,la,cl,ll,e)
    ax.set_xticks(ind )
    font = FontProperties(fname=r"C:\\windows\\fonts\\simsun.ttc",size='xx-large')
    if x=='stock_code':
        ax.set_xticklabels(stock_code+"_"+stock_name, size='xx-large', rotation=90, fontproperties=font)
    else:
        ax.set_xticklabels(t, size='xx-large', rotation=90, fontproperties=font)
    # ax.legend(loc='upper left')



def read_df_by_industry(str_industry):
    dateparse = lambda dates: pd.datetime.strptime(dates, '%Y-%m-%d')
    df_is_cfs_bs = pd.read_excel('../data/is_cfs_bs_' + str_industry + '.xlsx', parse_dates=['report_date_str_bs'],
                                 date_parser=dateparse)
    # df_is_cfs = pd.read_excel('../data/is_cfs_'+str_industry+'.xlsx',converters={'enddate':str})
    # print(df_is_cfs.keys())
    return df_is_cfs_bs


def filter_df_by_enddate(df_is_cfs_bs,str_enddate):
    df_is_cfs_bs = df_is_cfs_bs[df_is_cfs_bs['report_date_str_bs'] == str_enddate]
    df_is_cfs_bs = df_is_cfs_bs.sort_values(by=['total_revenue'],ascending=False)
    return df_is_cfs_bs


def filter_df_by_stock_code(df_is_cfs_bs,str_stock_code):
    df_is_cfs_bs = df_is_cfs_bs[df_is_cfs_bs['stock_code'] == str_stock_code]
    df_is_cfs_bs['is_year_report'] = df_is_cfs_bs['report_date_str_bs'].map(lambda d: d.strftime("%Y-%m-%d").endswith('12-31'))
    df_is_cfs_bs = df_is_cfs_bs[df_is_cfs_bs['is_year_report'] == True]
    df_is_cfs_bs = df_is_cfs_bs.sort_values(by=['report_date_str_bs'], ascending=True)
    return df_is_cfs_bs


def draw_industry_is_cfs_bs_chart_for_stock(str_industry,str_stock_code):
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(20, 8))

    df_is_cfs_bs = read_df_by_industry(str_industry)
    df_is_cfs_bs = filter_df_by_stock_code(df_is_cfs_bs, str_stock_code)
    # plt.title('stock:' + df_is_cfs_bs['stock_name'][0])
    draw_industry_is_cfs_bs_subplot(ax, df_is_cfs_bs, x='report_date_str_bs')
    plt.savefig('../data/charts/is_cfs_bs_' + str_stock_code + '.jpg')
    plt.show()


def draw_industry_is_cfs_bs_chart_for_enddate(str_industry,str_enddate):
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(200, 20))
    plt.title('date:'+str_enddate)
    # plt.ylabel('Damped oscillation')
    # plt.suptitle('This is a somewhat long figure title', fontsize=16)
    df_is_cfs_bs = read_df_by_industry(str_industry)
    df_is_cfs_bs=filter_df_by_enddate(df_is_cfs_bs,str_enddate)
    # print(df_is_cfs)
    draw_industry_is_cfs_bs_subplot(ax, df_is_cfs_bs, x='stock_code')
    plt.savefig('../data/charts/is_cfs_bs_'+str_industry+"_"+str_enddate+'.jpg')
    plt.show()




