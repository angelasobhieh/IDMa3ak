from web3 import Web3
import json

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))

# Load and compile Solidity contract
with open("contracts/compiled/IdentityVerification.json", "r") as file:
    compiled_contract = json.load(file)

abi = compiled_contract["abi"]
bytecode = compiled_contract["bytecode"]

contract = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = contract.constructor().transact({'from': w3.eth.accounts[0]})
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("Contract deployed at:", tx_receipt.contractAddress)
