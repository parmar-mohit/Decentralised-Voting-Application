import tkinter as tk
from tkinter import ttk
import pickle
from web3 import Web3
from contracts.voter_functions import getCandidates, hasVoted, voteCandidate
from tkinter import messagebox

def showElectionVote(election_name,private_key,wallet_address):
    def vote_button_on_click():
        candidate_name = candidate_combobox.get()

        if not candidate_name:
            messagebox.showerror("Candidate Name", "Please Select Candidate Name")
            return

        if hasVoted(my_contract,wallet_address):
            messagebox.showerror("Voter","You have already casted a vote you cannot vote again")
            return
        
        voteCandidate(my_contract, candidate_name, private_key, wallet_address)
        messagebox.showinfo("Vote"," Your vote has been casted successfully")


    # Reading Contract
    fin = open("./Deployed_Contracts/{}/contract.adr".format(election_name),"r")
    contract_address = fin.read()
    fin.close()

    fin = open("./Deployed_Contracts/{}/contract.abi".format(election_name),"rb")
    contract_abi = pickle.load(fin)
    fin.close()

    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:7545"))
    my_contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi,
    )
    
    root = tk.Tk()
    root.geometry('500x300')
    root.title("Voter : Vote")
    root.configure(bg='#f2f2f2')

    select_candidate_label = tk.Label(root,text="Select Candidate",fg="#00b33c",font=("Arial",16))
    candidate_list = getCandidates(my_contract)
    candidate_combobox = ttk.Combobox(root,values=candidate_list)
    vote_button = tk.Button(root,text="Vote",fg="#00b33c",font=("Arial",16),command=vote_button_on_click)

    select_candidate_label.pack(pady=10)
    candidate_combobox.pack(pady=10)
    vote_button.pack(pady=10)

    root.mainloop()