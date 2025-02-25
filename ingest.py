#!/usr/bin/env python
# coding: utf-8

import os
import argparse
from time import time
import pandas as pd
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    # Determine file extension
    if url.endswith('.parquet.gz'):
        parquet_name = 'output.parquet.gz'
    else:
        parquet_name = 'output.parquet'

    csv_name = "output.csv"

    # Download the file
    print(f"Downloading file from {url}...")
    result = os.system(f"curl -o {parquet_name} {url}")
    if result != 0:
        raise FileNotFoundError(f"Failed to download the file from {url}")
    
    # Convert Parquet to CSV
    print(f"Converting {parquet_name} to CSV...")
    df = pd.read_parquet(parquet_name)
    df.to_csv(csv_name, index=False)

    # Set up the database connection
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)

    # Process first chunk and create table
    df = next(df_iter)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    df.to_sql(name=table_name, con=engine, if_exists='append')

    print("Data loaded into the database. Inserting chunks...")
    while True:
        try:
            t_start = time()
            df = next(df_iter)
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
            df.to_sql(name=table_name, con=engine, if_exists='append')
            t_end = time()
            print(f"Inserted another chunk, took {t_end - t_start:.3f} seconds.")
        except StopIteration:
            print("Finished ingesting data into the PostgreSQL database.")
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')
    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')
    parser.add_argument('--table_name', required=True, help='name of the table where we will write the results to')
    parser.add_argument('--url', required=True, help='URL of the Parquet file')
    args = parser.parse_args()
    main(args)
