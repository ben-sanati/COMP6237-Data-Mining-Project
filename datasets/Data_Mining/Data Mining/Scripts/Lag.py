import pandas as pd

# Load the CSV file
data = pd.read_csv('/Users/adwaith/Documents/University/Final Year/Data Mining/Combined.csv')

# Define a dictionary to map month abbreviations to numbers
month_mapping = {
    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
    'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
}

# Map the month abbreviations to numbers
data['month'] = data['month'].apply(lambda x: month_mapping[x.lower()])

# Convert year and month columns to datetime format
data['date'] = pd.to_datetime(data[['year', 'month']].assign(day=1))

# Set date as index
data.set_index('date', inplace=True)

# Prepare a list of column names to create lag columns
column_names = ['Normalised GDP', 'Normalised Temperature', 'Normalised Unemployment Rate']

# Create lag columns for 1-12 months
for i in range(1, 13):
    for col in column_names:
        lag_col_name = f'{col}_lag_{i}'
        data[lag_col_name] = data[col].shift(i)

# Reset index
data.reset_index(inplace=True)

# Save the results to a new CSV file
data.to_csv('data_with_lag_columns.csv', index=False)
