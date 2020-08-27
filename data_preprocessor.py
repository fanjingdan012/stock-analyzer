import pandas as pd
import datetime
import time
from sqlalchemy import create_engine
import numpy as np

def adapt(name,report_type,isIndustry=True):
    if isIndustry:
        adapted = pd.read_excel('../data/' + report_type + '_' + name + '.xlsx')
    else:
        adapted = pd.read_excel('../data/'+report_type+'/'+report_type+'_'+name+'.xlsx')
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
    engine = create_engine('mysql+pymysql://root:123456@localhost:3306/stock')
    # adapted4 = adapted3.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis=1)
    # adapted4.to_sql(report_type+'_fin', engine, if_exists='append', index=False)
    # return adapted4

# name is stock_code or industry(chinese)
def merge_is_cfs(name,isIndustry=True):
    df_cfs_all = pd.read_excel('../data/cfs1_'+name+'.xlsx')
    df_is_all = pd.read_excel('../data/is1_'+name+'.xlsx')
    if isIndustry:
        df_merged = pd.merge(df_cfs_all, df_is_all, left_on=['stock_code','report_date'], right_on = ['stock_code','report_date'],copy=True, indicator='both',suffixes=('_cfs','_is'))
    else:
        df_merged = pd.merge(df_cfs_all, df_is_all, left_on=['report_date'], right_on = ['report_date'],copy=True, indicator='both',suffixes=('_cfs','_is'))

    # df_merged.fillna(0, inplace=True)
    df_merged.to_excel('../data/is_cfs_'+name+'.xlsx')
    return df_merged


def merge_is_cfs_bs_match_enddate_bsdate(name,isIndustry=True):
    df_is_cfs_all = pd.read_excel('../data/is_cfs_'+name+'.xlsx')
    df_bs_all = pd.read_excel('../data/bs1_'+name+'.xlsx')
    df_is_cfs_all.fillna(0, inplace=True)
    df_bs_all.fillna(0, inplace=True)
    if isIndustry:
        df_merged = pd.merge(df_is_cfs_all, df_bs_all, left_on=['stock_code','report_date'], right_on = ['stock_code','report_date'],copy=True, indicator='exists',suffixes=('_is_cfs','_bs'))
    else:
        df_merged = pd.merge(df_is_cfs_all, df_bs_all, left_on=[ 'report_date'],
                             right_on=[ 'report_date'], copy=True, indicator='exists',
                             suffixes=('_is_cfs', '_bs'))

    # df_merged.fillna(0, inplace=True)
    df_merged.to_excel('../data/is_cfs_bs_'+name+'.xlsx')
    return df_merged


def merge_is_cfs_bs_match_begindate_bsdate(name):
    df_is_cfs_all = pd.read_excel('../data/is_cfs_'+name+'.xlsx', converters={'report_date_str': str})
    df_is_cfs_all['is_year_report'] = df_is_cfs_all['report_date_str_is'].map(lambda d: d.endswith('12-31'))
    df_is_cfs_all['begin_date'] = df_is_cfs_all['report_date_str_is'].map(lambda d: d[:5]+'01-01')
    df_is_cfs_all['begin_date_minus1d'] = df_is_cfs_all['begin_date'].map(lambda d: (pd.datetime.strptime(d, '%Y-%m-%d')-datetime.timedelta(days=1)).strftime("%Y-%m-%d"))

    df_cfs_all_yearly = df_is_cfs_all[df_is_cfs_all['is_year_report'] == True]
    df_cfs_all_yearly.fillna(0, inplace=True)
    df_cfs_all_yearly.to_excel('../data/is_cfs_yearly_' + name + '.xlsx')


    # df_is_cfs_bs = pd.read_excel('../data/is_cfs_bs_' + str_industry + '.xlsx', parse_dates=['enddate'],
    #                              date_parser=dateparse)
    df_bs_all = pd.read_excel('../data/bs1_' + name + '.xlsx', converters={'report_date_str': str})
    df_bs_all['is_year_report'] = df_bs_all['report_date_str'].map(lambda d: d.endswith('12-31'))
    df_bs_all_yearly = df_bs_all[df_bs_all['is_year_report'] == True]
    df_bs_all_yearly.fillna(0, inplace=True)
    df_bs_all_yearly.to_excel('../data/bs_yearly_' + name + '.xlsx')

    now = datetime.datetime.now()
    date = now + datetime.timedelta(days=1)

    df_merged = pd.merge(df_cfs_all_yearly, df_bs_all_yearly, left_on=['stock_code','begin_date_minus1d'], right_on = ['stock_code','report_date_str'],how='outer',copy=True, indicator='exists',suffixes=('_is_cfs','_bs'))
    # df_merged.fillna(0, inplace=True)
    df_merged.to_excel('../data/is_cfs_bs_begin_'+name+'.xlsx')
    return df_merged

