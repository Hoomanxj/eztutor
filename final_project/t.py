import pandas as pd
from sqlalchemy import create_engine

# Connect to your database (replace with your actual connection string)
engine = create_engine('mysql+pymysql://root:Whoman946626@localhost/eztutor')

# Query all data from a table and load it into a pandas DataFrame
df = pd.read_sql('SELECT * FROM Student', engine)

# Print the table data
print(df)
