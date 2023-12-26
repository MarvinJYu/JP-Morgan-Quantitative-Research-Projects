# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 16:58:36 2023

@author: Jiachen
"""
from datetime import datetime
import pandas as pd
import calendar
from dateutil.relativedelta import relativedelta

# import the settlement price data
data = pd.read_csv('Nat_Gas.csv', index_col='Dates', parse_dates=True, date_format='%m/%d/%Y')

# define the function to price the contract
def contract_price(injection_date, withdrawn_date, rate, storage_fee, max_vol=1000000):
    '''

    Parameters
    ----------
    injection_date : string
        The date when the contract starts. Format: 'mm/dd/yy'
    withdrawn_date : string
        The date when the contract ends.Format: 'mm/dd/yy'
    rate : number
        Injection or withdrawn rate.
    storage_fee : number
        Storage fee on monthly basis from storage facility.
    max_vol : number
        Maximum volumn that can be stored in the storage facility, without specific mentioning, the default max storage volumn would be 1 million
    
    Returns
    -------
    Contract price based on the income minus all relative costs.

    '''
    # convert the injection_date and withdrawn_date to datetime type
    inj_date = datetime.strptime(injection_date, '%m/%d/%y')
    end_date = datetime.strptime(withdrawn_date, '%m/%d/%y')
    
    # define a function to convert the injection_date and withdrawn_date to the last day of the month
    def last_day_of_month(date):
        # Find the last day of the month
        _, last_day = calendar.monthrange(date.year, date.month)
    
        # If the given date is not the last day, adjust to the last day
        if date.day != last_day:
            date = date.replace(day=last_day)

        return date
    
    # conver the date to string
    inj_adj_date = last_day_of_month(inj_date).strftime('%#m/%d/%y')
    end_adj_date = last_day_of_month(end_date).strftime('%#m/%d/%y')
    
    # using the date string to infer the prices at each timestamp
    inj_price = data.loc[inj_adj_date]
    end_price = data.loc[end_adj_date]
    
    # calculate the income of the transaction
    income = (end_price - inj_price)*max_vol
    
    # calculate storage cost
    # compute the number of months between the injection and withdrawn date
    delta = relativedelta(last_day_of_month(end_date), last_day_of_month(inj_date))
    month_diff = delta.years * 12 + delta.months
    # compute the storage cost in total
    storage_cost = storage_fee * month_diff
    
    # calculate the injection/withdrawn cost
    operation_cost = rate * max_vol
    
    # calculate the final price of the contract
    price = income - storage_cost - operation_cost
    return price

    
    