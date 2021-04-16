import pandas as pd
from yahoo_fin import stock_info as si
from tabulate import tabulate
import datetime


# Index America & Oceania
def america_oceania():
    indices = set(['^DJI', '^IXIC', '^RUT','^GSPC','^BVSP','^AXJO','^NZ50', '^GSPTSE', '^MXX'])
    value = {}
    for ticker in indices:
        data = si.get_quote_data(ticker)
        value[data['symbol']] = round(data['regularMarketChangePercent'], 2)

    new_key = {'^DJI':str('DOW 30'+u'\U0001F1FA\U0001F1F8'), '^IXIC':str('NASDAQ'+u'\U0001F1FA\U0001F1F8'), '^RUT':str('RUSSELL2000'+u'\U0001F1FA\U0001F1F8'), '^GSPC':str('S&P500'+u'\U0001F1FA\U0001F1F8'),'^BVSP':str('IBOV'+u'\U0001F1E7\U0001F1F7'), '^AXJO': str('ASX'+u'\U0001F1E6\U0001F1FA'), '^NZ50':str('NZ50'+u'\U0001F1F3\U0001F1FF'), '^GSPTSE':str('TSX'+u'\U0001F1E8\U0001F1E6'), '^MXX':str('IPC'+u'\U0001F1F2\U0001F1FD')}
    value = dict((new_key[key], value) for (key, value) in value.items())
    value = pd.DataFrame.from_dict(value, orient='index', columns=['% Change'])
    return value

# Index Europe
def europe():
    indices = set(['^FTSE', '^GDAXI', '^FCHI', 'FTSEMIB.MI','^IBEX', '^AEX','IMOEX.ME','^SSMI'])
    value = {}
    for ticker in indices:
        data = si.get_quote_data(ticker)
        value[data['symbol']] = round(data['regularMarketChangePercent'], 2)
    new_key = {'^FTSE':str('FTSE'+u'\U0001F1EC\U0001F1E7'),'^GDAXI':str('DAX'+u'\U0001F1E9\U0001F1EA'), '^FCHI' : str('CAC40'+u'\U0001F1EB\U0001F1F7'), 'FTSEMIB.MI' : str('FTSEMIB'+u'\U0001F1EE\U0001F1F9'), '^IBEX' : str('IBEX'+u'\U0001F1EA\U0001F1F8'), '^AEX' : str('AEX'+u'\U0001F1F3\U0001F1F1'),'IMOEX.ME':str('IMOEX'+u'\U0001F1F7\U0001F1FA'), '^SSMI':str('SMI'+u'\U0001F1E8\U0001F1ED')}
    value = dict((new_key[key], value) for (key, value) in value.items())
    value = pd.DataFrame.from_dict(value, orient='index', columns=['% Change'])
    return value

# Index Asia & Africa
def asia_africa():
    indices = set(['000001.SS','^BSESN','^NSEI', '^N225', '^HSI','^KS11','^SET.BK','WIZAF.L'])
    value = {}
    for ticker in indices:
        data = si.get_quote_data(ticker)
        value[data['symbol']] = round(data['regularMarketChangePercent'], 2)
    new_key = { '000001.SS' : str('SSE'+u'\U0001F1E8\U0001F1F3'), '^BSESN':str('BSE'+u'\U0001F1EE\U0001F1F3'),'^NSEI':str('NIFTY50'+u'\U0001F1EE\U0001F1F3'),'^N225':str('NIKKEI'+u'\U0001F1EF\U0001F1F5'), '^HSI':str('HS'+u'\U0001F1ED\U0001F1F0'),'^KS11':str('KOSPI'+u'\U0001F1F0\U0001F1F7'),'^SET.BK':str('SET'+u'\U0001F1F9\U0001F1ED'),'WIZAF.L':str('SA'+u'\U0001F1FF\U0001F1E6')}
    value = dict((new_key[key], value) for (key, value) in value.items())
    value = pd.DataFrame.from_dict(value, orient='index', columns=['% Change'])
    return value

# Picks larger daily gainers
def gainers():
    gain = si.get_day_gainers().iloc[0:10,[1,4]]
    gain['Name'] = gain['Name'].str.replace('Inc',"")
    gain['Name'] = gain['Name'].str.replace('Public',"")
    gain['Name'] = gain['Name'].str.replace('Company',"")
    gain['Name'] = gain['Name'].str.replace('Holdings',"")
    gain['Name'] = gain['Name'].str.replace('Limited',"")
    gain['Name'] = gain['Name'].str.replace('Group',"")
    gain['Name'] = gain['Name'].str[:17]
    gain = tabulate(gain, tablefmt='psql', showindex=False,numalign="center",colalign=("left",))
    return gain

# Picks most traded stocks
def most_active():
    gain = si.get_day_most_active().iloc[0:10,[1,4]]
    gain['Name'] = gain['Name'].str.replace('Inc',"")
    gain['Name'] = gain['Name'].str.replace('Public',"")
    gain['Name'] = gain['Name'].str.replace('Company',"")
    gain['Name'] = gain['Name'].str.replace('Holdings',"")
    gain['Name'] = gain['Name'].str.replace('Limited',"")
    gain['Name'] = gain['Name'].str.replace('Group',"")
    gain['Name'] = gain['Name'].str[:17]
    gain = tabulate(gain, tablefmt='psql', showindex=False,numalign="center",colalign=("left",))
    return gain

# Picks larger daily losers
def loosers():
    gain = si.get_day_losers().iloc[0:10,[1,4]]
    gain['Name'] = gain['Name'].str.replace('Inc',"")
    gain['Name'] = gain['Name'].str.replace('Public',"")
    gain['Name'] = gain['Name'].str.replace('Company',"")
    gain['Name'] = gain['Name'].str.replace('Holdings',"")
    gain['Name'] = gain['Name'].str.replace('Limited',"")
    gain['Name'] = gain['Name'].str.replace('Group',"")
    gain['Name'] = gain['Name'].str[:17]
    gain = tabulate(gain, tablefmt='psql', showindex=False,numalign="center",colalign=("left",))
    return gain

def earnings_today():
    value = pd.DataFrame.from_dict(si.get_earnings_for_date(str(datetime.datetime.today().date())))
    value = value[['companyshortname','epsestimate']]
    value['companyshortname'] = value['companyshortname'].str[:17]
    value = tabulate(value, tablefmt='psql', showindex=False,numalign="center",colalign=("left",))
    return value