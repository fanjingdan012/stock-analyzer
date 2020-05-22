import pandas as pd
import datetime
import time
def adapt(name,report_type):
    adapted = pd.read_excel('../data/'+report_type+'_'+name+'.xlsx')
    report_dates=[]
    df_items = []
    for i,v in adapted['report_date'].items():
        timeTemp = float(v / 1000)
        tupTime = time.localtime(timeTemp)
        report_date_str = time.strftime('%Y-%m-%d',tupTime)
        report_dates.append(report_date_str)
    adapted['report_date_str'] = report_dates
    adapted2 = adapted.applymap(lambda x: x.split(',', 1)[0][1:] if (isinstance(x, str) and x.startswith('[')) else x)
    adapted3 = adapted2.applymap(lambda x: 0 if (x == 'None') else x)
    adapted3.to_excel('../data/'+report_type+'1_' + name + '.xlsx')
    return adapted3

# name is stock_code or industry(chinese)
def merge_industry_is_cfs(name):
    df_cfs_all = pd.read_excel('../data/cfs_'+name+'.xlsx')
    df_is_all = pd.read_excel('../data/is_'+name+'.xlsx')
    df_merged = pd.merge(df_cfs_all, df_is_all, left_on=['stock_code','report_date'], right_on = ['stock_code','report_date'],copy=True, indicator='both',suffixes=('_cfs','_is'))
    # df_merged.fillna(0, inplace=True)
    df_merged.to_excel('../data/is_cfs_'+name+'.xlsx')
    return df_merged


def merge_industry_is_cfs_bs_match_enddate_bsdate(name):
    df_is_cfs_all = pd.read_excel('../data/is_cfs1_'+name+'.xlsx')
    df_bs_all = pd.read_excel('../data/bs1_'+name+'.xlsx')
    df_is_cfs_all.fillna(0, inplace=True)
    df_bs_all.fillna(0, inplace=True)
    df_merged = pd.merge(df_is_cfs_all, df_bs_all, left_on=['stock_code','report_date'], right_on = ['stock_code','report_date'],copy=True, indicator='exists',suffixes=('_is_cfs','_bs'))
    # df_merged.fillna(0, inplace=True)
    df_merged.to_excel('../data/is_cfs_bs_'+name+'.xlsx')
    return df_merged


def merge_industry_is_cfs_bs_match_begindate_bsdate(name):
    df_is_cfs_all = pd.read_excel('../data/is_cfs1_'+name+'.xlsx', converters={'report_date_str': str,'begindate_is':str})
    df_is_cfs_all['is_year_report'] = df_is_cfs_all['report_date_str'].map(lambda d: d.endswith('12-31'))
    df_is_cfs_all['begindate_minus1d'] = df_is_cfs_all['begindate_is'].map(lambda d: (pd.datetime.strptime(d, '%Y-%m-%d')-datetime.timedelta(days=1)).strftime("%Y-%m-%d"))

    df_cfs_all_yearly = df_is_cfs_all[df_is_cfs_all['is_year_report'] == True]
    df_cfs_all_yearly.fillna(0, inplace=True)
    df_cfs_all_yearly.to_excel('../data/is_cfs_yearly_' + name + '.xlsx')


    # df_is_cfs_bs = pd.read_excel('../data/is_cfs_bs_' + str_industry + '.xlsx', parse_dates=['enddate'],
    #                              date_parser=dateparse)
    df_bs_all = pd.read_excel('../data/bs1_' + name + '.xlsx', converters={'report_date_str': str})
    df_bs_all['is_year_report'] = df_bs_all['report_date_str'].map(lambda d: d.endswith('1231'))
    df_bs_all_yearly = df_bs_all[df_bs_all['is_year_report'] == True]
    df_bs_all_yearly.fillna(0, inplace=True)
    df_bs_all_yearly.to_excel('../data/bs_yearly_' + name + '.xlsx')

    now = datetime.datetime.now()
    date = now + datetime.timedelta(days=1)

    df_merged = pd.merge(df_cfs_all_yearly, df_bs_all_yearly, left_on=['stock_code','begindate_minus1d'], right_on = ['stock_code','report_date_str'],how='outer',copy=True, indicator='exists',suffixes=('_is_cfs','_bs'))
    # df_merged.fillna(0, inplace=True)
    df_merged.to_excel('../data/is_cfs_bs_begin_'+name+'.xlsx')
    return df_merged

def calc_profit_ability(name):
    df_is_cfs_bs_begin = pd.read_excel('../data/is_cfs_bs_begin_' + name + '.xlsx', converters={'report_date_str': str})
    df_is_cfs_bs_begin['roe'] = df_is_cfs_bs_begin['netprofit_is']/df_is_cfs_bs_begin['total_holders_equity']
    df_is_cfs_bs_begin['roa'] = df_is_cfs_bs_begin['netprofit_is']/df_is_cfs_bs_begin['total_assets']
    df_is_cfs_bs_begin['ni_div_sr'] = df_is_cfs_bs_begin['netprofit_is']/df_is_cfs_bs_begin['total_revenue']
    df_is_cfs_bs_begin['sr_div_a'] = df_is_cfs_bs_begin['total_revenue']/df_is_cfs_bs_begin['total_assets']
    df_is_cfs_bs_begin.to_excel('../data/is_cfs_bs_begin_'+name+'.xlsx')


def merge_is_cfs(name):
    df_cfs = pd.read_excel('../data/is_cfs_' + name + '.xlsx')
    df_is = pd.read_excel('../data/bs_' + name + '.xlsx')
    df_cfs.fillna(0, inplace=True)
    df_is.fillna(0, inplace=True)
    df_merged = pd.merge(df_cfs, df_is, on='enddate',copy=True, indicator='both',suffixes=('_cfs','_is'))
    df_merged.to_excel('../data/is_cfs_bs_' + name + '.xlsx')
    return df_merged