def calc_profit_ability(name):
    df_is_cfs_bs_begin = pd.read_excel('../data/is_cfs_bs_begin_' + name + '.xlsx', converters={'report_date_str': str})
    df_is_cfs_bs_begin['roe'] = df_is_cfs_bs_begin['net_profit']/df_is_cfs_bs_begin['total_holders_equity']
    df_is_cfs_bs_begin['roa'] = df_is_cfs_bs_begin['net_profit']/df_is_cfs_bs_begin['total_assets']
    df_is_cfs_bs_begin['ni_div_sr'] = df_is_cfs_bs_begin['net_profit']/df_is_cfs_bs_begin['total_revenue']
    df_is_cfs_bs_begin['sr_div_a'] = df_is_cfs_bs_begin['total_revenue']/df_is_cfs_bs_begin['total_assets']
    df_is_cfs_bs_begin.to_excel('../data/is_cfs_bs_begin_'+name+'.xlsx')

def calc_op_asset(name,isIndustry=True):
    df_bs = pd.read_excel('../data/bs1_' + name + '.xlsx', converters={'report_date_str': str})
    df_bs['oca'] = \
                   +df_bs['general_risk_provision']\
                   +df_bs['account_receivable']\
                  +df_bs['bills_receivable']\
                   +df_bs['pre_payment']\
                   +df_bs['othr_receivables']\
                   +df_bs['inventory']\
                  +df_bs['nca_due_within_one_year']\
                   +df_bs['othr_current_assets']\
                   +df_bs['lt_receivable']\
                   +df_bs['dev_expenditure']\
                  +df_bs['lt_deferred_expense'] \
                   + df_bs['othr_noncurrent_assets'] \
                   + df_bs['contractual_assets'] \
                   + df_bs['fixed_asset_sum']\
                  +df_bs['construction_in_process_sum'] \
                   + df_bs['project_goods_and_material'] \
                   + df_bs['productive_biological_assets']\
                  + df_bs['oil_and_gas_asset']\
                   +df_bs['intangible_assets']\
                   + df_bs['goodwill']
    df_bs['ola'] = df_bs['dt_assets'] \
            +df_bs['lt_equity_invest']\

    df_bs.to_excel('../data/bs1_'+name+'.xlsx')

def calc_op_liab(name,isIndustry=True):
    df_bs = pd.read_excel('../data/bs1_' + name + '.xlsx', converters={'report_date_str': str})
    df_bs['ocl'] = df_bs['payroll_payable'] + df_bs['tax_payable'] + df_bs['estimated_liab'] + df_bs[
        'dt_liab'] + df_bs['accounts_payable'] + df_bs['bill_payable'] + df_bs['pre_receivable'] + df_bs['special_payable'] \
    + df_bs['othr_current_liab'] + df_bs['contract_liabilities']
    df_bs['oll'] = df_bs['payroll_payable'] + df_bs['tax_payable'] + df_bs['estimated_liab'] + df_bs[
        'dt_liab'] + df_bs['accounts_payable'] + df_bs['bill_payable'] + df_bs['pre_receivable'] + df_bs[
                      'special_payable'] \
                  + df_bs['othr_current_liab'] + df_bs['contract_liabilities']
    df_bs.to_excel('../data/bs1_' + name + '.xlsx')

