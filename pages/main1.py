import pandas as pd

# Load the Excel file
file_path = 'ROO.xlx'
df = pd.read_excel(file_path, engine='openpyxl')

# Initialize an empty list to collect rows for the transformed data
data = []

# Extract the classification, section, and account columns
classification_column = 'CLASSIFICATION'
section_column = 'SECTION'
account_column = 'ACCOUNT'

# Define the streams
streams = ['SEA', 'INLAND', 'RORO', 'COURIER', 'AIR', 'WHSE', 'OTHERS']

# Iterate over each month and stream to reshape the data
months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

for month in months:
    # Find the starting index of the month column
    month_index = df.columns.get_loc(month)
    
    # Iterate over each stream
    for i, stream in enumerate(streams):
        stream_column = df.columns[month_index + i + 1]
        
        # Collect data for each account
        for index, row in df.iterrows():
            classification = row[classification_column]
            section = row[section_column]
            account = row[account_column]
            revenue = row[stream_column]
            
            # Append the row to the data list
            data.append([classification, section, account, stream, month, revenue])

# Create a DataFrame from the collected data
transformed_df = pd.DataFrame(data, columns=['CLASSIFICATION', 'SECTION', 'ACCOUNT', 'STREAM', 'MONTH', 'REVENUE'])

# Save the transformed data to a new Excel file
transformed_df.to_excel('Transformed_Budget.xlsx', index=False)

print("The data has been successfully transformed and saved to 'Transformed_Budget.xlsx'.")




