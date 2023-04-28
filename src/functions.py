import pandas as pd
import requests

def cleanDF(df):
    all_cols = ['ID', 'Language', 'Subscription Type', 'Subscription Event Type',
                'Purchase Store', 'Purchase Amount', 'Currency',
                'Subscription Start Date', 'Subscription Expiration', 'Demo User',
                'Free Trial User', 'Free Trial Start Date', 'Free Trial Expiration',
                'Auto Renew', 'Country', 'User Type', 'Lead Platform',
                'Email Subscriber', 'Push Notifications', 'Send Count', 'Open Count',
                'Click Count', 'Unique Open Count', 'Unique Click Count',
                'App Session Platform', 'App Activity Type', 'App Session Date']

    category_cols = ['Language', 'Subscription Type', 'Subscription Event Type', 'Purchase Store',
                    'Currency', 'Country', 'User Type', 'Lead Platform',
                    'App Session Platform', 'App Activity Type']

    int_cols = ['ID', 'Send Count', 'Open Count', 'Click Count', 'Unique Open Count', 'Unique Click Count']

    date_cols = ['Subscription Start Date', 'Subscription Expiration',
                'App Session Date', 'Free Trial Start Date', 'Free Trial Expiration']

    bool_cols = ['Demo User', 'Free Trial User', 'Auto Renew',
                'Email Subscriber', 'Push Notifications']

    # Keep only columns that exist in df
    all_cols = [col for col in all_cols if col in df.columns]
    category_cols = [col for col in category_cols if col in df.columns]
    int_cols = [col for col in int_cols if col in df.columns]
    date_cols = [col for col in date_cols if col in df.columns]
    bool_cols = [col for col in bool_cols if col in df.columns]

    # if 'Auto Renew' is in df.columns
    if 'Auto Renew' in df.columns:
        # convert to True/False
        df['Auto Renew'] = df['Auto Renew'].replace({'On': True, 'Off': False})

    # convert na to 0 in int_cols
    df[int_cols] = df[int_cols].fillna(0)

    df[category_cols] = df[category_cols].astype('category')
    df[int_cols] = df[int_cols].astype('int64')
    df[date_cols] = df[date_cols].astype('datetime64[ns]')
    df[bool_cols] = df[bool_cols].astype('bool')

    return df

def transform_value(value):
    if pd.isnull(value):
        return value
    value_str = str(int(value))
    if value_str.endswith('0000'):
        value_int = int(value / 10000)
        return float(value_int / 100)
    else:
        return value

#fetch exchange rates
def fetch_exchange_rates(api_key, currencies):
    currency_list = ','.join(currencies)
    url = f'https://openexchangerates.org/api/latest.json?app_id={api_key}&symbols={currency_list}'
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()['rates']
    else:
        raise ValueError(f"Failed to fetch exchange rates. Status code: {response.status_code}")

#convert to USD
def convert_to_usd(amount, currency, exchange_rates):
    if currency in exchange_rates:
        return amount / exchange_rates[currency]
    else:
        return amount

def convert_currencies_to_usd(data_frame, amount_column, currency_column, exchange_rates):
    data_frame[amount_column] = data_frame.apply(lambda row: convert_to_usd(row[amount_column], row[currency_column], exchange_rates), axis=1)
    return data_frame
