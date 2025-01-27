#!/usr/bin/env python3
"""
Fetch data from https://www.hvakosterstrommen.no/strompris-api
and visualize it.

Assignment 5
"""
from __future__ import annotations

import datetime
import warnings

import altair as alt
import pandas as pd
import requests
import requests_cache

# install an HTTP request cache
# to avoid unnecessary repeat requests for the same data
# this will create the file http_cache.sqlite
requests_cache.install_cache()

# suppress a warning with altair 4 and latest pandas
warnings.filterwarnings("ignore", ".*convert_dtype.*", FutureWarning)


# task 5.1:


def fetch_day_prices(date: datetime.date = None, location: str = "NO1") -> pd.DataFrame:
    """Fetch one day of data for one location from hvakosterstrommen.no API

    """
    if date is None:
        date = datetime.date.today()

    url = f"https://www.hvakosterstrommen.no/api/v1/prices/{date.year}/{date.month:02d}-{date.day:02d}_{location}.json"
    response = requests.get(url)
    # Parse the json reponse
    date = response.json()
    df = pd.DataFrame(date)

    # Convert the 'time_start' column to datetime format
    df['time_start'] = pd.to_datetime(df['time_start'])

    return df[['NOK_per_kWh', 'time_start']]


# LOCATION_CODES maps codes ("NO1") to names ("Oslo")
LOCATION_CODES = {"NO1": "Oslo", "NO2": "Kristiansand",
                  "NO3": "Trondheim", "NO4": "Tromsø", "NO5": "Bergen"}

# task 1:


def fetch_prices(
    end_date: datetime.date = None,
    days: int = 7,
    locations: list[str] = tuple(LOCATION_CODES.keys()),
) -> pd.DataFrame:
    """Takes a given time, number of days and locations and
    generates the prices for multiple days and locatons into a single
    DataFrame.

    """

    if end_date is None:
        end_date = datetime.date.today()

    # Initialize an empty DataFrame to store the results
    result_df = pd.DataFrame()

    for location in locations:
        for i in range(days):
            date = end_date - datetime.timedelta(i)
            prices_df = fetch_day_prices(date, location)

            # Add location code and name columns
            prices_df['location_code'] = location
            prices_df['location'] = LOCATION_CODES[location]

            result_df = pd.concat([result_df, prices_df], ignore_index=True)

    return result_df


# task 5.1:


def plot_prices(df: pd.DataFrame) -> alt.Chart:
    """Generate an Altair line chart to visualize
    energy prices over time. Each location is represented by a separate line 
    on the chart. The x-axis consist of time_start, the y-axis is the price in
    NOK.
    
    """
    chart = alt.Chart(df).mark_line().encode(
        x='time_start:T',
        y='NOK_per_kWh:Q',
        color='location:N',
        tooltip=['location', 'time_start', alt.Tooltip(
            'NOK_per_kWh:Q', format='.2f', title='Price (NOK/kWh)')]
    ).properties(
        title='Electricity Prices Over Time',
        width=800,
        height=400
    )

    return chart


# Task 5.4


def plot_daily_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot the daily average price

    x-axis should be time_start (day resolution)
    y-axis should be price in NOK

    You may use any mark.

    Make sure to document arguments and return value...
    """
    raise NotImplementedError("Remove me when you implement this task (in4110 only)")
    ...


# Task 5.6

ACTIVITIES = {
    # activity name: energy cost in kW
    ...
}


def plot_activity_prices(
    df: pd.DataFrame, activity: str = "shower", minutes: float = 10
) -> alt.Chart:
    """
    Plot price for one activity by name,
    given a data frame of prices, and its duration in minutes.

    Make sure to document arguments and return value...
    """
    raise NotImplementedError("Remove me when you implement this optional task")

    ...


def main():
    """Allow running this module as a script for testing."""
    df = fetch_prices()
    chart = plot_prices(df)
    # showing the chart without requiring jupyter notebook or vs code for example
    # requires altair viewer: `pip install altair_viewer`
    chart.show()


if __name__ == "__main__":
    main()
