def get_nominal_delta_min_max(stocks):
    sorted_nominal = sorted(stocks, key=lambda x: x['delta'])
    return sorted_nominal[:5], list(reversed(sorted_nominal[-5:]))

def get_percent_delta_min_max(stocks):
    sorted_pct = sorted(stocks, key=lambda x: x['delta_pct'])
    return sorted_pct[:5], list(reversed(sorted_pct[-5:]))

def calculate_deltas(stocks):
    for stock in stocks:
        stock['delta'] = stock['c'] - stock['o']
        stock['delta_pct'] = stock['delta'] / stock['o']
    return stocks