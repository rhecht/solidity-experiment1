from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./contracts/SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()
    #print(simple_storage_file)
    #Compile Our Solidity

install_solc("0.7.0")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*" : {"*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]}
            }
        },
    },
    solc_version="0.7.0"
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
    ]["object"]
    
#get abi
abi=compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# for connecting to ganache
# test variables from ganache
#w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/48f91ad494244b1892fe3f768c5cf4af"))

# get chain_id from chainid.network
#chain_id = 1337
chain_id = 4 #rinkeby

my_address = os.getenv("PUBLIC_KEY")
print(os.getenv("SOME_OTHER_VAR"))

#private_key = "0xbf1c2259d231d6f21f7b9be81b57c54cc37f415796d58f13e5a26f6f26ec6cf0"

#Set up private key in Terminal Fas an environment variable as follows:
# export PRIVATE_KEY=0xbf1c2259d231d6f21f7b9be81b57c54cc37f415796d58f13e5a26f6f26ec6cf0
# echo $PRIVATE_KEY
# problem is that the environment variable will be gone once shell is closed.
# apparently there's a more effective way when moving to Brownie for private key management
# python dot-env -  https://pypi.org/project/python-dotenv/

private_key=os.getenv("PRIVATE_KEY")
print(private_key)

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
#print(SimpleStorage )

nonce = w3.eth.getTransactionCount(my_address)

#print(nonce)

# 1. build a transaction
# 2. sign a transaction
# 3. send a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)
#print(transaction)

signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

#send this signed transaction
print("Deploying contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!")

# working with the contract, you always need
# contract address

# contract ABI
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# Call -> Simulate making the call and getting a return value
# Transact -> Actually making a state change

#initial value of favorite number
print(simple_storage.functions.retrieve().call())
print("Updating Contract...")

store_transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce + 1}
)
signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Updated!")
print(simple_storage.functions.retrieve().call())
#print(simple_storage.functions.store(15).call())


#print(abi)
# print(compiled_sol)

#  4:27:56 https://www.youtube.com/watch?v=M576WGiDBdQ&ab_channel=freeCodeCamp.org