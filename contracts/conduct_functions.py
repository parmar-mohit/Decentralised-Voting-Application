from web3 import Web3
from solcx import compile_source
import os
import pickle


def deploy_contract(election_name,private_key,wallet_address):
    web3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))


    fin = open("./contracts/Election.sol","r")
    contract_source_code = fin.read()
    fin.close()

    compiled_sol = compile_source(contract_source_code)
    contract_interface = compiled_sol[list(compiled_sol.keys())[0]]

    contract = web3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']
    )

    if not os.path.exists("./Deployed_Contracts/"+election_name):
        os.makedirs("./Deployed_Contracts/"+election_name)

    fout = open("./Deployed_Contracts/{}/contract.abi".format(election_name),"wb")
    pickle.dump(contract_interface["abi"],fout)
    fout.close()

    fout = open("./Deployed_Contracts/{}/contract.bin".format(election_name),"wb")
    pickle.dump(contract_interface["bin"],fout)
    fout.close()

    constructor_arguments = [election_name]

    transaction = contract.constructor(*constructor_arguments).build_transaction({
    'chainId': 1337,
    'gas': 2000000,
    'gasPrice': web3.to_wei('20', 'gwei'),
    'nonce': web3.eth.get_transaction_count(wallet_address),
    })

    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)

    transaction_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

    tx_receipt = web3.eth.wait_for_transaction_receipt(transaction_hash)

    contract_address = tx_receipt['contractAddress']

    fout = open("./Deployed_Contracts/{}/contract.adr".format(election_name),"w")
    fout.write(tx_receipt['contractAddress'])
    fout.close()

    return contract_address

def startElection(contract,private_key,wallet_address):
    web3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))

    transaction = contract.functions.startElection().build_transaction({
    'chainId': 1337,
    'gas': 2000000,
    'gasPrice': web3.to_wei('20', 'gwei'),
    'nonce': web3.eth.get_transaction_count(wallet_address),
    })

    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)
    result = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    return result

def endElection(contract,private_key,wallet_address):
    web3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))

    transaction = contract.functions.endElection().build_transaction({
    'chainId': 1337,
    'gas': 2000000,
    'gasPrice': web3.to_wei('20', 'gwei'),
    'nonce': web3.eth.get_transaction_count(wallet_address),
    })

    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)
    web3.eth.send_raw_transaction(signed_transaction.rawTransaction)

def addCandidate(candidateName,contract,private_key,wallet_address):
    web3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))

    transaction = contract.functions.addCandidate(candidateName).build_transaction({
    'chainId': 1337,
    'gas': 2000000,
    'gasPrice': web3.to_wei('20', 'gwei'),
    'nonce': web3.eth.get_transaction_count(wallet_address),
    })

    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return tx_receipt["status"]

def getVotes(contract,private_key,wallet_address):
    result = contract.functions.getVotes().call()
    return result       # [[candidateName],[votes]]

def isElectionRunning(contract):
    result = contract.functions.isElectionRunning().call()
    return result