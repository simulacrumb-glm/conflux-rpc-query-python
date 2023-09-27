import os
import pandas as pd
import requests
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

# import sys
# print (f'Written with Python version: { sys.version }')
# # Written with Python version: 3.9.7
# # cmd.exe /C C:\ProgramData\Anaconda3\Scripts\activate.bat C:\ProgramData\Anaconda3 && C:\ProgramData\Anaconda3\python.exe fetch_data.py

'''
cfx_getSupplyInfo in simple python
    convert to human readable decimal
    add datetime for context
'''
def fetch_supply():
    url = 'https://main.confluxrpc.com'
    parameters = {"jsonrpc":"2.0","method":"cfx_getSupplyInfo","params":[],"id":1}
    headers = {'Content-Type': 'application/json'}

    resp=requests.post(url, json=parameters, headers=headers)
    res = resp.json()["result"]

    # hex_to_decimal & Wei to whole coin decimal
    converted = {k: int(v,16) / 10**18 for k, v in res.items()}
    # created datetime as ISO_8601 string
    converted["create_ts"] = "{}".format(parsedate_to_datetime(resp.headers["Date"]).isoformat())
    return converted


'''
cfx_getCollateralInfo in simple python
    convert to human readable decimal
    add datetime for context
'''
def fetch_collateral():
    url = 'https://main.confluxrpc.com'
    parameters = {
        "jsonrpc": "2.0",
        "method": "cfx_getCollateralInfo",
        "params": [],
        "id": 0
    }
    headers = {'Content-Type': 'application/json'}

    resp=requests.post(url, json=parameters, headers=headers)
    res = resp.json()["result"]

    # hex_to_decimal
    converted = {k: int(v,16) for k, v in res.items()}
    # Wei to whole coin decimal
    converted["totalStorageTokens"] = converted["totalStorageTokens"] / 10**18
    # created datetime as ISO_8601 string
    converted["create_ts"] = "{}".format(parsedate_to_datetime(resp.headers["Date"]).isoformat())
    return converted


if __name__ == "__main__":
    data_dir = ".\\data"
    datastore=[]
    datastore.append(fetch_supply())
    datastore.append(fetch_collateral())
    df = pd.DataFrame(datastore)
    filename = ''.join(filter(str.isalnum, df.loc[0]["create_ts"])) + str(".csv")
    if df.size > 0:
        df.to_csv(
            os.path.join(data_dir, filename),
            index=False
        )

