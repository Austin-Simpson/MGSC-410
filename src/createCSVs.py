import pandas as pd
from functions import *

#CREATE MERGED DF
# clean subscriberDF 
subscriberDF = pd.read_csv('../data/Original_Subscriber_Information.csv')
subscriberDF['Purchase Amount'] = subscriberDF['Purchase Amount'].apply(transform_value)

currencies = [
    'AED', 'AUD', 'BGN', 'BRL', 'CAD', 'CHF', 'CLP', 'COP', 'CRC', 'CZK',
    'DKK', 'EGP', 'EUR', 'GBP', 'GHS', 'HKD', 'HUF', 'IDR', 'ILS', 'INR',
    'JPY', 'KRW', 'KZT', 'LBP', 'MXN', 'MYR', 'NOK', 'NZD', 'PEN', 'PHP',
    'PLN', 'QAR', 'RON', 'RSD', 'RUB', 'SAR', 'SEK', 'SGD', 'THB', 'TRY',
    'UAH', 'VND', 'ZAR'
]

api_key = '418dd91a76a743c7bee44a1feb77fe51'
exchange_rates = fetch_exchange_rates(api_key, currencies)

subscriberDF = convert_currencies_to_usd(subscriberDF, 'Purchase Amount', 'Currency', exchange_rates)


# clean appDF
appDF = pd.read_csv('../data/Original_App_activity.csv')
appDF.dropna()
appDF = appDF.dropna(subset=['App Activity Type', 'App Session Platform', 'App Session Date'])
appDF.to_csv('../data/app_nonull.csv', index=False)

# Use currencies to determine the country of the subscriber
currency_to_country = {
    'AED': 'United Arab Emirates',
    'AUD': 'Australia',
    'BGN': 'Bulgaria',
    'BRL': 'Brazil',
    'CAD': 'Canada',
    'CHF': 'Switzerland',
    'CLP': 'Chile',
    'COP': 'Colombia',
    'CRC': 'Costa Rica',
    'CZK': 'Czech Republic',
    'DKK': 'Denmark',
    'EGP': 'Egypt',
    'EUR': 'European Union',
    'GBP': 'United Kingdom',
    'GHS': 'Ghana',
    'HKD': 'Hong Kong',
    'HUF': 'Hungary',
    'IDR': 'Indonesia',
    'ILS': 'Israel',
    'INR': 'India',
    'JPY': 'Japan',
    'KRW': 'South Korea',
    'KZT': 'Kazakhstan',
    'LBP': 'Lebanon',
    'MXN': 'Mexico',
    'MYR': 'Malaysia',
    'NOK': 'Norway',
    'NZD': 'New Zealand',
    'PEN': 'Peru',
    'PHP': 'Philippines',
    'PLN': 'Poland',
    'QAR': 'Qatar',
    'RON': 'Romania',
    'RSD': 'Serbia',
    'RUB': 'Russia',
    'SAR': 'Saudi Arabia',
    'SEK': 'Sweden',
    'SGD': 'Singapore',
    'THB': 'Thailand',
    'TRY': 'Turkey',
    'UAH': 'Ukraine',
    'USD': 'United States',
    'VND': 'Vietnam',
    'ZAR': 'South Africa'
}

#skip rows with na or nan in currency
subscriberDF['Country'] = subscriberDF['Currency'].apply(lambda currency: currency_to_country[currency] if currency in currency_to_country else None)
subscriberDF.to_csv('../data/subscriberClean.csv', index=False)

merged_df = subscriberDF.merge(appDF, on='ID', how='left')

# merged_df.to_csv("../data/mergedClean.csv")