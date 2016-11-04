import pandas

def ConstructURL(company, start, end):
    prefix = 'http://chart.finance.yahoo.com/table.csv?'
    suffix = 'ignore=.csv'

    s = 's=' + company + '&'
    a = 'a=' + str(int(start.format('M')) - 1) + '&'
    b = 'b=' + start.format('D') + '&'
    c = 'c=' + start.format('YYYY') + '&'
    d = 'd=' + str(int(end.format('M')) - 1) + '&'
    e = 'e=' + end.format('D') + '&'
    f = 'f=' + end.format('YYYY') + '&'
    g = 'g=d' + '&'

    return prefix + s + a + b + c + d + e + f + g + suffix

def getStockData(data):
    for d in data.values():
        url = ConstructURL(d['ticker'], d['begin'], d['end'])
        d['stocks'] = pandas.read_csv(url)
    return data
