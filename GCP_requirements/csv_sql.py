import csv
import sqlparse

csv_file = 'C:\Users\sunny\Downloads\olympic_event.csv'
sql_file = 'C:\Users\sunny\OneDrive\Desktop\data.sql'


def escape_sql(value):
    if value is not None:
        return value.replace("'", "''")
    return ''

def format_value(value, data_type):
    if value is None or value.strip() == '':
        return 'NULL'
    value = escape_sql(value)
    if data_type == 'TEXT':
        return f"'{value}'"
    return value

def infer_data_type(value):
    if value.isdigit():
        return 'INTEGER'
    try:
        float(value)
        return 'FLOAT'
    except ValueError:
        return 'TEXT'

with open(csv_file, 'r') as csvf, open(sql_file, 'w') as sqlf:
    reader = csv.reader(csvf)
    headers = next(reader)
    table_name = 'my_table'

    # Define the data types for each column (could be improved with actual data analysis)
    column_types = {
        'ID': 'INTEGER',
        'Name': 'TEXT',
        'Sex': 'TEXT',
        'Age': 'INTEGER',
        'Height': 'FLOAT',
        'Weight': 'FLOAT',
        'Team': 'TEXT',
        'NOC': 'TEXT',
        'Games': 'TEXT',
        'Year': 'INTEGER',
        'Season': 'TEXT',
        'City': 'TEXT',
        'Sport': 'TEXT',
        'Event': 'TEXT',
        'Medal': 'TEXT'
    }

    for row in reader:
        values = [
            format_value(value, column_types[header])
            for value, header in zip(row, headers)
        ]
        sql = f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES ({', '.join(values)});\n"
        sqlf.write(sql)

# Optionally format the SQL for better readability
with open(sql_file, 'r') as sqlf:
    formatted_sql = sqlparse.format(sqlf.read(), reindent=True, keyword_case='upper')

with open(sql_file, 'w') as sqlf:
    sqlf.write(formatted_sql)
