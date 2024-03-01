#!/usr/bin/env python
# coding: utf-8

   
# Importations
import pandas as pd
from sqlalchemy import create_engine


# To create a database engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')

# Connect to the engine
con=engine.connect()



query ="""
SELECT 1 AS number
"""
pd.read_sql(query,con=engine)


# The file is downloaded as parquet file
parquet_file = 'yellow_tripdata_2021-01.parquet'


# Read Parquet file into a DataFrame
df = pd.read_parquet(parquet_file)

# Replace 'output_file.csv' with the desired CSV file name
csv_file = 'yellow_tripdata_2021-01.csv'

# Write DataFrame to CSV
df.to_csv(csv_file, index=False)




df = pd.read_csv('yellow_tripdata_2021-01.csv',nrows=100)



df.head(5)




# To convert pickup and dropoff time into datetime data type
df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)


df.info()


df.to_sql(name='yellow_tripdata',con=engine,index=False)


query = """
SELECT *
FROM pg_catalog.pg_tables
WHERE schemaname != 'pg_catalog' AND
    schemaname != 'information_schema'

"""
pd.read_sql(query,con=engine)

query ="""
SELECT * FROM yellow_taxi_data LIMIT 10;
"""
pd.read_sql(query,con=engine)


# In[34]:


df.head()

# TO convert dataframe into ddl
print(pd.io.sql.get_schema(df,name='yellow_taxi_data',con=engine))


# To chunk the csv files into small batches using iterators. We will be uploading the data in chunks

# In[11]:


df_iter = pd.read_csv('yellow_tripdata_2021-01.csv',iterator=True,chunksize=100000)


df_iter


#To get the next values of the iterators
df = next(df_iter)


df


len(df)


# In[16]:


df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)


df.head(n=0)


# To create a table with only the column names
df.head(n=0).to_sql(name='yellow_taxi_data',con=engine,if_exists='replace')


get_ipython().run_line_magic('time', "df.to_sql(name='yellow_taxi_data',con=engine,if_exists='append')")


# In[21]:


from time import time


# In[22]:


while True:
    t_start = time()
    df = next(df_iter)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.to_sql(name='yellow_taxi_data',con=engine,if_exists='append')

    t_end = time()
    print("Inserted another chunk...., it took %.3f seconds"% (t_end-t_start))
    


# In[23]:


query ="""
SELECT COUNT(*) FROM yellow_taxi_data LIMIT 10;
"""
pd.read_sql(query,con=engine)


# In[ ]:


query ="""
SELECT * FROM yellow_taxi_data LIMIT 10;
"""
pd.read_sql(query,con=engine)

