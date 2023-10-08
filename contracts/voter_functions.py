import os
import pickle
from web3 import Web3

def isElectionRunning(contract):
    result = contract.functions.isElectionRunning().call()
    return result

def getElectionNames():
    names = []
    path = "./Deployed_Contracts"
    for contract_name in os.listdir(path):
        contract_path = path + "/" + contract_name

        fin = open(contract_path+"/contract.abi","rb")
        abi = pickle.load(fin)
        fin.close()

        fin = open(contract_path+"/contract.adr","r")
        adr = fin.read()
        fin.close()

        w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))

        contract = w3.eth.contract(
            address=adr,
            abi=abi,
        )

        if isElectionRunning(contract):
            names.append(contract_name)

    return names

def getCandidates(contract):
    return contract.functions.getCandidates().call()

def hasVoted(contract,wallet_address):
    web3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545")) 
    return contract.functions.hasVoted(web3.to_checksum_address(wallet_address)).call()

def voteCandidate(contract,candidate,private_key,wallet_address):
    web3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))

    transaction = contract.functions.voteCandidate(candidate).build_transaction({
    'chainId': 1337,
    'gas': 2000000,
    'gasPrice': web3.to_wei('20', 'gwei'),
    'nonce': web3.eth.get_transaction_count(wallet_address),
    })

    signed_transaction = web3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_transaction.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)