def calc_fin_asset(name,isIndustry=True):
    df_bs = pd.read_excel('../data/bs1_' + name + '.xlsx', converters={'report_date_str': str})
    df_bs['fca'] = df_bs['tradable_fnncl_assets'] + df_bs['interest_receivable'] + df_bs['saleable_finacial_assets'] + df_bs[
        'held_to_maturity_invest'] \
                  + df_bs['invest_property'] + df_bs['current_assets_si'] + df_bs['noncurrent_assets_si'] + df_bs['dividend_receivable'] \
                  + df_bs['othr_payables'] + df_bs['salable_financial_assets'] + df_bs['to_sale_asset'] + df_bs[
                      'other_eq_ins_invest'] \
                  + df_bs['other_illiquid_fnncl_assets'] + df_bs['currency_funds']
    df_bs['fla'] = df_bs['tradable_fnncl_assets'] + df_bs['interest_receivable'] + df_bs['saleable_finacial_assets'] + df_bs[
        'held_to_maturity_invest'] \
                  + df_bs['invest_property'] + df_bs['current_assets_si'] + df_bs['noncurrent_assets_si'] + df_bs['dividend_receivable'] \
                  + df_bs['othr_payables'] + df_bs['salable_financial_assets'] + df_bs['to_sale_asset'] + df_bs[
                      'other_eq_ins_invest'] \
                  + df_bs['other_illiquid_fnncl_assets'] + df_bs['currency_funds']
    df_bs.to_excel('../data/bs1_' + name + '.xlsx')

def calc_fin_liab(name,isIndustry=True):
    df_bs = pd.read_excel('../data/bs1_' + name + '.xlsx', converters={'report_date_str': str})
    df_bs['fcl'] = df_bs['st_loan']+df_bs['tradable_fnncl_liab']+ df_bs['derivative_fnncl_liab'] +  df_bs['bond_payable'] +df_bs[
        'interest_payable'] \
                   + df_bs['current_liab_si'] + df_bs['noncurrent_liab_si'] + df_bs['dividend_payable'] \
                  + df_bs['noncurrent_liab_due_in1y'] + df_bs['lt_loan'] + df_bs['lt_payable'] + df_bs[
                      'othr_non_current_liab'] \
                  + df_bs['to_sale_debt'] + df_bs['lt_payable_sum'] + df_bs['noncurrent_liaGAb_di']
    df_bs['fll'] = df_bs['tradable_fnncl_liab'] + df_bs['bond_payable'] + df_bs['derivative_fnncl_liab'] + df_bs[
        'interest_payable'] \
                  + df_bs['st_loan'] + df_bs['current_liab_si'] + df_bs['noncurrent_liab_si'] + df_bs[
                      'dividend_payable'] \
                  + df_bs['noncurrent_liab_due_in1y'] + df_bs['lt_loan'] + df_bs['lt_payable'] + df_bs[
                      'othr_non_current_liab'] \
                  + df_bs['to_sale_debt'] + df_bs['lt_payable_sum'] + df_bs['noncurrent_liaGAb_di']
    df_bs.to_excel('../data/bs1_' + name + '.xlsx')
def calc_fin_liab(name,isIndustry=True):
    df_bs = pd.read_excel('../data/bs1_' + name + '.xlsx', converters={'report_date_str': str})
    df_bs['fl'] = df_bs['tradable_fnncl_liab'] + df_bs['bond_payable'] + df_bs['derivative_fnncl_liab'] + df_bs[
        'interest_payable'] \
                  + df_bs['st_loan'] + df_bs['current_liab_si'] + df_bs['noncurrent_liab_si'] + df_bs['dividend_payable'] \
                  + df_bs['noncurrent_liab_due_in1y'] + df_bs['lt_loan'] + df_bs['lt_payable'] + df_bs[
                      'othr_non_current_liab'] \
                  + df_bs['to_sale_debt'] + df_bs['lt_payable_sum'] + df_bs['noncurrent_liab_di']
    df_bs.to_excel('../data/bs1_' + name + '.xlsx')
# def merge_is_cfs(name):
#     df_cfs = pd.read_excel('../data/is_cfs_' + name + '.xlsx')
#     df_is = pd.read_excel('../data/bs_' + name + '.xlsx')
#     df_cfs.fillna(0, inplace=True)
#     df_is.fillna(0, inplace=True)
#     df_merged = pd.merge(df_cfs, df_is, on='enddate',copy=True, indicator='both',suffixes=('_cfs','_is'))
#     df_merged.to_excel('../data/is_cfs_bs_' + name + '.xlsx')
#     return df_merged
