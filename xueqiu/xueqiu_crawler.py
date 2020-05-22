import xueqiu.xueqiu_balance_sheet as xueqiu_balance_sheet
import xueqiu.xueqiu_cash_flow_statement as xueqiu_cash_flow_statement
import xueqiu.xueqiu_income_statement as xueqiu_income_statement
import stock_reader


def get_reports_for_1_stock(stock_code):
    xueqiu_balance_sheet.get_bs_for_1_stock(stock_code)
    xueqiu_cash_flow_statement.get_cfs_for_1_stock_new(stock_code)
    xueqiu_income_statement.get_is_for_1_stock_new(stock_code)
    print("finished craw: %s" % (stock_code))


if __name__=="__main__":
    stock_codes=[
        'SH600531',
'SH600547',
'SH600549',
'SH600595',
'SH600614',
'SH600615',
'SH600687',
'SH600711',
'SH600766',
'SH600768',
'SH600888',
'SH600961',
'SH600980',
'SH600988',
'SH601020',
'SH601069',
'SH601137',
'SH601168',
'SH601212',
'SH601388',
'SH601600',
'SH601609',
'SH601677',
'SH601899',
'SH601958',
'SH603003',
'SH603045',
'SH603115',
'SH603260',
'SH603399',
'SH603527',
'SH603612',
'SH603663',
'SH603688',
'SH603799',
'SH603826',
'SH603876',
'SH603978',
'SH603993',
'SH688122',
'SH688300',
'SH688357',
'SH688388',
'SH688598'
    # 银行
    # 非银金融
    # 综合
    ]
    for stock_code in stock_codes:
    # for stock_code in df['stock_code']:
        get_reports_for_1_stock(stock_code)
