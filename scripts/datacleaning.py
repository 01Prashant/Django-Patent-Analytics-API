import os
import pandas as pd
import sqlite3

# Path to the CSV file
csv_file_path = '../data/patent_data.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

# 1. Remove rows where 'title' or 'assignee' is empty
df = df.dropna(subset=['title', 'assignee'])

# 2. Replace empty 'inventor/author' with 'unknown'
df['inventor/author'].fillna('unknown', inplace=True)

# 3. Replace empty 'representative figure link' with 'none'
df['representative figure link'].fillna('none', inplace=True)

# 4. Handle missing 'grant date'
df['grant date'] = df.apply(
    lambda row: row['publication date'] if pd.isna(row['grant date']) and pd.notna(row['publication date']) else row['grant date'],
    axis=1
)
df['grant date'] = df.apply(
    lambda row: row['grant date'] if pd.notna(row['grant date']) else row['publication date'],
    axis=1
)
df = df.dropna(subset=['grant date'])

print(df.isnull().sum())

# Add index as a column named 'id'
df.reset_index(inplace=True)

df.rename(columns={
    'id'                            : 'patent_id',
    'index'                         : 'id',
    'inventor/author'               : 'inventor',
    'priority date'                 : 'priority_date',
    'filing/creation date'          : 'filing_date',
    'publication date'              : 'publication_date',
    'grant date'                    : 'grant_date',
    'result link'                   : 'result_link',
    'representative figure link'    : 'representative_figure_link'
}, inplace=True)

# Save to SQLite database
database_path = '../patentProject/db.sqlite3'
connection = sqlite3.connect(database_path)
df.to_sql('patentApp_patent', connection, if_exists='replace', index=False)

print("Data saved to SQLite database 'patentProject/db.sqlite3' in table 'patentApp_patent'.")

# Close the connection
connection.close()


# # Save data to Django models
# for _, row in df.iterrows():
#     Patent.objects.update_or_create(
#         patent_id=row.get('patent_id'),
#         defaults={
#             'title': row.get('title'),
#             'assignee': row.get('assignee'),
#             'inventor': row.get('inventor'),
#             'priority_date': row.get('priority_date'),
#             'filing_date': row.get('filing_date'),
#             'publication_date': row.get('publication_date'),
#             'grant_date': row.get('grant_date'),
#             'result_link': row.get('result_link'),
#             'representative_figure_link': row.get('representative_figure_link'),
#         }
#     )

# print("Data successfully imported into Django models.")
