import requests
from prettytable import PrettyTable
from colorama import Fore, Back, Style

convert = 'INR'

listings_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?convert=' + convert

request = requests.get(url=listings_url, headers={'X-CMC_PRO_API_KEY': 'Your_API_Key'})
result = request.json()
data = result['data']

# global_cap = data['quote'][convert]['market_cap']
# global_cap_string = '{:,}'.format(global_cap)

while True:
    print()
    print('CoinMarketCap Explorer Menu')
    # print('The global market cap is ₹' + global_cap_string)
    print()
    print('1 - Top 100 sorted by name')
    print('2 - Top 100 sorted by 24 hour change')
    print('3 - Top 100 sorted by 24 hour volume')
    print('0 - Exit')
    print()
    choice = input('What is you choice? (1 - 3): ')

    ticker_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?convert=' + convert + '&sort='

    if choice == '1':
        ticker_url += 'name'
    if choice == '2':
        ticker_url += 'percent_change_24h'
    if choice == '3':
        ticker_url += 'volume_24h'
    if choice == '0':
        break

    request = requests.get(url=ticker_url, headers={'X-CMC_PRO_API_KEY': 'Your_API_Key'})
    results = request.json()
    data = results['data']

    table = PrettyTable(['Rank', 'Asset', 'Price', 'Market Cap', 'Volume', '1hour Change', '24hour Change', '7day Change'])

    print()
    for currency in data:
        rank = currency['cmc_rank']
        name = currency['name']
        last_updated = currency['last_updated']
        symbol = currency['symbol']
        quotes = currency['quote'][convert]
        market_cap = quotes['market_cap']
        hour_change = quotes['percent_change_1h']
        day_change = quotes['percent_change_24h']
        week_change = quotes['percent_change_7d']
        price = quotes['price']
        volume = quotes['volume_24h']

        if hour_change is not None:
            if hour_change > 0:
                hour_change = Back.GREEN + Fore.BLACK + str(hour_change) + '%' + Style.RESET_ALL
            else:
                hour_change = Back.RED + Fore.BLACK + str(hour_change) + '%' + Style.RESET_ALL
        if day_change is not None:
            if day_change > 0:
                day_change = Back.GREEN + Fore.BLACK + str(day_change) + '%' + Style.RESET_ALL
            else:
                day_change = Back.RED + Fore.BLACK + str(day_change) + '%' + Style.RESET_ALL
        if week_change is not None:
            if week_change > 0:
                week_change = Back.GREEN + Fore.BLACK + str(week_change) + '%' + Style.RESET_ALL
            else:
                week_change = Back.RED + Fore.BLACK + str(week_change) + '%' + Style.RESET_ALL

        volume_string = '{:,}'.format(volume)
        market_cap_string = '{:,}'.format(market_cap)
        price_string = '{:,}'.format(price)

        table.add_row([
            rank,
            name + ' (' + symbol + ')',
            '₹' + price_string,
            '₹' + market_cap_string,
            '₹' + volume_string,
            str(hour_change),
            str(day_change),
            str(week_change)
        ])

    print()
    print(table)
    print()

    choice = input('Again? (y/n): ')

    if choice == 'n':
        break
