import pandas as pd
import numpy as np

# Load the CSV file
data = pd.read_csv('/Users/adwaith/Documents/University/Final Year/Data Mining/Combined.csv')

# Define cyclical embedding function
def cyclical_embedding(value, max_value):
    sin_val = np.sin(2 * np.pi * value / max_value)
    cos_val = np.cos(2 * np.pi * value / max_value)
    return sin_val, cos_val

# Apply cyclical embedding on Normalised GDP
data['GDP_sin'], data['GDP_cos'] = zip(*data['Normalised GDP'].apply(lambda x: cyclical_embedding(x, data['Normalised GDP'].max())))

# Apply cyclical embedding on Normalised Temperature
data['Temperature_sin'], data['Temperature_cos'] = zip(*data['Normalised Temperature'].apply(lambda x: cyclical_embedding(x, data['Normalised Temperature'].max())))

# Apply cyclical embedding on Normalised Unemployment Rate
data['Unemployment_Rate_sin'], data['Unemployment_Rate_cos'] = zip(*data['Normalised Unemployment Rate'].apply(lambda x: cyclical_embedding(x, data['Normalised Unemployment Rate'].max())))

# Save the results to a new CSV file
data.to_csv('data_cyclical_embedding.csv', index=False)
