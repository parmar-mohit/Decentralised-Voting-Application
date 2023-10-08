import tkinter as tk
from tkinter import ttk
from contracts.voter_functions import getElectionNames
from tkinter import messagebox
from web3 import Web3
from voter_interfaces.election_vote import showElectionVote

def showElectionListInterface(private_key,wallet_address):
    def get_balance():
        web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
        try:
            balance_wei = web3.eth.get_balance(wallet_address)
            balance_eth = web3.from_wei(balance_wei, 'ether')
            balance_label.config(text=f'Balance: {round(balance_eth,2)} ETH')
        except Exception as e:
            print(e)
            balance_label.config(text='Error fetching balance')

    def vote_button_on_click():
        election_name = election_names_combobox.get()
        if not election_name:
            messagebox.showerror("Election Name","Select Election Name")
            return
        
        root.destroy()
        showElectionVote(election_name,private_key,wallet_address)
        showElectionListInterface(private_key,wallet_address)

    root = tk.Tk()
    root.geometry('500x300')
    root.title("Voter : Election")
    root.configure(bg='#f2f2f2')

    balance_label = tk.Label(root, text='Balance: N/A', fg='#00b33c',font=("Arial",16))
    get_balance()
    
    election_label = tk.Label(root,text="Select Election",fg="#00b33c",font=("Arial",16))
    names = getElectionNames()
    election_names_combobox = ttk.Combobox(root,values=names)

    vote_button = tk.Button(root,text="Vote",fg="#00b33c",font=("Arial",16),command=vote_button_on_click)

    balance_label.pack(pady=30) 
    election_label.pack(pady=10)
    election_names_combobox.pack(pady=10)
    vote_button.pack(pady=10)

    root.mainloop()