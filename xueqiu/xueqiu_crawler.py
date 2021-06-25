import xueqiu.xueqiu_balance_sheet as xueqiu_balance_sheet
import xueqiu.xueqiu_cash_flow_statement as xueqiu_cash_flow_statement
import xueqiu.xueqiu_income_statement as xueqiu_income_statement
import stock_reader


def get_reports_for_1_stock(stock_code, country='cn'):
    xueqiu_balance_sheet.get_bs_for_1_stock(stock_code, country)
    xueqiu_cash_flow_statement.get_cfs_for_1_stock_new(stock_code, country)
    xueqiu_income_statement.get_is_for_1_stock_new(stock_code, country)
    print("finished craw: %s" % (stock_code))


if __name__=="__main__":
    stock_codes=[
         'SH603995', 'SH688186'
    # 银行
    # 非银金融
    # 综合
    ]
    for stock_code in stock_codes:
    # for stock_code in df['stock_code']:
        get_reports_for_1_stock(stock_code)
