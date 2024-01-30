#!/usr/bin/env python
# coding: utf-8
import argparse
import os
from time import time

import pandas as pd
from sqlalchemy import create_engine


def main(params):
    """
    Argparse parameters:
    user
    password
    host
    port
    db_name
    table_name
    csv_name
    """
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db_name = params.db_name
    table_name = params.table_name
    csv_url = params.csv_url
    csv_zone_url = params.csv_zone_url

    csv_name = "output.csv"

    os.system(f"wget {csv_url} -O {csv_name}.gz")
    os.system(f"gzip -dk {csv_name}.gz")
    os.system(f"wget {csv_zone_url}")

    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db_name}")
    engine.connect()

    # taxi zones lookup
    df_zones = pd.read_csv("taxi+_zone_lookup.csv")
    df_zones.to_sql(name="zones", con=engine, if_exists="replace")

    # taxi trip data
    df = pd.read_csv(csv_name, nrows=100)
    df.head(0).to_sql(name=table_name, con=engine, if_exists="replace")
    print(pd.io.sql.get_schema(df, name=table_name, con=engine))
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=1000, low_memory=False)

    ctr = 1
    while True:
        t_start = time()
        ctr += 1
        try:
            df = next(df_iter)
        except Exception:
            print(f"ERROR{'@'*30}")
            break
        print(f"iteration: {ctr*chunk_size}")
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        df.to_sql(name=table_name, con=engine, if_exists="append")
        t_end = time()
        print(f"Inserted another chunck..., took {t_end-t_start:.3f} seconds")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")
    parser.add_argument("--user", help="user")
    parser.add_argument("--password", help="password")
    parser.add_argument("--host", help="host")
    parser.add_argument("--port", help="port")
    parser.add_argument("--db_name", help="db name")
    parser.add_argument("--table_name", help="table name")
    parser.add_argument("--csv_url", help="url of the csv")
    parser.add_argument("--csv_zone_url", help="url of the zone lookup csv")

    args = parser.parse_args()
    main(args)
