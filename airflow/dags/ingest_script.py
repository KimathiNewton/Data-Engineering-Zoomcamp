

import os
from time import time
import pandas as pd
from sqlalchemy import create_engine


def ingest_callable(user, password, host, port, db, table_name, csv_file, parquet_file, execution_date):

    print(table_name,parquet_file,execution_date)

    # Convert Parquet to CSV
    print(f"Converting {parquet_file} to CSV...")
    df = pd.read_parquet(parquet_file)
    df.to_csv(csv_file, index=False)
    
    # Set up the database connection
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect() 

    print("Connection Established Successfully, Waiting for Data....")

    t_start = time
    df_iter = pd.read_csv(csv_file, iterator=True, chunksize=100000)


    # Download the file
    result = os.system(f"curl -o {parquet_file} {url}")
    if result != 0:
        raise FileNotFoundError(f"Failed to download the file from {url}")
    
    # Convert Parquet to CSV
    print(f"Converting {parquet_file} to CSV...")
    df = pd.read_parquet(parquet_file)
    df.to_csv(csv_file, index=False)



    # Process first chunk and create table
    df = next(df_iter)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')

    print("Data loaded into the database. Inserting chunks...")
    while True:
        t_start = time()
        try:
            df = next(df_iter)
        except StopIteration:
            print("Finished ingesting data into the PostgreSQL database.")
            break


        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

        df.to_sql(name=table_name, con=engine, if_exists='append')
