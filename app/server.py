from flask import Flask, request, jsonify
from blockchain.blockchain import Blockchain
from web3 import Web3

app = Flask(__name__)
blockchain = Blockchain(authority="Authority_Node_1")

# Web3 setup
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))  # Ganache URL
contract_abi = [...]  # Contract ABI
contract_address = "0x..."  # Deployed contract address
contract = w3.eth.contract(address=contract_address, abi=contract_abi)

@app.route("/add_transaction", methods=["POST"])
def add_transaction():
    data = request.json["data"]
    blockchain.add_transaction(data)
    return jsonify({"message": "Transaction added"})

@app.route("/mine", methods=["POST"])
def mine():
    block = blockchain.mine()
    return jsonify({"block": block.__dict__}) if block else jsonify({"message": "No transactions"})

@app.route("/register_user", methods=["POST"])
def register_user():
    name = request.json["name"]
    tx_hash = contract.functions.registerUser(name).transact({"from": w3.eth.accounts[0]})
    w3.eth.wait_for_transaction_receipt(tx_hash)
    return jsonify({"message": "User registered"})

if __name__ == "__main__":
    app.run(debug=True)
