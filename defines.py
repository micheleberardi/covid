from datetime import datetime, timedelta

import requests
from dateutil.parser import parse

def get_country_confirmed_infected(country, start_date, end_date):
    resp = requests.get(f"https://api.covid19api.com/country/{country}/status/confirmed", params={"from": start_date, "to": end_date})
    if resp.status_code == 404:
        return False
    else:
        return resp.json()

def main(country):
    country = country
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    print("Getting COVID data by Michelone")
    cases = get_country_confirmed_infected(country, week_ago, today)
    if cases == False:
        response = "COUNTRY NOT EXIST"
        return response
    else:
        latest_day = cases[-1]
        earliest_day = cases[0]
        percentage_increase = (latest_day['Cases'] - earliest_day['Cases']) / (earliest_day['Cases'] / 100)
        msg = f"There were {latest_day['Cases']} confirmed COVID cases in {country} " \
            f"on {parse(latest_day['Date']).date()}\n"
        if percentage_increase > 0:
            msg += f"This is {round(abs(percentage_increase), 4)}% increase over the last week. " \
               f"Travel is not recommended in {country}"
        else:
            msg += f"This is {round(abs(percentage_increase), 4)}% decrease over the last week. " \
               f"Travel may be OK in {country}"
        print(msg)
        print("Job finished successfully")
        response = "Getting COVID data by Michelone \n " +str(msg)
        return response