import pandas as pd

def cleanDF(df):
    all_cols = ['ID', 'Language', 'Subscription Type', 'Subscription Event Type',
       'Purchase Store', 'Purchase Amount', 'Currency',
       'Subscription Start Date', 'Subscription Expiration', 'Demo User',
       'Free Trial User', 'Free Trial Start Date', 'Free Trial Expiration',
       'Auto Renew', 'Country', 'User Type', 'Lead Platform',
       'Email Subscriber', 'Push Notifications', 'Send Count', 'Open Count',
       'Click Count', 'Unique Open Count', 'Unique Click Count',
       'App Session Platform', 'App Activity Type', 'App Session Date']

