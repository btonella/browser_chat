import requests
import csv


def find_stock(key):
    url = f'https://stooq.com/q/l/?s={key}&f=sd2t2ohlcv&h&e=csv'
    try:
        resp = requests.get(url)
        if (resp.status_code == 200):
            reader = csv.reader(resp.text.split('\n'), delimiter=',')
            for row in reader:
                if (len(row) > 0):
                    value = row[-2]
            if (value == 'N/D'):
                return f'{key} quote per share not found'
            return f'{key} quote is ${value} per share'
        else:
            print('resp error: '+resp.text)
            return False
    except Exception as e:
        print('error: '+str(e))
        return False
