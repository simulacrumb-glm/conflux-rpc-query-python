import os
import time
from web3 import Web3 
#https://web3py.readthedocs.io/en/stable/quickstart.html
#from web3.gas_strategies.rpc import rpc_gas_price_strategy

#number of sequential transactions to send
batch_size = 10

''' gas price and gas max to use
    raise during active times, or look into using a gas strategy
    for more advanced usage: https://web3py.readthedocs.io/en/stable/gas_price.html
'''
gas_price = web3.to_wei('21', 'gwei')
gas = 50000

''' Network Endpoints
    US and HK endpoints may perform differently during times of high activity
    https://doc.confluxnetwork.org/docs/espace/network-endpoints
'''
provider_rpc = {
    "core_testnet": "https://test.confluxrpc.org",
    "core_mainnet": "https://main.confluxrpc.org",
    "core_mainnet_hk": "https://main.confluxrpc.com",
    "evm_testnet": "https://evmtestnet.confluxrpc.org",
    "evm_mainnet": "https://evm.confluxrpc.org",
    "evm_mainnet_hk": "https://evm.confluxrpc.com",
}
web3 = Web3(Web3.HTTPProvider(provider_rpc["evm_mainnet"]))


''' Coin Specific calldata
    https://cfxscriptions.com/inscriptions
'''
#calldata_str= 'data:,{"p":"cfxs-20","op":"mint","tick":"pepe","amt":"1000"}'
#calldata_str= 'data:,{"p":"cfxs-20","op":"mint","tick":"hope","amt":"1000"}'
#calldata_str= 'data:,{"p":"cfxs-20","op":"mint","tick":"MEOW","amt":"250"}'
#calldata_str= 'data:,{"p":"cfxs-20","op":"mint","tick":"888","amt":"8"}'
#calldata_str= 'data:,{"p":"cfxs-20","op":"mint","tick":"SIMULACRA","amt":"1"}'
#calldata_str= 'data:,{"p":"cfxs-20","op":"mint","tick":"CFXScriptions","amt":"10000"}'
calldata_str= 'data:,{"p":"cfxs-20","op":"mint","tick":"BSIM","amt":"1000"}'
#minted out
#calldata_str= 'data:,{"p":"cfxs-20","op":"mint","tick":"CFX","amt":"1000"}'
#calldata_str= 'data:,{"p":"cfxs-20","op":"mint","tick":"XFC","amt":"1"}'

hex_data=web3.to_hex(calldata_str.encode('utf-8'))

''' Wallet Config
        Best practice is to set 'address' and 'private_key' values via terminal or .env script
        faillback, paste them into the variables below, but be careful, NEVER EVER share your private_key
    Windows cmd example:
        set private_key=yourprivatekey
        set address=youraddress
    Jupyter Notebook example
        ! set private_key=yourprivatekey
        ! set address=youraddress
    MacOS and *nix shell example
        export private_key=yourprivatekey
        export address=youraddress
'''
yourprivatekey = ""
youraddress = ""


if __name__ == '__main__':
    
    account_from = {
        "private_key": os.environ.get("private_key", yourprivatekey), # this will prioritize env variable 'private_key', then 'yourprivatekey'
        "address": os.environ.get("address", youraddress),  # this will prioritize env variable 'address', then 'yourprivatekey'
    }
    assert account_from["private_key"], 'account_from["private_key"] is not set'
    assert account_from["address"], 'account_from["address"] is not set'

    address_to = account_from["address"]
    start_nonce = web3.eth.get_transaction_count(
        Web3.to_checksum_address(account_from["address"])
    )
    cache = []
    for i in range(batch_size):
        nonce = start_nonce + i 

        # https://web3py.readthedocs.io/en/stable/transactions.html
        tx_create = web3.eth.account.sign_transaction(
            {
                "nonce": nonce,
                "gasPrice": gas_price,
                "gas": gas,
                "to": Web3.to_checksum_address(address_to),
                "value": web3.to_wei(0, "wei"),
                "data": hex_data
            },
            account_from["private_key"],
        )
        cache.append(tx_create)

    print("packed %s transactions" % (batch_size) )  
    start = time.time()
    print("Starting to send transactions @ %s " % (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))) )
    res = [web3.eth.send_raw_transaction(j.rawTransaction) for j in cache]
    print("Sent %s transactions in %s seconds" % (batch_size, time.time() - start) )
    print("From: %s" % (account_from["address"]) )
    print("To: %s" % (address_to) )
    print("Last Nonce hash: %s" % (res[-1].hex()) )
    print(nonce)
    print(gas_price)
