'''
Aggregate data
'''
import os
import pandas as pd
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime


if __name__ == "__main__":
    data_dir = "data"
    output_dir = "output"

    df = pd.DataFrame([])
    for root, dirs, files in os.walk(data_dir):
         for file in files:
            df=df.append(pd.read_csv(os.path.join(root,file)))
            
    df['hour'] = pd.to_datetime(df.create_ts)
    df["convertedStoragePoints_cfx"] = df["convertedStoragePoints"] / 1024
    df=df.set_index(df["hour"])
    df=df.resample('1H').min().dropna()

    if df.size > 0:
        filename = '{}_aggregate_supply_and_burn.csv'.format(''.join(filter(str.isalnum, df["create_ts"].max())))
        df.drop('hour', axis=1).to_csv(
            os.path.join(output_dir, filename),
            index=False
        )