import pandas as pd
import numpy as np

def productivity() -> pd.DataFrame:
    # https://www.ons.gov.uk/generator?format=csv&uri=/employmentandlabourmarket/peopleinwork/labourproductivity/timeseries/lzvb/prdy

    # Read data/productivity.csv from line 60, with columns Date and Productivity
    df = pd.read_csv('data/productivity.csv', skiprows=60, names=['Date', 'Productivity'], header=None)

    # Split Date into Year and Quarter, which are separated by ' Q'
    df['Year'] = df['Date'].str.split(' ').str[0]
    df['Quarter'] = df['Date'].str.split(' Q').str[1]

    # Drop the date column
    df = df.drop('Date', axis=1)

    # Convert all columns to numeric
    df = df.apply(pd.to_numeric)

    df = df.reindex(df.index.repeat(3))

    # Add a new column - 'Month'. Start at quarter 2, so month 4
    df['Month'] = 1
    df['Month'] = df['Month'].cumsum() + 3

    df['Month'] = df['Month'] % 12
    df['Month'] = df['Month'].replace(0, 12)

    # Set index to [Year, Month]
    df = df.set_index(['Year', 'Month'])

    return df


def median_pay() -> pd.DataFrame:
    # https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/bulletins/annualsurveyofhoursandearnings/2022

    df = pd.read_csv('data/weekly_pay.csv', skiprows=10, names=['Year', 'Full-Time', 'Part-Time', 'All'], header=None)

    # Create a new column - 'Month'
    df['Month'] = 1

    # Duplicate each row 12 times
    df = df.reindex(df.index.repeat(12))

    # Set month correctly, resetting cumsum() each year
    df['Month'] = df['Month'].cumsum()
    df['Month'] = df['Month'] % 12
    df['Month'] = df['Month'].replace(0, 12)

    # Set index to [Year, Month]
    df = df.set_index(['Year', 'Month'])

    # Convert all columns to numeric
    df = df.apply(pd.to_numeric)

    # Convert to monthly pay
    df['Full-Time'] = df['Full-Time'] * 4.33
    df['Part-Time'] = df['Part-Time'] * 4.33
    df['All'] = df['All'] * 4.33

    for index, row in df.iterrows():
        year, month = index
        if year > 2021:
            break

        # Calculate the difference between the current year and the next year
        year_rate = df.loc[(year, 1)]
        next_year_rate = df.loc[(year + 1, 1)]
        diff = next_year_rate - year_rate

        # Calculate the monthly difference
        monthly_diff = diff / 12

        # Update the current row with the monthly difference
        row['Full-Time'] += monthly_diff['Full-Time'] * (month - 1)
        row['Part-Time'] += monthly_diff['Part-Time'] * (month - 1)
        row['All'] += monthly_diff['All'] * (month - 1)

        # Update the dataframe with the new row
        df.loc[(year, month)] = row

    # Remove data from after index (2022, 1)
    df = df.loc[:(2022, 1)]

    # df["Full-Time-Normalised"] = (df["Full-Time"] - df["Full-Time"].mean()) / df["Full-Time"].std()
    # df["Part-Time-Normalised"] = (df["Part-Time"] - df["Part-Time"].mean()) / df["Part-Time"].std()
    # df["All-Normalised"] = (df["All"] - df["All"].mean()) / df["All"].std()

    return df


def core_inflation() -> pd.DataFrame:
    # https://www.ons.gov.uk/economy/inflationandpriceindices/articles/newestimatesofcoreinflationuk/2022
    # https://www.ons.gov.uk/generator?uri=/economy/inflationandpriceindices/articles/newestimatesofcoreinflationuk/2022/29c6f303&format=csv

    df = pd.read_csv('data/core_inflation.csv', skiprows=7, names=['Date', 'CPIH', 'Core'], header=None)

    # Split Date into Year and Month
    df['Year'] = df['Date'].str.split(' ').str[0]
    df['Month'] = df['Date'].str.split(' ').str[1]

    # Drop the date column
    df = df.drop('Date', axis=1)

    # Convert Month column (Jan, Feb, etc) to numeric
    months = {
        'Jan': 1,
        'Feb': 2,
        'Mar': 3,
        'Apr': 4,
        'May': 5,
        'Jun': 6,
        'Jul': 7,
        'Aug': 8,
        'Sep': 9,
        'Oct': 10,
        'Nov': 11,
        'Dec': 12
    }

    df['Month'] = df['Month'].map(months)

    # Convert all columns to numeric
    df = df.apply(pd.to_numeric)

    # Set index to [Year, Month]
    df = df.set_index(['Year', 'Month'])

    # df["Core-Inflation-Normalised"] = (df["Core"] - df["Core"].mean()) / df["Core"].std()

    return df

# Combine all dataframes into one
df = pd.concat([productivity(), median_pay(), core_inflation()], axis=1)

# Save to csv
# df.to_csv('data/combined.csv')

# If a row has any NaN values, drop it
df = df.dropna()
# print(df)
df.to_csv('data/combined_nonan.csv')